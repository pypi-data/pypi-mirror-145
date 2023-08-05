# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Selection Node

This is a SQL Query Execution Plan Node.

This Node eliminates elminiates records which do not match a predicate using a
DNF (Disjunctive Normal Form) interpretter. 

Predicates in the same list are joined with an AND/Intersection (all must be True)
and predicates in adjacent lists are joined with an OR/Union (any can be True).
This allows for non-trivial filters to be written with just tuples and lists.

The predicates are in _tuples_ in the form (`key`, `op`, `value`) where the `key`
is the value looked up from the record, the `op` is the operator and the `value`
is a literal.
"""
import numpy
from typing import Union, Iterable
from pyarrow import Table
from opteryx.engine.attribute_types import TOKEN_TYPES
from opteryx.engine.query_statistics import QueryStatistics
from opteryx.engine.planner.operations.base_plan_node import BasePlanNode
from opteryx.exceptions import SqlError
from opteryx.utils.columns import Columns


class InvalidSyntaxError(Exception):
    pass


def _evaluate(predicate: Union[tuple, list], table: Table) -> bool:
    """
    Evaluate a table against a DNF selection.

    This is done by creating a mask for the values to return - we evaluate the page
    against a predicate (including resolving child predicates) and then AND or OR the
    masks together to return the rows that match the predicate.
    """

    from opteryx.third_party.pyarrow_ops import ifilters

    columns = Columns(table)

    # If we have a tuple extract out the key, operator and value and do the evaluation
    if isinstance(predicate, tuple):

        # this is a function in the selection
        if len(predicate) == 3 and isinstance(predicate[2], dict):
            # The function has already been evaluated, so we can use the existing
            # results
            if predicate[0] in table.column_names:
                predicate = (
                    (predicate[0], TOKEN_TYPES.IDENTIFIER),
                    "=",
                    (True, TOKEN_TYPES.BOOLEAN),
                )
            # The function has not already been evaluated, so we need to do this.
            # The evaluation SHOULD be done as part of the evaluation node, but
            # presently it only evaluates in the SELECT clause.
            else:
                ## TODO: push this to the evaluation node
                from opteryx.engine.functions import FUNCTIONS
                import pyarrow

                function = predicate[2]

                arg_list = []
                # go through the arguments and build arrays of the values
                for arg in function["args"]:
                    if arg[1] == TOKEN_TYPES.IDENTIFIER:
                        # get the column from the dataset
                        mapped_column = columns.get_column_from_alias(arg[0], only_one=True)
                        arg_list.append(table[mapped_column].to_numpy())
                    else:
                        # it's a literal, just add it
                        arg_list.append(arg[0])

                if len(arg_list) == 0:
                    arg_list = [table.num_rows]

                calculated_values = FUNCTIONS[function["function"]](*arg_list)
                if isinstance(calculated_values, (pyarrow.lib.StringScalar)):
                    calculated_values = [[calculated_values.as_py()]]
                table = pyarrow.Table.append_column(
                    table, predicate[0], calculated_values
                )

                predicate = (
                    (predicate[0], TOKEN_TYPES.IDENTIFIER),
                    "=",
                    (True, TOKEN_TYPES.BOOLEAN),
                )

        if not isinstance(predicate[0], tuple):
            return _evaluate(predicate[0], table)

        # filters from pyarrow_ops only filters on a single predicate
        return ifilters(table, predicate)

    # If we have a list, we're going to recurse and call ourselves with the items in
    # the list
    if isinstance(predicate, list):
        # Are all of the entries tuples?
        # We AND them together
        mask = None
        if all([isinstance(p, tuple) for p in predicate]):
            # default to all selected
            mask = numpy.arange(table.num_rows, dtype=numpy.int8)
            for p in predicate:
                mask = numpy.intersect1d(mask, _evaluate(p, table))
            return mask  # type:ignore

        # Are all of the entries lists?
        # We OR them together
        if all([isinstance(p, list) for p in predicate]):
            # default to none selected
            mask = numpy.zeros(0, dtype=numpy.int8)
            for p in predicate:
                mask = numpy.union1d(mask, _evaluate(p, table))  # type:ignore
            return mask  # type:ignore

        # if we're here the structure of the filter is wrong
        raise InvalidSyntaxError("Unable to evaluate Filter")  # pragma: no cover

    raise InvalidSyntaxError("Unable to evaluate Filter")  # pragma: no cover


def _evaluate_subqueries(predicate):
    """
    Traverse the filters looking for where we have query execution plans, these
    are subqueries as part of IN and NOT IN conditions which we need to resolve
    in order to evaluate the predicate.
    """
    if (
        isinstance(predicate, tuple)
        and len(predicate) == 2
        and predicate[1] == TOKEN_TYPES.QUERY_PLAN
    ):
        import pyarrow

        table_result = pyarrow.concat_tables(predicate[0].execute())
        if len(table_result) == 0:
            SqlError("Subquery in WHERE clause - column not found")
        if len(table_result.columns) != 1:
            raise SqlError("Subquery in WHERE clause - returned more than one column")
        value_list = table_result.column(0).to_numpy()
        # performing IN with a set is much faster than numpy arrays
        value_list = set(value_list)
        return (value_list, TOKEN_TYPES.LIST)
    elif isinstance(predicate, tuple):
        return tuple([_evaluate_subqueries(p) for p in predicate])
    elif isinstance(predicate, list):
        return [_evaluate_subqueries(p) for p in predicate]
    return predicate


def _map_columns(predicate, columns):
    """
    This rewrites the filters to refer to the internal column names.
    """
    if isinstance(predicate, tuple):
        if len(predicate) > 1 and predicate[1] == TOKEN_TYPES.IDENTIFIER:
            identifier =  columns.get_column_from_alias(predicate[0])
            if len(identifier) == 1:
                return (identifier[0], TOKEN_TYPES.IDENTIFIER,)
            else:
                return predicate
        return tuple([_map_columns(p, columns) for p in predicate])
    elif isinstance(predicate, list):
        return [_map_columns(p, columns) for p in predicate]
    return predicate

class SelectionNode(BasePlanNode):
    def __init__(self, statistics: QueryStatistics, **config):
        self._filter = config.get("filter")

    def __repr__(self):
        return str(self._filter)

    @property
    def name(self):
        return "Selection"

    def execute(self, data_pages: Iterable) -> Iterable:

        if isinstance(data_pages, Table):
            data_pages = [data_pages]

        # we should always have a filter - but harm checking
        if self._filter is None:
            yield from data_pages

        else:
            # if any values in the filters are subqueries, we have to execute them
            # before we can continue.
            self._unfurled_filter = _evaluate_subqueries(self._filter)
            self._mapped_filter = None

            for page in data_pages:

                # what we want to do is rewrite the filters to refer to the column names
                # NOT rewrite the column names to match the filters
                if self._mapped_filter is None:
                    columns = Columns(page)
                    self._mapped_filter = _map_columns(self._unfurled_filter, columns)

                #print(page.column_names)
                #print(get_columns_from_aliases(page, ["s.id", "$satellites.gm"]))

                mask = _evaluate(self._mapped_filter, page)
                yield page.take(mask)
