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
Projection Node

This is a SQL Query Execution Plan Node.

This Node eliminates columns that are not needed in a Relation. This is also the Node
that performs column renames.
"""
from typing import Iterable
import pyarrow
from opteryx.engine.attribute_types import TOKEN_TYPES
from opteryx.engine.query_statistics import QueryStatistics
from opteryx.engine.planner.operations.base_plan_node import BasePlanNode
from opteryx.exceptions import SqlError
from opteryx.utils.columns import Columns


def replace_wildcards(arg):
    if arg[1] == TOKEN_TYPES.WILDCARD:
        return "*"
    return str(arg[0])


class ProjectionNode(BasePlanNode):
    def __init__(self, statistics: QueryStatistics, **config):
        """
        Attribute Projection, remove unwanted columns and performs column renames.
        """
        self._projection = {}

        projection = config.get("projection", {"*": "*"})
        # print("projection:", projection)
        for attribute in projection:
            if "aggregate" in attribute:
                self._projection[
                    f"{attribute['aggregate']}({','.join([replace_wildcards(a) for a in attribute['args']])})"
                ] = attribute["alias"]

            elif "function" in attribute:
                args = [
                    ((f"({','.join(a[0])})", None) if isinstance(a[0], list) else a)
                    for a in attribute["args"]
                ]
                self._projection[
                    f"{attribute['function']}({','.join([replace_wildcards(a) for a in args])})"
                ] = attribute["alias"]

            elif "identifier" in attribute:
                self._projection[attribute["identifier"]] = attribute["alias"]
            else:
                self._projection[attribute] = None

    def __repr__(self):
        return str(self._projection)

    @property
    def name(self):
        return "Projection"

    def execute(self, data_pages: Iterable) -> Iterable:

        from opteryx.utils import arrow

        if isinstance(data_pages, pyarrow.Table):
            data_pages = [data_pages]

        # if we have nothing to do, move along
        if self._projection == {"*": None}:
            # print(f"projector yielding *")
            yield from data_pages
            return

        # we can't do much with this until we have a chunk to read the metadata from
        columns = None

        for page in data_pages:

            # first time round we're going work out what we need from the metadata
            if columns is None:

                projection = []
                columns = Columns(page)
                for key in self._projection:
                    projection.append(columns.get_column_from_alias(key, only_one=True))

            page = page.select(projection)  # type:ignore


            # then we rename the attributes
            if any([v is not None for k, v in self._projection.items()]):  # type:ignore
                names = []
                existing_columns = page.column_names
                for k, v in self._projection.items():
                    if v and v not in existing_columns:
                        names.append(v)
                    elif k in existing_columns:
                        names.append(k)
                page = page.rename_columns(names)

            yield page
