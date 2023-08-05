"""
astronauts
----------

This is a sample dataset build into the engine, this simplifies a few things:

- We can write test scripts using this data, knowing that it will always be available. 
- We can write examples using this data, knowing the results will always match.

This data was obtained from:
https://www.kaggle.com/nasa/astronaut-yearbook

Licence @ 22-FEB-2022 when copied - CC0: Public Domain.

To access this dataset you can either run a query against dataset $astronats 

`SELECT * FROM $astronauts`

or you can instantiate a AstronautData() class and use it like a pyarrow Table.

"""

if __name__ == "__main__":
    import sys
    import os

    sys.path.insert(1, os.path.join(sys.path[0], "../.."))


class AstronautData:
    @staticmethod
    def get():
        import io
        import base64
        import pyarrow.parquet as pq

        # The table is saved parquet table, base85 encoded.
        return pq.read_table(
            io.BytesIO(
                base64.b85decode(
                    b"P(e~L6$BNybrs+`Oclxn6$BCh04TLD{a{=iHFW^$(rhCv(2B<B_?qmLD2aUv^ud+^;v5a0B7SsesT*A3Tv-Zxw@=&V{sUCKhEV1XECMG2CIUX~HyC3Mb}JR78q5U#P7Njkw|BA@y-k8kV&{ITi$BNzdvV%eI<P5!{Jz%)f4SAcYg-ra5tN$#HW*_GzpwZ5+F)M$+F&+tTP=nER@yL7>9x`Z^T9xYc6TWfz}7aC3%nwI2gX<d{=8Dt23>0HUj}1r!L~`8ZpSRZ7*o(ziZ+-E1ytlF3M{RZw-T7mg4V1ACWPQxOJpU`^4c1_lp7UU2}}k9T3#Q<Sb_&7#w29?9ly64#+U=Qlf;)>xZOT=X)d)&c%SQ)x)DHX{f$~9Fvb!tNk4(Pc<_L`S0MGadm)?g1ZD$!smne{tM>$2TA$G?HBVqN62D-K1>hEn`zwSomVo&Wl-?^=bG90cu?JFHu2k+Vf%$l#l(q!s0u%IFntHz!muv#l!PbUgj3K~<1$=LvbK732hA}3<`eUHP7*#-M%E9G;ZMjv!7*lvp|22UrVSrHZYtaNIguSgT7-I>oJZS<m;%#Z~FT@yAxG0oEU_yB9S1OAO3n(@3M_@`&dZi+kFvcEC?f+c$jhBHjw%|2ODV0*uBQPJh>oCR`;KITJz6%1k@?UOk+h4@Zl`9xy4%#EwR;h>|##n>)_IGJ(7-J3Guha-k1Xjwe@q{t9ptXAKJ&&NswwBqK8o@6$1U@`i3C36e?$?6ARG`z!DF?=wLc6O}LSQ!Nw$cY<OhNmL5SSC}eRmjR2};ojf%zbHS?3SNm_paKj5-#x4~i^xU^?7;b$qXbF-E}qbzqDo;76eJ+P?|Lm;lsdDdp9H`DoByRqDWPb{v=vt*vY7s2(_02j&E&W$>{7%g?&DC59Md4Wzae*VZ>MpUR!%Z(uH9<LNm9V{Cz&CjJIW*<gUFSZSZp+!mwXz+6!Dnc?2RbjV2Fz<f}pW~a9`FdYmQ^T1KKf!RRmmFnLHrsLqX+6JcLJ?DpDZ>Hh3folQ4YP9s)Xsxde%*S@6q7BUKGv04&7NfC5{0vNn-DhAnxbKp0gUWKw8JLUb_8Vx4_@73!+K2Scz(ge2rrt2d6fh_UwHrZ2jv1H=v_uMPiJBRhi+#>|%fNhK^Lu@qHT^OMXl05rFrQY;0&{^<({|u4m&JSAy6eD|THDkM%n4rY)az~QxZ9=IjI_XH;QE6x*5Ex$ff<Qf|1E`8Da06K@JeZmyFI}eQ?M3Gf%#M_mI7P(Gy4k61U6$BIE}2fim3N9>M%wX*!sX^V2mMH{<or52F92|rAv7MDy638ZmYrH*VNtnr8J8GDzf|=OvvTJ-}s{@-fu7)7W`Jae^JjXcEEUp*>G`huw8m@U^<Mk2a<k!qu`ob^9J+5-fg_t=KM=NZEfEY`BQH&9qGMN;nrYE7Ngr5Ob4$|u)MamZ>jSdQ_UC!u1qy}`3Imaqf~?1dT9!&E)cwMV=BTJTkxQ)fH1WLo0|ZYia)ND`j`rAy%tQrl#5|sEt+u#%m>x6!x&4T)ABn5<^nozuT5qdFdYih`!?D#U~AlVQU**3Mt^eFgV+0mT3fRo%!l6}1g+EigDF9MrMxDViXOjC(!%j$NX-s}O4I1=gZcac%@_qrtxdt@-}ceAl}5PRK9~zh_Y*uTL-b%SwEc-5Ov!tUVMX+`W<8pF6Fr!XbK9iWCVFrq>k|@xB6_@1;btMC2h~AB1iVGPM??>{PWxcu!UA4xYJN{2OvnJvR21nygg000oIaS3w<wf*t0#Rh9jGt0LL6D%t(4_pIv~in(_oAtKw#X#Y&@uPDM3r5JGJEwu7w{=<#$K<r)>xb4|{P3b3s`mcPx!ut!-wTgNfkZ=Rj@$PQA~yZn8fyU~Ag|q}d5z`la+fDq_d~N^o=Qu=hHci3M6cx9hBf*`Or=%miLi?_}DCU`qbt5KL#X{3#Vfa9b%zf!6pz31G8+V+f{0Ky&67vS@7~m=8;>7=>)B+xCZ}DSu!#Zy%Twe7&F0iTn3~xj=obwB2#F4}BQ(`oK&eW&smIrQGW;U?vizR*JJ6l5KA}ZIk8Fd!<<n2yUs#a^P}n505kc?!bIBTQ2Uvgq~Z=fvUL!(@|(uskj3Z;SS7(XUFx_Q^;@C*n!!g#F$E{=alAYVh82|Tb;7(z<f;2pO74w53civCE|BjhwcaNbznBIy}GKcL!AXN#u5T*sgwbQsV!dsb0WR(R~ll$eS$f8P-#A4OoB?q9ZxVJm=Dxy9Zyhd@Pu36tHzU82la7V42uf4=2=nW3FhS20fE;vZDb#N+odL$j-~ukZzq_FhsQg?d@N-rQ|kn?f$!}~cvv8KEDBz#=>+qE53Gbc!8wnB3BBhCm=h|}jeu9A4zB}OYK?&D@G9;|#q^uNUI|+<XlZ~mEBV!|cffQsJ76l%Ez02)7O&}7ATTGG(Ceg>L-o$kl2!-I=lxEcf!wubAWR8{TeBccMaC`BTMxpVJb2HydBhB_nSB?IK<JBdS8HV-#IMy#e1JX(Gcq;*1#-{)QV#XFf*?!?hM$5kA4@&2m!%+epw#bknSJ1XTU+RtbxK$W^TFrb+Cq{RLS0INZ(pa^$9d&-AxuQZBM`3EtO&wXV6*(W=E+h#f-oiMIBI={S|Z+z<E;0%q9Vu{V-575sR+V+1i<|0DTL`@q>uuS+LEC2>(flJB+ez6j&ql&rSLm7S1!SffUg(QOmPV&1f_SNa>V}(ScxT=5WHGTz<`zn6M@uY$$B_m$^L8OCc%UXxFkteg2{Nxqx}fx<FdHc<`GQiJ+M-<M=%@K<Pl8Cg<E4Pg6Z&+yp3QwBHFkfqP7{0U_Q-T#0(b4Z*hG+=xYRXv5hr?iMXm?OamsPX~s2RLKf?RyTNg53k<ggOa*V-$~Isk8mLoI!}Yoj0u7iB-t7$n4FQ6TsB(gi!$1-;rqs;HOp-JPLI@;q6h|UW9DWi&@Y~#?DoJakAs~yVSjBGSURua#LZS8>SepwiTjwZM6TsSI+8E(D#P&4CH)KS4&akyabh&U3E4%K~WTGJ7`Ll+u`vEY&?E}fyPsN?BXFe!~FQdu$!S_u)G%WKUOqI-{#Jwi<s17)J@9~b9pwtmCw;`JInR3e_0iWr<oLZ2Gxm&*#%^2RL42iTkY5^_v33avV=dOS<YdcW_iMCllG}C#(`4M<Rs!^4iXNgmV>;^slM{3bq-59@O&m>NmSQe3aru>^eUHRI2moX1j4>osEMl~Bn`6K+AK3o@Z#1d7G9#MDBX5|Rk=`BA3(IAn@^Tj!?XwY!SzTN%qp=)$-*IfxrtU<NC0?SUzU)DKb%VgUQ@N0<IoRv#{dWEk&`rU0amA!MgE|;PK@6WV*Bwt!JuQax*YF=IMWwH8e=+j_Zs2XGeo9F<~Xb=LNmFBJ!#W_6lUe4O|i9!S<X9<mF-VFpD407uQQBp!AFvGmA2ICdKznSH*hhkqDrV<axON>@|cH#L=wr**?>F1tV<}td7l<*l2Goe({7yF`X_QGZ6aL8dK4qq;Gm<geB>@8o~MFxfs{$$tObfTOg9Z<eX77JN8T+AaZ*KgHl5^3ALNcEAL1AscZ&)!8;4-0u%K!KnM{O_aen@5IAZK8~vP#wN5yCsj!rr~Q5p=@uQgF_8<JVf9>)A;b^_LVk2TInM<YA1JvQ2Rd7K!K_RxRf<pnBnQDUQtlaWpD=X4MgN<W5Y6GAucD;;lA)bwsDMI)S!HRNCQ<ENpp*M*()Edsu$$Jn(V}6YTW2@kz}9aAyesQ;@NJdX%7I-Ci{3?FUQAj5mAi}UK3C<>r@B6s~Y%TVF5D81NgnVR0(S#S^j<jJLy)oR<ha9p$L0HdR3hXoT?`eBKY*SqFIQ$6@3tmubTWev>s4CvRK_BOjN)*y|CsjjjNz)h5L6#rJ$N51NGjDUv(*z+|3;9(mjIRfm;>eps3-<t`IbsKBq(92t7@!x`OBw#{!(YDxuRXn`JNLm+j9Pq{<+zMng57%50b)A$aChq-m1_pY@RxmQEm)Qszv~4P=o4OGYmeiz<l};<1}yF}2wjihRR;E%8eLU3L!2nIr9nXlmsem@tqnZoKhyqLIUh3!QGCR=La#DcRj#rQr+piqKM$IZ_rI4do-`lmyw=wBsPHxxNTU9aZ~y^&Y4vRrK%lT3Cvr4}iR8_?Zw$4fsjvpLAcSR=E8r+FBeYUc(}fr@6orne)8aZ_quav9Uvruo)xR1Zcwv=q8OYNP6xoYphfvf$-y$W4w@@WawkGUVJvDM#cQ(SWeNzXqX^P_Y4Et#d<(fg@7cpnOD73dML7K5d_9Dvth{jFC18$NHKi_Sb=I*0LS#m$pfCr?RS3A1E6mk`xBo;p|I|xPdaeyQ+gQ7%{%6nq@mEk8Q4&|S&S!sHt7Tb9Qs*E8wDA`K!R)Hn^<TwgHw8rFH7vn;}u6e@>_x0gtCfh>6CRX`(3K53tWuKO+|Ihq;Xc~)=Z0U3Ajv`uWf%ckcl<D6utmF=ZQM+FOVul`{GjbT#-de`T}zeQs`a9tJ#)aM$t$cV>MwcLS);8*?p#>!pc4LM-|ldio>x)uM|!waR710Pp5}CL?+`G=XyvctCVD;@B{<>KgHcSS_m)aHSYP@#0brFsH|=RvWE++2h6?f@ze}z^h1OF=DbG7Z(+UQ&&~ph9MQ$_5z!}_)xhz!q);MLx|$;7weX+<Uya6MQBjQizeK{G%e%~i<dSBd0el*4;*u1CpJV0J?xq-uhPp&2po)WO(njgJha@oed*-29EG3~I6R>bd?gNby2+?>5eFjv6ChRHjG+ARsE6>}MTB#0N0TlohyapA}1}qiI1r-Dp1{DSzHUKCOS$1!3Ze<`uE+9i;XKZB{6hUlZZXiM~AX8{%aA9&}AWCvBAOHXWD77#BV4eW+3;+WF007Db0SQ|G0tgsDpn!n`2ofk*z@UMH2M{7im_VU|g$o!mXxPA^gNF|wLWmeaqJ)VPC{n0c!J>tW7cgSTm_eh4jT<;}=-9!dhmRjXf(RKxq==CtNRlX7!la3lCs3kDnL?$Cl`B}XXxYN0i<d88!iX6|ri__0Xws-z!={a!H*n&}nM0?JojZ8)=-I=kkDot)0tp&KsF0yUh!QDU#Hf*@N01^(nnbCRrAwGHY1+i8lc!IhLWvqhs+6fys8Xp~#j2I7SFmEqnnkOYty{Qq>DtAsm#<&If(aW&teCN5$dV~r#;lpMXV9Wan?|jgwQJb2Y1_uFo40S^!igJ4uAI4Z=+dcM$F7~bcktrLn@6vny?glb>D$MzpTB<q0}32Su%N+%2oow?$grWqhY%x5oJg^v#fum-YTU@NqsNaRLy8<pvZTqAC{wCj$+D%(moQ_>oJq5$&6_xL>fFh*r_Y~2g9;r=w5ZXeNRujE%CxD|r%<Cxol3Q;)vH*uYTe4UtJkk!!-^eC761SMCfGt86$}|Q1ONsZ7z9pXZDkb<7Rm({lzkS^LMDnkCI}oh04NVxc5iNOWgtW@AVXniY-Jb}L2O}eAVMx6Q)p#yVRB?3N^&kB02wS51Qi4o0ss{N6$BLm0000L1Qoyn6|MnH6(|)15&!@wwJ-f3pmhQOWC8#H0000`pFjW%te(6qpEy7SsGek>@SY%_=$^#5FrOHlp0u7o698Z!$PA1IvVeTSz+hl7Fc=sN1et*>AYU*LWClh9SymFX;0P4}6`%wav;-^_$^{h!6$TXs92f`y00000WS>A72mk;8005kxKo&MA2mk;8003m4Ko|%B00000oSr}c001bpFa2N;0D%YqH~;_u1N|NW1O6NV1O5;J1O6TX2fp{;76Ak9H~|O#-}@W^1AHU_1O6BR2mZh2CIJQh{xksv{_Y|H1yvx3AxIgf9ApwGY6W!I7-yB{&PqqH*T51mv<D-C(7*uY3jvH_7AaA{6<cI+B-u=JVU#EidJB|6o_ft3sM-?8Kr^5_ZB4{xdlH>d)@-p!7G5+##O7Ly1ObTPDzFj7PI*BfW=t#)!dbv!EG+U=VT?cq*E1=U1_6Zc#P(naq9IWXn9smQT8jmqMWQhcIYx|w@EI6|D5k;HOkr;+0puKQu-H<BO@<~HTPwkKN;40##v%#?Dc4juBEkkDd%+|aM}y`-6{C5{00000CYVbc6$%+O1ONsZ7z9~mVR97=7Rm({fCv_X2PWi2CYD4T7zh9W0001FpFkK0000000Gysc7B(md000000A!y)7zh9W0001-o<IN@EENP51Qh}R6#x|k6#@VN02KrkzycMT0ZbJr6$BCh04TLD{UD$v0s!y;0000005d=UBq#_NE-^AD05l>jARH7hD)2uLKobC9Ajk}40r@~?APdL`G6PvaK9Cv60`h^(Ko*b>WVVu`1xFPC6`%wav;-^_$^{h!6$TXs92f`y0000005m`t2mk;80002+KNdD92mk;80000qKo|%B000000PsHm001bpFa2N;0D%YqH~;_u1N|NW1O6NV1O5;J1O6TX2fp{;76Ak9H~|O#-}@W^1AHU_1O6BR2mZh2CIJQh{xksv{_Y|H1yvx3AxIgf9ApwGY6W!I7-yB{&PqqH*T51mv<D-C(7*uY3jvH_7AaA{6<cI+B-u=JVU#EidJB|6o_ft3sM-?8Kr^5_ZB4{xdlH>d)@-p!7G5+##O7Ly1ObTPDzFj7PI*BfW=t#)!dbv!EG+U=VT?cq*E1=U1_6ZcjP_tiq9IWXn9smQT8jmqMWQhcIYx|w@EI6|D5k;HOkr;+0puKQu-H<BO@<~HTPwkKN;40##v%#?Dc4juBEkkDd%+|aM}y`-6{C5{00000CdgA96$%+O1ONsZ7zIaiZ*_1L3>L}-7JvvA?gl25PA1w+92f`y0000005m`t2mk;80002+KNdD92mk;80000qKo|%B000000PsHm87vh96$BLm02Kfg1Qh}R000#P6<!r^Oce+f1QGxMD77#BATN0V00sa606}APX?A4?0000|WprtBWn>5d002Z~V`X7;Wn>Bf002#4ZeeF-ZDnqB6#x~;0TtQ-EEUQH6$BLq6$TtO04N7iWprtBWn>rzL1T1jc4Ytn04TLD{UBr^0{{a6007Db0RkmdRV5`+Q$`g>7G)*9T;-IMWi_Q;RToufVFesKURQNlSCw8A0X0@tR}`An^ifc4MO~Gh6%$)lR#RP7MP6oE6=hX<TE=Brm7S$mMPYSTR7jFkg=_#+6#yp0SR54$88rj|1{oLzQ*>c;b#oOA7Rm({lmiyH116YOCX7`aHUKCGQe|{$a%E%~20>$VX?A4*87vh96$BLm02Kfg1Qh}R000#P6(kilOcewb1QGxMD77#BAQF)P00aO408L?RWd;BM07hkPVQgg;02P7(6_f!i70Lw_1QiAq1{^j3C<IMmY-Jb*MrCbbY-Iod04TLD{UAXJ0ssR5007Db0RbWa0|hbw0|gQQ4H*Mq2m}Nm00RLW01JVFXb2G`00%<>ln?*|6DR-&83G^{00k8w5C9305DEY$j$9lS3>h^900tQt21jLXWMy&{3>L}-7LEcIvH~WqS|;3C95w(b1WjRVWf%rVWo=<>WdIp06$BLo6#@Vi02Krk0ssI26$BOb9~J%!Ocka96$BCh04TLD{b2hBtrq~6Bxoi8lbZv;5JHMwaSMx*xUO@qf&;Me1o?X{Q~A^`)q!_``6dBQ0a^fF0AK*RI$e2Cmqq_AQe)VnQ@#8bP-upVa+Cj&x0Y$t{GY(S<OAbs?(OA2#gqRl$(C|klWyj}rIq2Lc7iLDoMqPOT>ei6TDhyqBc;Y~x3Scs|C35`%&o@%NR;Ln@`F*6Y*E}U|0PZEe?ggAZ!!NT9kMk44I)|@b~>Qy!G3@yTA6aqX_QYUNRA;;Dh+}8A5cBmOzorujPXA*kPvK3t+d+8WcN1ii1FV7p)0FxSvToG{zo>jBd2lvw=}h|tIhw3K|98H3uA|JnE#S$>bQ1{Crv)t_(?oTxd01?Fy{Y3TdN)a4_4c1oFRewqLLhQlUD8VU*O4x>Mgi!F^_yw`R&wcN5M;0K$r=>6(xt6+x!o!ZCN*xd>l6a3)(;<<&K&E0RI=>Vo{g5%>RQ&VrphmixQIbKwI1$KN89(D@sDG44dJCn|!h(m~rMmC7)yqqAe<J{4Y>$F5yMS7F=kK;nK*7{s$yP!7qT1sG&I{H6xNFDHMh=AVOl0V|N1)loV8uK~<(HNMSgGJF!#Z(`hSgq1>N{E(OWbG^wyTNcnUl9;!hK1GHw>MaY6W9Fufra+b0+FnSiRqJVRX$hM_rrO8*x#s=yw_y@SF{U8Y5pa57B^BxDNr*dXj2be$YWrV*$ux_HwWHa-*li?#YFiTcyyu7c^m?OTp4*o210G({=S_TO_B+6wYII}jLM)~TfE}OdTHFHk{ljd^-!X^vE4W?V9Xof<*@F7%?#I?%@wRB2aad<X{Pose^;rtIUn#9s=ej;rH$z{wgEyp0jxf#El0fug7kzAYR*Dy;1Vt4pN=Ttxdpk5tARQ^<f67ijIZ=%)I64zF$6jSkmH!^0ypjQ4tnD@FPF**8$ETKC|!upQW(?N+$@O@E~>E8zFgz+Iv9?sEhe7r<dQ>jz|6#x~$1r^i<EEUQH6$BLq6$TtOEGP$BZ*OdGXL%S3L1SZYb#8QNZf5`h04TLD{a|1K0Sf>$0000y0Ry%~0R`OqECB<)Bmo2T76AkPAOQpZDgg!l-yQ)2{u%)T{wM(h-Vy-={x|^x{ty8NRe*qCKp+$h2Sh@FFf15^1_9uBG!TsiBqDJvCJhIrP>D1whDC$WKvXUSj6;!G5HOL7qp@fZG>c8-!69Hei$w(EKsXQ%j^_iaghYsug9KP08U#YgbQ)n04hM?hAf!}*6{{gY2o@nh!GUQ-A_T-@A#g+t76Jm1SX5k%L7`E3IbaQkAm$>39E}aa;aFfsvc_!Wpp9CtMI+)sSRyss22;5S3JV0Tfk7a0x`hL^TZDL{5uztZU;qf;4;U0W5D1!sAV44*1cw7bvmg?J;b=qLISdPjqiAdpHb)E6wIC#wn@tFya4ZK4rlu(gITnjhLl7cV76fO2Kp;d22mu0tAS^a6#H-?n5DcLw0<l>*P_YVufPyw6QA7hFT~q)j?r$6w3>h^900tQt6IE_xWpZb7VPth-bY)*nVQO!36$}>21s1X<7S0kTz-cC+T^u$nC<j_^Z)|U8c^C>oV`Fc1ZggpGX8;*26$BLo6#@Vi02Krk0ssI26$BONOBLuAOckC26$BCh04TLD{b2MFRV@JK^Ohrk>{bUNR#vfmm~LItaZ4F(S+VE^v!kkqi@9poAOLUzfE0!Ri~x@SSH7NM7$uKpVkhbuVYJ%jzktp9+O6W~L;A1KaCU?h%XepIlh)`nOaC3@+hB@qM13uxb|c@z|A0y3ef8QnV`h=q+MdyBF8@Uq#;d(a>$Rl+1{TKqvc~SSVXLD&ok;&d*NnA$#%q?i;X7GcoAlqo!e}?l#Pvy9{Xf_)Drw974+!iswt73G_k_a^(&)l&tJhxCYc*@qu-k6;yz2j`1*2kz!TQ>E4%<HA{Qsah+axvppO_eI9j5p{3p-e1`63UkFxve0_}?&Tyjs0>(y;4znSIg}GWjSOZS~riHTJ^tF@PF)zJ@se7ydJ_1G%%azTSK`9D<k+gCSS@YNw38u&WogEd3{uzyi;QMytLTb}=@g(!K?@qov)7VZ8djdMnVtR^RRUr0M@cSM5Tr-ij}FMH%xSWy|QK_<1$#Agp|`_I)=0EB-57P!<jYTSh??G(cIUJ)r-hf~L{sKf(pa2A@z?b`HxoYu`!ppJuD{zDjvs&3_Tdy3EF|*o6p2WY~dDv@d5Ltj=J}UhS9v9R*QRQxY2#Z#PyAcE$4Du)FV8Y(-Fr!it)Vk=m=)HuIlam>6vrm6?SV6c)l*8#`H=-P&-zm;VUX7B~+`v4{%@LxEzLAAqjfeYJ0_VW+~bXDpepOfh!rEB%jvaZ-`!s+yGVLi`_vK+P)sAK0+ds~6?iAjSVXKvE1y64<S5_03rO_RjxN)>b@~RM=_I27z#>!99`@5fPCjNeaUnAp{9Tfh6|U0}@EWL<+Jb$sl7yW`rh5(r(RQx{RjKn#Po4iK9dr&ET81XyW^(RzL^GXd6{=p~3D&s$eBP_mF~VWsdd;!{<uK1Z)N+oXP1nMv61#;L>*Qwa`|ktpyBApLH#eAw364&C0={JzXbOs|;>*i(BO0#qx=e2f0mix%1#55@HBHy&DIL!k@YZ8z!2_cW-1sgMgoz(fc*p#>w;zr6tZ<a7(novM?Zd420(=Q^Xrc$Kvf0&xYhfDvc3n8jH3gW$@@s`jft|M`p`XNRx;ug6FCllrC6m4!8)R2k|Y`Jf;wQN@V^hj+a8?0b)Zepnjde;*tDQV}E%U>=+-R0U-mvAvEtTN$1}=v3Ftlihx{z*yw>a^lds5VIp{!W`#Fp(T7)7-@^RsZNs$oaV&W60?i6<PNsbS_HGnOl}TisoA>FnsFN0p*SLE9#3)tTzE5U`YzyLI67_(b05sU7K=n34#k$o_+yR?kP-P$u9buLLAwDu@sX;MTYdC_}pm4}<zU8hU2~0xVG&HZ#7t7$?Tr}eSxCWc^)X5yi8F}7J^O2pq7l9pQ7YBiPql%~`ZfIVmCR5{_8c+wK?h?UMc9jd9_9YAsktSWDUf;rh1uHeyG;Sa!U_n=Li=KjxUwV4yApx)&?SP=+oG)RVVT<*u#)aq+=PYPLwn7_@(&;mz#1#hqlIgfwKbDCS#RcNL+oGZS5UPCr?SL%f37N@QND|=)HmhEer>awYP}Q^j0pcQAMs-|2NE@&5od|>e>RqO?Gd{H1q6|)ywhUg6wH{@>wzmJ&1bpiYh*`)+S_7EfvZmQ3U;`a#Y`(gFqNH-g#JT!7;u(@sR$X+9nj@fr==V&BZ+<!nhXB5TzDrlX3bX$gR+zz$G{}GiM;25}q7Wy=3<t`-5+q4&V>eQvXY+Zm71&KJ%>P2ds{Lc}W~E%QG@?pSJO~#G0Sz0fMgVzGutAg`s4p3cbxAY|vU&AKq~jtid>m9Zz02f4ptqhjoE2qcW__bD@DVG#gy{9)toXlEfB`{HOd-G^{5t(s_EW3PX292i#XU6;RTTgg-USu%1uPZH1r-Dp1{DSzHg+f~R%LW$a%pa1a(N(4Wn^h%X>MgZAW(H;Y-wX4L1b-dZfSFLa$$67Z*CYUL1l7pZeewFX=7n*ASNI|b98cVZeewFX=7n*AVqFxX>Mg@a%pa70000ewJ-f(Zvc4<0672v04M<i&J+O+_UHTke_R{^1O6HT2WqUh6afeRp1nE&3I6VW`xXHM{ty8b{`YOaJ$v`=`Hm0)0|E$5009C61O)~M2m%HP1_}ZT3=Itq4-f_s5)%{x6&42<5e)?l1Pu}x4F?$-6B`^I0tXEQ7aj*6ARz)G5e*{(Bqb&%2?i(z1}Q2LD=Zc*E-wiT1TX>zF$Xd;Gzm2}H#i45ItK?44LbxCJUs>i3_d?V1qMMv2O2{SL>dT12}Vaq2LeeIN=r-v0ucul4NV75Pf!8}3=INNQb!jN2NhFPRaOUASXod42S-{5Mq6B6USD8gVgh4iWoBmvXeDWC1|Mq&Y-epo25tutB}NqtZvriF4Ms+Ba&rhGbae*`c6WGZ6%i!{4QB@td3qvy00{{PEe$<<eST*W2NeQQ0uz6Lff0fcg9Z&25rl<YEry4PiHZgr2LcCOixZ3jja&_m3KIYT00000CV-Fu92E>1H3R?#85j;na$#h3VRU6*O<`(pauo~~$^{n0Qx@1BCbEbDCa7^7Hg+f~R%LW$a%pa1a(N(4Wn^h%X>MgZAW(H;Y-wX4L1b-dZfSFLa$$67Z*CYUL1l7pZeewFX=7n*ASNI|b98cVZeewFX=7n*AVqFxX>Mg@a%pa702wS51Qi4o0ss{N6$BLm0000L1QnhG6_f%@6&Mu+5&!@wwJ-f3&kY0sQpgz_U~Mx7M1V|=MTlB#3e<)AmtH~8C2}sRu-K*RHko1&Hre=>b(>5vXb&0xve=~KEKt+iJqL0yA?Y^&Fx5SB5C5RBsPq^MtXot>pnW2z_ywBRB$s{#H9f^P!A$&wh5D=~{YnS`LNmalgA>T@s^m@v1VkQyuQRhb1{DAmx&jr<0xT8E1r-Dp1{DSzHmm|D3|47lWgtOhZE130Y#0$ja%pE_WNBq`AV+0xWpZI`0000ewJ-f3o#_MsF8}}l2fQs28Ua!MJpKmTe$Tm1xI4MGI@WS_IDZG@3aH=FW~ssM5SLu~eF1V><@xdiH2@GYK_DUm001x`A_4;fAOZkEAV5+kApimZA_4*c1_UD@00JTa0wD(=0uTWp0D=hw0ssIY0w5v;ARr(h0HPp5VgLjp01^Te00#mBA|e1K2Lb>pZ~}m0P(%v=ARq#90wP2p04A!K0UQ+!88rj|1{oL)O=)atbYXINUs7RiYZVL@$^{ne1{U-MChC*{Cbp6R95$>1C=6C<V`U&gWNm43VQd%?LUL(mVPt7#av(=#Ze?;|YycT76$BLo6#@Vi02Krk0ssI26$BN81r@#mOcfjz1QGxMD77#BU_t<`1OQ|O5dZ)HRZ}2Aa&37aC{kr~X>w&`DHdsRAVzO;V`UjlVRC71WgtUua&U7IPGNQ*Qe|^xa&~152Toyjc^D5vZ((zEAV+m!a%2%sVRm6`6$f%{c^eu4TiAdr30yFNd^{z5TmZ&BLQxnj4SS@@){hqg37GK#E<<Mq%eWXAY%5~{u_qV@h5%|O7`Nx<Fq=&k02ROj719DM70Lw_1QiAq1{^k|0w@txQy@-Zc6lHuQe|{$a%E&G7z|ZYAVFzzAVzO;V`TsU04TLD{UD$L1pqDp000NPEfFdKPdxqx`+v{5PWU^yw>s8xb~t|r;|i$X(PpW^?huz;`h5X%TIKoj1UC>NLuEBnQxOp*VPiKKVIetE5+fEi76zjcI}tE5H&78Z5ff7}Ks6B)JS8y`Q59hkQxGF66<9G7F*Cz3F)=YBGcaQl5gB6<AR|)}6&)5cGZ8Zp6BIMC1`-BhX2S(BHN%AiW@a%0001VOpaC2e3>h^900tQt4^3%oX>?(7d0#?uVQyn+6$}>21s2!{7NiCy)|>$*_?ZD5HlzY55mi$lPGNR=AShC0bZK&BWGNU7RZ}2AX>uS&Z*pU002wS51Qi4o0ss{N6$BLm0000L1Qmb*6;4bQ5ETRx001bpFa01u^#A~%0ssL31ONj71po#B2LJ#70000022cV3V~}_Z0TlohpaK=L0xT8E1r-Dp1{DSz7zhUd00000000;W0000000000762#+2LJ#7000007zh9W000000000004TLD{UDHm1ONj7007Db0RvkIgh2ryAR{I$1Ue1E8Yyw0a1x0uNt7%&p#@tf2+EXYTA&n30tO4l#K1-%0D>tc1V~(hA_atOZK7lmRz?BRqzW`h!60b~l0qQHA=)}XixMOlh9OKcD-!}x0frPnk}a5q0THO?S+WE}He!R8C=dW`fhtiL5fErMMF9*<gn&h33;-sKrU4uk1Q|6100tQt4O4JoV`X1PY-wj`baNF97Rm({z62JY1SZ;|0VeLD0UQ_z2LJ#7000007zh9W00000000&MC<q4t00000000;W000000000002wS51Qi4o0ss{N6$BLm0000L1Qp;R75E5D6`TYW1QGxMD77#BU~mVO5dbz{c}bAkO*+hRRpFe0ThS)W(5LW9tAiH^+l>6|1Wb+XhmhLcu-1ZpY=H0WNp44lkFgP%`4cguCA~JNj_nmwi+rN4A4(IlrA#tr0Am1V05O(Wr9SH=6AMYZmkvgP_N<T+&K<nq=_aRtmIV!Q>q*|7D64-cg&QiS7njVN#uD8qm)*EYX`vX9u?}NM+mt9XA!mr)zB(8r13NvzcJ<nbgBYo_TBr*4;}fvWvoG2tOXCuJRh7!9dZd$5FADg~FC0VN9=EjlSy#T*J%_@)TKsJpdpkZ&QJoINM;+C?TJi+a=i?DftgUhy=q+Zl1!wzXl?+IK^ar{f+piN$q86#?A&>YFSGAUw@mf>yDL%JR5^+sqiw*JITHqZ0^`1F)Vm+mJIR3nz4eKWc+=M|KX;(DZAc}J{=mrKVb!=R?;!Ok#*~xdLhLh#+Fpd$bhGNW8tFXX#?Goc^TEXBDZ8RQ6g+Mr-FZw_o!(r~z#c?=7_zoupySuxr)j{QxN}zO6X-pvj3hd77beWEbX@qpp0KNpBDvcPdO`KwIe63CS*IuSsRnws~59fzEtO4>eUDm3(mWu5QDs&!E`l^U?3x;=Q!cmDFs=jy7ZH<{tbGT5GP2J2KkOP4Ys39=^;m-jPB-B0(#)-|PwoC=xoc?OrID`x%F}97MD4-i&iIWP}lH12slur&-y(RK6vteRIV)eBWwg`D&Vx$15niuG*6#x~y1{Kf-EEUQH6$BLq6$Ts_2of>?0000002l}W000000000M04N9&G5`Po0000O2mk;80000000000D77#BV4eW+3;+WF007Db0SQ|G0tgsDpn!n`2ofk*z@UMH2M{7im_VU|g#ZyQV920h1BVVCK7a@zVg!j20Zg1gkwQg;6)ajrh~VM{j2JRz(5PYK295|hbVS&}qsNIDK7IfRB4h}WB1VoNNup#4lO|4{K#3w{3Y98Wt}qFJB|;W0AhvYi5}}KiFJQum8504=2{L82m^p(cjhY#2B9LLz#?2cz5#q=>GlxzcJ9qHp(X;0apFV#61OOCB&>%vE3>`w0D1xFzWEeGa^e93ANRcE>qEyM!B}|z#ZQ|6)6NyitRD=>Wic~36N+O&>6(N<XRjgXMdIc+%tXZ@q)rw&2)(Kp>bamOqt5*^$5q$kB0W6rX8^eedTV?E61Z0JhDI2hiS+gp6oT*So;~BIW(WHsVG>uv{YY(nri;zv5uWj7AsVLzni?=i1z}X5XF2Xo+<$Rgra4rJ6bn4cfBEYWQCwF$<!HXwvUIcn>>P4_8Dp!Pi`0^3a_hBEuexm&S0~nB*z=0767BqMeVM2uqBRFE%5C8xGCeXM692Eo^H3R?#85j~%aA9L*Uq)<cXJ~X^NN;s=a}^90$^{m_DHiGwCV;U4Cg!IB92f`^G5`Po0000O2mk;80000002Tl!2of>?0000002l}W000000000087vh96$BLm02Kfg1Qh}R000#P6|eynTuc=f6$BCh04TLD{UBH^0RYef00aOA0096400#gG00jUD015yA0000000~e60Aq|X#u(%k02TTI6`let70Lw_1QiAq1{@d&3IG5A000007zh9W00000000&MC<qDw00000000;W00000000000000ewJ-f3y)^^?(u*J>kSS>m|9^a{D&hb{V=hmTs+?s@&+;;ast_W{KBo3WcJBuzC<w}-a$s*maCv76BVp%a#N4n$=^<%J^Km@o=A__)&}*a&VzG5nG)OZx?B4YzwZg026Ke+ANCMo@42)=hD8pK<7KxycH<{Ma#gS9%BV|%r(!zlRD$Y3p0RSe<z5yH+1Q|6100tQt3sZ1mV`X1gVQg!26$}>21s2E!7MKJkuDbyyw7LNt7zhdg00000000;W0000000000762#+3IG5A000007zh9W000000000PEENP51Qh}R6#x|k6#@VN02Krkzy=k(0!$TX6$BCh04TLD{a~N~r33)<1ONa40000gKma`;Kqx~d02DeTfI@&r02}}}Fh4jmLKyHrfJQVx07XbPKsh@sE<WHt2u(mTB7jA}P)Yzn01!2RM1V*@06arS05M5GG9cjR83)TE<6yasHblk)2g_}=A^8r>Y_u%$WtJshW?Ax0+_1v}Gs}`Mvn=^$Jn+B<4wfZfW?AxOc1D{_9P0=b02QtT74ict70Lw_1QiAq1{@d&000000KiZ{7zh9W000000Du+%C<p)m0002MP(T<6000000001h0000ewJ-f(7XW<+0M^hrGC*(B0mB4t7x2{3iB%2?{g(p{w%An@02u9mC$o+i&JWclVGVYdVN#Z#c1gniMPbV+04V?~0GroY9Z?JyjdkFwA?k(&zrOt>y?#r&ieP<j4xQeMA;6b~1;&)j1PB7Y<~OzaAKPoa=6HUqFXXrKAo!qCr;|bb56Y);{lh(C1Yi0U6s+Hw#RS$*PN5bo=`DEun9xz`9M<b&ekT|$A=1YU1bH6fgK!u1L*5|?!wZ?P;|(n}mC-L%Mz?ePhs;PbT{Rtvvx^3v9As4K)XHmp<QF4~6P<l|n4%5>0GJ{G*-M=PCh*4r92E)~H3R?#85j{$aA9L*UsqvlYja;nZ*_8W6$}>21s0AB7S0DI{=xw!qQC(h7zh9W0002MP(T<6000000001h762#+000000KiZ{7zh9W000000Du4)EENP51Qh}R6#x|k6#@VN02Krk%2E}+6-*WG0~G`k001bpFa2Pp6Rj!$2Jwg`;1*Q}n3D{5sQboXn*yYJ!vnud(xj9`R4+2q)b`&fJ4RK24UhnR0DAym^Tm$59Nm}XOX~I-&t&E8bYJdmx%trk*mP+GFD_K@XQ9t0B=QhNQNW&gK%S6JMHEE=GaiOcI2{hqM25|7(`Nc&An}xdIG>V-4C8K!f#cB#G5LfdGE8opHq%I_1JwC^I35uhM$!Hlh9SiSB{XH&vYy*CX`(1n3@9U=lh6i<M<T=K-=@tJMUfQ0)T{h2*%bU$x);2*9P8X)MYO+*Tuix3Q%1O7tSZ{yg`0wCZ;Yj6qw^6O$zUZUoegUUu_^rzR>tUHM;yYvMf;N^+8?{X^%gJ4F!Enhs?M13_`GMP!TF$oRQ9<`aITHaZ<1S`Z_}ia67J(`UJwTqMG?R{$5U1w2A0>R%>>;SbN6c|&9-2>xk|1^UUOCMO8eHVyqBD|Z1U3$@HOp^T`Ul~_%20veeP^F#j+Wu87AJstIO+inSXA|23K5#+onk)r&LfiyRd>xis}P%MY-nU>t1^+(M>2p*2f(73;kGiWGEvh8zUWzD2f82daDCcp={G;Vh!%CZd>2Xx~%Z5HMZK-FaN1~Q2*6l#jV?)I;BEX$6V`F=Jbv+l&!McG-)h*<vsgZ9ScNO$gD~2c2;^nStUQ#W`zplCH7nDUu(x!sBzDpPSyHayOrAju0HoR*G2ndn71Tr)D3~Ns3A#fh(wZ-Bw5yR1xYCe<$4hy6h)HEFsejE+9a(3g`fc7ks$-M%(3Hw59Qe8*}zW;Gz4BFheko9*^QM|e#Ii}w(v~Y7h?SGj(mtI!(rE$C=nf9t}2+q2l@}13yyJfOneZstUGoY`_?im!{KLzX&EL>kS$zulv651?sAbH;xAeNp~lk#Ducm57AR1@PqW(uI-%jaY~wF%-j5`BIGGR9a(<8-7@!4+`OB6Ur7KCH)15I}#1B->p=_l^uLr~w`_o6!wyFHnHWcK`eX8`~337$Ry<JQ;1>$|sxYr-gW+=dkLKXORK!bJJwu%=735IOe6&h$yXf`VZ6rB#pubK!!<ke`x$lc4AipV{u$H_@j;sIi*SX+oGFYc^Ji9-Hf{>LcKPH57>aQ-i{p%q_dpl_Q2q6Wf03&TfTroK9jFD2E<$NTadf#HUG-H0B`(LC-DKdaD7)jW={<I;@t*`mK#eDT2^b_tQ{zf$7;g*^Ra?LDoJu?R$zGn-P)V1*@gCRXCGosL$?!b=V(hWWB9z8S9M@>j@s_akr^NgGCD#1olCPH!3_Z3F-bU@WqZY-PruXe}=YW0diq9q;tXgwJREr<UfV7K|~=7zq7EMSOzlovsW9yq2&&S8x5|18R4PrZoBfOlXTK<*3?k>T%qvr8OC!=@Fm;r<sLD6vuf{*GaLSOyZwNhp<Cp6u9(I_l&`zH-q`OR&KX^tN%O$j^l>Gwio1P%KEmmWl=XM4azIq&adUIi*Rr{)%Iz4B{CEzjU1&`#^hfsk%>9U4%tZ}@A>`T+a=Mnn8-{Yxte5xJl~cY1ZM1evj6CI=$K}-xJ04auWQ(=mf|He;Uz`@FyY)D=7-8{>ZlKEeatVe0GMacXnZp72Otx=3o|~1_T#vNRoO2gJnTtXMH1qd(FE;WU(<x7fFq%K$uLM7-)Q4+DWufnoF?gR7X!Lt=$m~AO1&vEunPuMa%56F6kLy#<xV_$@j!b$0}axPz*)GlLA>Qeh#iV;g9Olnxv;u|h#XAoVx@;kD*7LDsXi>J0u=xi$`2LZ4=feR4HX0x1{DSzHUKCCZeea12tjafY;12JF#rGnD77#BVC4cS9{_Iv004i|wN7<q+BNF!*0tx3Psi@a;Fx~8X?we_vuk$Kc|kM{Uu{aIou{iiV=u2R+j|^y?QzQEoo?N!?ry~E(pg<@d#jrxT5ExQXP0tnc@;M8*2?9cpD|iCZQVFsb(`+pxhARiwsY#Mov!A_7XttQ0Ll#m2!8+p0s{mE1_uZU3JVMk4i69!5)%{^78e)*85$cL2ps?(3IHD<AtECrB_<~XC@Cr{EG;fC0wORmGBYDI1T{7{I5|2yJUu=?KtU`*LqtVJ6hRp*CI?4INlHshO-?#bPzF%~8&XqLRaO{RSXnzGS`Z=;TU=c!Q(gr<Utl64VPaz%WMvX&XEbPO3{z@rY;A6DaB*uT3q=ibb0TyYUoCZZ1{`-7czHb>cX}f{WP5ylb4MS3e}I94g9?O&FouVOh>3~^i%)1+jE#<ukdcaAl9N<@l$DlX5*tNSCSfc@l`VCbJ5VMk7fzTK7n1^+nj&tEPg_BoH4|~1opB-$nnYxOo>rfrp)ye~9iXD4q#`+`rUE3Rr#cU)PCqfJidYPLkddlqO>3wdCnBp=8XR}56B&gta;-9~u6eJOBCs^Em_M?!Z<s1p6A~mGv|nYAk+q{4JhnV(CrGz{j<|X|jSq=>YePsMX|_tWxdO4Vx0Xtvx;zG7l)H&&uMjh;VZ1+13kMA%y$wjUFC@O3E*QU13k)iKz#Aken0&!4DmYscGI1O!e0_4Qs={NeqN8zEVZ+3RkdZ;f#>bXQbgh^-a$|WLwn&cyL`+AiM6k$oRjQ&aw#iBm5;BmHB6GS&b-KzTnu$&^rlnm*2^6$Y1eJgh%TFZ)HOwK+o4(Ex6A@t+&zHDa6E$UZ(7=yPLl`B|(mZKWO~8sKwgm=tA=9N%79!MPIeMsQJ_0nc2YgRE8n<hXYl&TZVAX&)qNCP$BqC%|E;*DPpjp7LWSC5_u2MHuAk$8msZNwL5LrIgLD(SK0B5BZecHaaCxCLVT?kl37pfiG8G69N0|h3wjgKN!Rbw+pd{izV)ZE?Pw`E{C-?3>^M^WJ6lWx+Ez#h`SEp(4HcMv}$H6lfKA)*<ncmv|p8U-lhSwjm;z$r*pId~(A;cRV7TR}~(<Sbw>9iWdxL>&O-w5;Y*NI2(>uz9cOQ|ZEEUzU)OA~XgEM>?=*1`HyZI<StKB0MNF>ajh0wYimlkddu9rJH&`cn^6!d+S|a2wt$3wT3=WD1SG?y3^~?Z|v>vDF_!4B0nXy@9^>R^HKDo(-!rWDJpgLA-*ENvx9AyjH%Nz0000c-tPe%6$}|Q1ONsZI0#K?b8~5LZgT`|X>)W0X>?_66$}>24HkrB7K|n)vflwF(#ZiFHUKCCZeea12tjafY;12JF#s7X6$BLo6#@Vi02Krk0ssI26$BN^2Nlo*OchKO1QGxMD77#BVC4Yy1^|-I9SxAh4OG6h<gq(Mta=KCUJ_1cOq0JQ{!*0mmo>|b=?;ZCrgYF@5;vS=TcE$R%Pgc6t=JaGtZHowqF$B)g=kwC^s*wDza)-&X?o0<gY&;EmO?L!*}o(l+rl~B22{(MF@;&S0Yop$fIB8JYa1YD%+lLJE+C*HF}XWKWY7+@fcxMF)#(Bh0$%ro)WR@#nh@^v)z8DiTp0FX@k_i=BQ8!75IS(}N)f6z#A%TQu5+4eqlptT(Y+~Cwl9DVmH$R-iQ`FW1{VG}jN`T6gfmFk1-TV?6#x~|0Ttu{EEUQH6$BLq6$TtO;shuNI4?LaF*!Lg7zi*lFETSPFfjlC04TLD{UB*c0{}Sy000yK1rb0L01ZKeK!^kk8~_6m6aWhWAb<ft8~_6g8~_UeAOc7P8~_hd0t7Nig2)sA4MBh;AOQdd4?rLc08tnR03eC7FpYCO02E0R6#-EdSr-;%+QxN};C&GoiX(ZH0000czV`tf6$}|Q1ONsZ7z#vXVRUF;L}7Gg6$}>21s0YH7On;+fb{_;knsT=HsS;*2ske|FEKeeF&GFiG%qqUFEB9x87vh96$BLm02Kfg1Qh}R000#P6?PSf0ZbJJ6$BCh04TLD{UAHp0RR#J002`|Q!OztHy|iOZ)|mKVrgM12mk;8L2z$uY;Pbj6#xJLQ&dwRH8CwrASgp<VQg$=Zf9k3DHQ+}Y!!Yi70Lw_1QiAq1{^l31t=0zR8uW6FgGA5LvL(#ZDMI*DHsSraBpmEZy+%M001bpFa01ku>k-q0000K00RLq00RLU00WVV0RRI5EC2%uQUC*qE&u}o8UO<U5C8=MKuiDw0T2KJ1rUUyY9{*o0UQ+!88rj|1{oL)L}g)gXkSffb8~5LZWRm`$^{nc0v3(~CX)IAChYhD95$*2C=ydtQ!OztHy|iOZ)|mKVrgM17zjadZ)|LDATa<LEENP51Qh}R6#x|k6#@VN02Krkz$+EN9849s1r-Dm001bpFa2QP3AH!?8e%{fIv`%F15!C&SPgZ-|I@G{`;fP+VnQ?YQPKD<zD-d-ZWauVW)J=3qP?|8w{!i=P>Z&nR&;<i6i5L*0bl`p0e^kN3g-RSXic{>FC-SGd+)swm`TCtT);u6`>*HpphEAz9%N+NQ#0di{}-FFqrCt7*upd2vlIZ3%7Qj2ndMgmAMXDD#A}rZ)PuVJI!(FdZU6UPRp<8qEJG_ElNq%3e<mO9@ZK_5_kXD-LYhE-QJH;r`>)A9fP!h5U8!DMmv;Y;6z>t-e+{NGDtf&-V<*G#2&I8rUQl7I(g6DeeD{A11cW5_-ut;k0WpphR@(mS^5GjK5nu<fM81B8s$5YK51DF*+HgFt`~Q}a4$R(rD<v>O@Bc>B&eHuKQb~e!|FtFA64L%(cy)x`|7}nrLihhnuo<ZRA4`lm!2KVvsz$p1nv;`7)&6f~a6GmDCm7mB_y4*E)v5j0Xn0KN+W*m(=8*S)>l!CNTmVn@e>0$jy#tzQw4Hr+lHsf*?;i(om5jV40K`R;#_KNc4z1kTR^)0&&yUM(+JC*}$lrqv;H&+gZ^BxI0*q^*aI3QJqNsav{*ok7I4OUzV|o1%_Jq0rn#q|{%t9DCMd6kyXxSw+4~uZGd)<GX8Kew@Os_KUtB4qNg3?;K{})&jR%EeZyZ@Rp3ZPL+5-p|>Y{Glhy0exnFycBA+x_1JTAnZ*nb5uWE-LdR=PM4=2l0z$BT;e9RMCsO|GHC4hrIXR0wheLlcZ_tj1qYsiUa##BE0kHW7vUAkU5jG`|R4AbL%!RbPTiJX~{p?Ax}%>zv=e8|1WOw;IOoj`+xS!5vhuYAiYZtosQ%rbtudq%KNXos89m$zpfNw=ehqH^8%FE{(mLP65{@U7-TU=00!y(zXazYkS!E0!7(l!`jYnlB9K$O`+p&q9bz1!z5nkaOB|a%;JncJk#~eZLtHz}C+Le5*9HhU&2tPoMNAIrNJ!Iqg%U-wwkjGDgS4a-9FxJD&!;x?O4UH96!keHXGzRJG94R%23~G`z5B28;B{W@y|)Akhk|0T#1t2Zcm(nyYKG>NEu&+N`WU;c+J9XJ4^gF*=Gs)z$pSixg|FJdD32fwtGa30+a2`YdqbJVjXze{s)H)JY)XFP3cC&;CvWE{>hh`km>~~!YCydIdMv$sT9!rQTy#=VNKF9LqJn5U1yV_t$q%o%{nvG{ep*oolrf<g_HC62RbfHY&%O6v(4(yp%?fdhtA_AenxwXficvTVRo3N-0AB;kIB8R~Rl~dy(V7FDOpAnsBQCOy%w(D~v*epKI#bd_ff3D@^pQTtE59$qY!$&V);vxMSSu?gB6qC)S(zNzvN%!Zrl(5eI3qSXgO<DEAVQ&5gD~PCJ+V!*ru~1+?o4unqFvBfI1gT>7re+RwZ1c#t3fugt!c%1Z|&-s6#pB?q^o6qR5vb3US9lcHkmYgYk<)1y>|s@U$h*6#up4XyD_^z<|=$aR{^wMV1v6ccCa1PQiD=6k>#h0%I4)2-G6O9AxEu)?TTPVkgn^ZG_`zzMx_#KUTH9;!(YfZrt%iY9Bon|gA}4E`dEIWM_cv8p=!pb;Bo@^(#lEeNMIx+5^NATjM%v>F6A||K&cegpV!RBc?-7)bN{uQ5qj3cEUHz_yd_TLGVD4Af_<MBAta5rzOYV0aOnqpSXZ3<Ik{L7g2ba2Y?AJ~|Jtvp3p#7SPgKrvo7vv9bNjCwjR1IGd}styEuhLYA_Fta+0>%t-~zm!<IF7pw#n}PYjA=IVobR@;4IR$RU$)s?>+Sfh?#}(jO9SOi4eC+yT!0{j9yXQiiBQg2qqD_*|-~H>k#P(7r8S?-2p@+i$MxYC*zDY1K$ymBCQ;r7Dxz)qB0tPbPK}}AT0Ct*JU7yDveep<eG?pZ<}QeffA?@WH54^5EZ4ctN~$0A~J>N0TEF80h@&zg-4fTc5cVvK1NMS22C-9y)n8>a#Zb^(=$Z$6+_v3ZjvyK(O)z-!mr<~CQnSise<tm69~<-bH+E!oAP8|thnp#CWBZ1U);Mvtj5wX$9-05Omojz<YbLe?bWVvgeABdD%j)7vACo(np%h5YG5WMw!FZEUiM4(t!5OjBW*veZxT-)?A{25$8lEY@>!h~3(Ps*jRTF5Z0MfmYuR`~w+h-4-R!0lb~t+gD@xF(pso>Ris1AvPqYP$m$yw{?5%^w#^Hr#J7cx54-XKtb7USWz9VL>%#KD|&@_33Pp`Se{(fE4f_ulC5W33RP*EEsN9PqloZ?HfjKq*kZ_GMVr&iL;+R0`kJ&ZrKWCJ*2-Ii$mF+>*r7WHb;?FSVA6}$!&&;~3O$^{h!6$TXs92f`y;IN250000O2moyL^qc<w{}uo!2ms))h(G`U02l}WZ1wb;{{Q~~001bpFa2Pi0Pzd}0{{R3$^`)lTL1zG7(k$afddE<C|JOtfrAGSB1o7(p@M}A7&2(sz@dYO4<JH_7(t?hi4!PNs93?Gg^L$3V#t_5qlS$eICALN!J~(dA3%Z#8A7Cpkt0ZwC|Sa!iIXQ#qDYxSrHYj+Sh8r@!ljFsFJQum8AGOwnKNk8s9D3Njhi=c;>ejpr;eRFc=G7k!>2$WKYsuP5;TZVAw!1{B~rAAQ6oo>AVrciiBcs?moR10w24zEPoF@A5;clcDO0CVrBbzuRV!DoV8xO(i&m{#wr=6drE3?jUcP<-3npwBv0}!KAxoxg8M9{2o<WNyZ5p*|)~;d8rfnOyZr;9u3ny+IxpL;tp-ZQ39VK?{+`WSrPu@Iw_3Yilmrvh5e*OIY0~k=?s)3>i7BqMeVM2uq88&qI5Mo4$6Dd}-coAbpjT<?3^!O2ENRcB+mNa=1WlEDO&#h$H(&bB-F=fuAS<~iCO*nJv+{v@2&!0fO1Qj}zXi=j_ktS8Tlxb6^PoYMYI+bcwt5>mR)w&e`001WRp#mHg1Q|6100tQt3PNdebZB2hVRU5`3>L}-7M?Q}vLq&?ngS-m{Q(>p2ms))h(G`U02l}WZ1wb;{{R0L04N9m;IN250000O2moyL^qc<w{{R^*6$BLo6#@Vi02Krk0ssI26$BNSUKOe#OckU96$BCh04TLD{a}n1T|xlbX=oBUK&vDj!!QiPFbreHF`Svw$dX;qN=eqVB&10~LTYsk4b9B1Fl}sY_yOmXAS!B-R-gO6?_)~MN&yoA6#*Fm4LKak@^qRlFp~sf9A^I$xK0iyA25d%QzQQ=El;u?p5%x`PR;4y|A0*AayLgTm_q4;ahOSq?P`Q7rnWZEad-UB*iPzMoH>w|)K<virYSrGq{fntpeD_}{GV8U(<<dqb78_C|0#0H*7(BQwE7%+{C~J6ZoE{KBaFi=pY`;){a_h2cd*vV{{s(=nTj$jA6gRj^c;t<h9w9xz$ve`_R-M7e+Lr_LlW~J0wry39TZr?i>+ye{}Ur0(0>5f8jC#I7CWcVfaRCbYKQ!vxT=&es<5l^X;X-0DEyaT37Z>VDp)>z8HS5*8Tx;L%NVpP6xg_Fv@m>&nFn>7Ioj~TILxl6uCqj!!vBqIgBLdA%9XAR<1l+xq%X={zF;hHozt^K{zqKR4^A7C;De7{?ka>}aZ)N$=s(8QI?Qc}bg3xc)i~t;0jDL1c?vAQ&ep7sM?u4Wn->BcIgJ*(gDqzM7kCyfcUD+7Nm7yL>P^M*KY`R}IbhErUs#4YD-o&4e~0H%lOZL<P*<nc3dr%_z|{z`4OXGHrkW`mMz*FUC%h1zmJ&X_une&3mLsPcmo2BQFvk%RbS%t&ht|}CwIo66!X7eQZQOWa40KajO~OESFam4Lc6pYcv)F^_VoAH)Zif6PpsN*QnA9Zvx0v{^(J)enCuzcuf|``d2>&6pLX~*bq^<dH(fM4OP_G%}zeUS!zWk5ijXhXWuhOTD(6ibIvA0M?oe;}3Gl03+Ah2RhMr$1TkFmk+Ld$;$rxH^yA+}B6xlXF8{C7~$P+HzJUY_j**@yu_SVp8AjWC2I^&GHGsj-9q6^r{Hz{TTOBmW;9c*01j%W8*&J(ydHAN;>~%T;Fu#$omx{=cZKX|>}l=syIbA{Kc~H=WXAg^DR`9SIaZ3K0W1(vyUkNmf7`73T0{qT=EnsSv}mAA{s1X>Te-2^TMqh721v)0*&~Ldm@ta&YJtAy6u$rq!y|!X7gB*7A6;!VR{HwXrJyAt;oR@Sox_fQ>JX@LxdZbDPxsk4R@l*q3`Rokd0H96}Td-?CE)p(k5*IxSD@$}_EY=IXQ@0jtkhl?V-rhCO5pxEn9bViUrD3W^`Fw~CoY6Ksj8c$`*1K}n}e5w;qZ4lj~oOQ|9?b6%rIq;Ijk3Pqj8RGYwH^+icY)H!udAq^=XsHv^Zs>Jd1^8aE{rTzG?;jlHtJQ$AzE$lzV!cA+jh5wX{ur<`MRTHV9#bF3*9MAHUo$>zxA9oPLGN@;9^%}2EWW7xY@1-_E{~!KKJgp`4q)xe=u~<E&q~(f=R3w|r)*wbUDvZ}<cRXssmj4oX!BZ-REoL-2v88jHBL7)7cd+bKEIUa{5cB^bBd`sMBv}x<Qi8)#sj-!EBo%rvlLX1VDwdzil7<c*Dq3ty1AOeRY;F1ffEspHU11pu=eRHI3W1HNfh{q{2$9T)BuPQi7;%KeAm*f|dJ!Nnq?AHTkrA>|kb<Nzi~#}nX(kY9q(0M`UImE|(?or+7r#KwLP>IZ$>CJOf?4m}{O1y=lbSaEBkKdEky8&-dZFiF_d8>*ouX2Uz0guNiBoSs5pzLeXT&Lx<4r*AiinA`O|kLgLCrj?eyXsyY>FYGJLo9ztWr_9DAF;R95Ss%qSoTfNux8%1prYTO12fnGt2orZtWBV9Z$=cem#<J%7|R=Ua&Pmq^B+3$25l{@+`;|VE#VH*6i_6cp8z`gg7YhwJpg>3+^(<M5bv7fm~l$C=1XsQv*O_C&5sItw$Ae?*WQ@T``gt=?t@|f{}s`ldUeorqRMXQ!q$;bPCusY-iK>`DpU@c(rzVimH<y0~LrBBzFnu%;+@ABHqo^BonIye>Q{X-2CiG%jQMd2R=`pGOKny!bJ3WT%V8*S-~^)_J9&!ZP?Ho+$ndYqS#AVyjKalrc==0!*MBZ@PiA~)$rkrPc1M`!MFD?><a)_&W={Kh+Wz?CgpNx5l1W$H)K#N`4s;FPa7v^bh>kxREt58dz!OHg%(l!MZCJV91HM=^|lrt;cNIwI5@LQOW`tNxJpJYixcd_xH7(BAqynUMs4?4{D(*z_Kt!c#Fb;6Wem*6$IbCHM2O5@p@tT7T;N%_0Nip;8W?^N9ozT}JbSQE{*FE#9Y$>vT9rs)G-_nN6Ya~xn1<WU=9lh2<r5|{n)-4D4I!NYCcvipy??WhVQjj0SR}DTA(P<a>kyov#xtQFB;~ZP*;*=N1E*a_zD@3B7bM;yurnwG!a?w+iINz}#vrOF7ziw2CFu3=tglwIiYn#=@VpZ;w6l$N4uaxR{Owq7CoJ$@>&S|0qpC7*#WXpkCaxbPwqh=78Q>7201<ME7%m$W|Nn}a2GID#VqzVLI$h;(A=6kAhqhp-AULITgpJz<<X~>7!<Jp5eGRzqstqN$X?A7ewL}l@*qiE_F-nR!im{XdxHEZQdSArHPEpOF1+7}(tT(TnE154iLLcYYgMNZiBMEs<M)`OI1RbTmspd~*x*vUd4>n(}llTdj8;N^oz2!9{B@S>!0aXII03Z&c7nGn*c^Hm5=@x<3Az5Txm^QWMdAApsqqT86RPN5(+Q4lj;Q8Beq*m>!Xxay`{ifx<j)l}jVMcYv4Yr*G!mU0sG~wJ`6eV5TGc^?e6|4*u$O|kL(h3y>6$TXs95w(b18!k%7$HGvav(-;a${v6Np5p=X>@gTWgu^6AXH^zXl`$8Z)bS`001bpFa2N^0@W4(X0f#~AgWOZJiu78aQz2OA7#k4E)U&x(>g`lxuNCMSaKKKSTgr`vD{oq_9H>8a8e%G0k8n00H^@74W9j{Vf$1jzv&DZUjNbs3l%Pf2|dTYny9mnKJTU^;q|XcX#@xl9MIGTNN1X=3>F-vJDq}D0#qZwxDy{Z4HUR}wh<Um6M)SCH1h(Ol~@Aq07hk5-WjhYK6QO^bwHKW#nmV&Il}2{3Q5*;T0(}6srl3D9*0-*sVoLq8<xfel7(2ZeX&-H3<;Oz)W{Io3n^h=i(Ubl1Yt`7`A=T05KSB;Sld2US(d~@j>i2$pl}c!u?au08uB#z*^5$-1oA(y-nmrockiRe>->zW;<3YZtW-I0m>YRRzpeJOQ3JSUKRWL=Wi+$jYEn@&YQx>)=WRSg2i1IZ7G-3pTns2&^d&$4!Wf>|(f|Dm7esc53bVHk;wjxZZlV81Gg<5vDlk);cg~tAf+%`l0`CbYYyy|SD+!%-lM;6QBWM}DB0^vgyAK{Za0o*-y0N_m2tka?Q#IK$>PvHWF%lqS>kY$NuoXoU&6zD5=dabv*oDn-X;@QShRh#z&N**;9wUY|!?Z-+Rten80%QEb20(6gt6u!<l8@JMo;|hVvS~QsmZTQy#m~|byr1O;#)3?7cKq0-{t9cdCTj($$`X}4MarL5QD&d^{><(JZgoR>a*qzf%1IL@?2>I8DoKL#A#p6v>eZ2JB;T?Kkq>2AmStI9IeRpBi?AZSjXt(goG#Iomt|8E5%~@sP1cOcN<eL>5FwxIArR|J{Qd7iL7<>OtOkU-mXYY{A3v!b8}74pr}*4GdPs2ioydbd`^?<gwdlw07VzA;!f&VOfa{yccCb0axYcnOLusnB!|0oX+XJ0Bo2e>yl>1t9$U(Dv8IjkSjYHNl`E0Cc>W8C5h2N|_BsDjC>T?^vz5piN(E=P53>h^900tR23PEgbVP8#QbY*e`Y-w|J1Zi|-Z50d_(h3&lYZjC)CX~ejCdi`#95w(b18!k%7$HGvav(-;a${v6Np5p=X>@gTWgu^6AXH^zXl`$8Z)bS`87vh96$BLm02Kfg1Qh}R000#P6^IBG$^=XmeiZ}~001bpFa2Ny0o@1yLd`28P;2u;U_Elgiw7PT9Zt(_|C`kE_SuqCRaFxcZ^MYDGX*qymlHZFEQq{6CRC(Kp+T}7$b<k(KhWY((H&fZLg~=^L-h9&9{#>iSi_FJha1)|dY6q?((Vd4#%W4P793_;M0({FqhD!v6CS0{N+He=o#d4^5P0P80ZsYG`mixM?e0Lcq*=jW7Q~No&B0R)^;50z61Fs6OzEZ<FA%yhMn9Hz7r`p+E+RT0KqI2b1HVa9(|3Z+9du*bMiF?D!R$-gnVcvXxl(Ajv8ZVc7yPh>C0M*@+F{M9h6Fp!6&Ngs+Xw~5`Hv-kj(0_D1Cr(Nh6O*YVS*2Dm|%w+F4$oW1v||(O(5Pd!49Kg5||Pd02Rap71#tU70Lw_1QiAq1{^j7C=DQ2Wpi{OM`dztVQzUC10X?60000ewJ-f(A^;Hy01f~E01yHLsjAii0t2b4!~+5bTR<QTL}46=kSNE(G)Cb(P*g0<&?JQ*O@=}_KxJJHWnjV+6`7y`!jf&<H7UiBaGm#604M-JGYMfKj%3q36Uda3U@8tIoz!BW0@@TpQEWn!8cU-Vg|G@4C8~=cG|R9+tk9amX&kG|64%lcFMvABwE!Y^fG;dGL(vFL!6fgKKq)hT1aVwVBS=*u#f3Zri9*m#t!xRfEQ)<NLUi1Yf-3-UB-0@P)K)b>-YACz0=k(23P1rjv=HMWq{88zln4;Y&hW%iNI(H>n-K{LMXUtWNM7<ZOPb^lSUF@gh?yw>gs>Hd<SqT{M2hPJ)WN(4U|h{&FNGj9p!FKn@+b^t90@=G0000c-rWKm6$}|Q1ONsZC<{Vqa&%~4P;6miWd(C|VRU5`3>L}-7Q_t}nhGYa*a9ZR(*hhe1Skz4S7mc_AV+0#ZDDSC7y}?dOaK`y6$BLo6#@Vi02Krk0ssI26$BN+G!@_+Ocjs>6$BCh04TLD{a_&sH8}tpb$AmraB0&4{Qv*|zti7-BqL2GNkmfGo2T6^t&GQ5AR2)h-*4DPZ=FB-*9|kOfp6b$UDQnhDFG+}CjtFTJ@PE0g^zbeT77Y7rs$|yY;bpvbx8DyK?u4MclUtLxDUBIM@DmndhZFR-}4dU?iikXg19TpTa>JpyJLvH^~B!Wa(9nU#xUwQPTU;;RLs=2bwahcI|a$xf#M{ByIXkHo!p&5EB7-*F<!KmsN7_O=VnG2cjw^#4n{z%7|7i%NQ)eA1b64~+_YYd4I<5y7WtnYoZQ_5(`^kh>ca;Z?qbB<H9G6L$w+c{3;4+`q2?huT9kwdHZ=pWy5{2U8eZE!Bks--LEbRzAJ=ks4H)5+;O-P4?g|BQQ|^v|w-;;W?i{(R8}@i-7zbT)cLGo&&E|uvk>&0jTyfWPTihK3)7BLQ@fUZ;z(MASad!>wXUfUS-7P%boLq<x+#N%b#Z0C#Mhl72fwIKi0a(C5K}1V0OdBZtg>X-<IPsLY9Uz9SV_%r(1}VEZQ5mhZ8CsO%Vchq&yn?oedOpL&Sm~_P?U77h$+{;NqfZ#Cv^1ji6fM1QLQMj9alxak!`v?ZyAd&DZJ~Ffg&9%UtEW|ryL+Vfq`w%sI|gStAw|QC+}%P#jGkb%Xknu$h<C_j4n`MKUtFh^$aRb)`m90juF=mqp|3}?K91}e3BdiD38Qa)ad!<YC&=9aV7Un~M6rfUsUc@|ksT}Uu957mF`LPnLNP9;FR({7cu^0dPe8adl5qODl^NU}!<35`cc;LaKC#eq!|C~K>uqRJ5P!kAxyhAqW>au?4b%shvvh?h)|@SJcMi|m7WFKXxnTp`z}IL!Fj}z2<DE%QN;1|i!HVh!y>|fQ4HGTy^e;s9q6H%=m-j@uLR5a^0-aaL8-~>zR@%00Zc4*=K4Lt|7;`1KI|lsRO~nXej2cRfP>dIwjz|5$OhzBaXX!XC>?VhCPPr2G+#WPFiVGGukK<|Wiy?QXzzwCunnioit_|+a(M(!Mad!@!xvLe=8q`|kX)M&|wm{vC{}@Ty<LX^?oFLyzAC}ln47KRV58RBHba-PNDauhXZNa({X=<OE2_-68oIb&hNA6Cc!-!ePBeO16<lsNV6Gjm0<QiGclnd^z5g{{fkQLX`-q4I*jkE`z?LosVWHVZ?7Sig<duuqUQo_pqW8&m!xjTi1`8c{xsMG{V=uyW^7$KvlraPTiiRvWtq*xCQX*=VMV3)UgYFY+&ld*QWI|uJT6vSJ!ov3RD#HbXkHRZ`jH|NPqM%1Ps?`V08B#Q0gs>HOdHzxNV(mtU$@thiZZVPW2iP0yx`9K)e5j(k$K3Z5>D6DvAJfp{k$2;?m8OqtwduJME#8H#UBn9;7MM>Ck&j|GlCGPIQpw`|PZw$-yj5~CapT^WyLgh-@YZ8H86#j$4J^6z<?GU54i1$XIHZfEuE1uC8w@d2&n3|$k(SYYhFX}lnT7YESO~KtgOc?zl2J?Kha6ZTor<4+SZdQ?-6@ziv0VS=zxJFF!cEIW0kXBz*?!QV48K<<6g5H%TrG$%Fad(fWo735Cii%!<Yi~9q3gS~;(JhKeh%muZB7hTs{(%Lkkr<>DWJ(c<h$Kmp)=`9nVU)yT9}zH+&nj&O{TDL>V+F_rjE{2Gs>4Tig))!@fD*7>j9DGKX*fullGvM{_Be3N=GAqGLqgz~u43#D5pczEcEZp1=g0Pn7PBKuA3nbD9_e5yV$q(=uzS9;)o=4FSsfWV)UAdrOQjM9U!A7eH!neDTG`h*zZ?23lFuK$IR-yGP(4Z<fR&X`Ymr4iP*=defZKG<F-m%L;1mBC04&o3bkbf88%8X2_<T1i$C?Cv-g$T=7WVw%&S5HcPcvwGQ1D!}E$I?&YEsFXHySrn4wMh5@`wfhe?WGaPe+!SqlP-jMZ@65E7M;hch+}TsgVq33wp3M@c=xe{$1wQvYBjV5xGHpV<Aus#W7o!MIhb2jke%$xH2v8mDxHL{AnYst)z^RYNuJ|z0Q>5Kmyp{y;%b)pBw5jt#7iM8tBR(#$wpVnx&oS?yxzsKF|+RP=}RK@0*bGY)21~J~~r2>AA2*9X&S-8&2WPsO!zf3D~0HKAb5I2}6Jga7)*H!wu@c*&0%$<z!gm|Jw>#g_7rWpD$>?8Gi!dC@+v3%K8sbI4$v7L^HXhQQ9%uruq~#!)kI|BVhzT?(8t6B!nC-6r<WVz%aT{d4iw2W_Ox>$;@Q`eEvfP*G2Ht8C#w@e0o#9F6()os86KhxaE2;^=K~NjvX)~K`!jCIIM}c&=!WjvpZoL|0hy(1r-t1Q#6Xl>`1R?zi%YaQy`|O0u=xiyapA}1}qiI1r-Dp1{DSzHUKCGS#NG@WpZ;E2ti_LZfA6FZU6uPD77#BV4eW+3;+WF007Db0ts6H0tgsDpn!n`2ofk*z@UMH2M{6@kT8Kl1q&B2WYDmo0EZ49K7a@zVg!j2CQhJ8p@PGN6)ak~cmX4Zj2Sd)*tmfshmIXQdieMOB#4k9M2Z+Wf+R@+B}<qzaq{E{lqgcBP^n_&3YIKdws48ig^HIi1;B(6Gll~MGG(}!IfF(_8Z~R!v~lwWP8>ON=+v=u2TvXjdaCRx!$(ISKYsuPk|9XUAVP(%7&?R~k)kI$7BOlB27;pkk03=76J>#<NtEzZio(EBlO_!=VKTxYlcr4_ICb*$2?nT8qDDm`RjS4gQ!->QIE5;es#Q8zwX$-=iYZe%Hn@7l0ah$ovuM?_b;}B_4!KO}s<Nwzl_0!&`NH!HSTJE6hRGpT%owj@$dV~r#;lpMXV9Vrkyd0HwQAO`S-}P@o3?ElI&cHk4T21B-@t_vH;!C6a|6!JsB#EhIx02Ptz*|thP!w0;>nvwuU0)BQS9Brmye4+8T(}L>*r6yKY)w^3LMzYN)&<-bQCmr5C8xGCcuLO92E>1H3R?#87K=vX>xREUr=meV`T(%Z+C7L3>L}-7WO+9s3azu`~oJJ-vS&q04N7pZ*FU4a&s66L1JlcXLN6F02wS51Qi4o0ss{N6$BLm0000L0vY@oH2@d}b7N>_ZDAEA02K@+0vH5NVQpn408AVJ000#VB?1@(S!H2z02K-)0vH8Ha&L8T02K@+0vHBUbYXOLb0q*w8~^|S6$~W;7zRgWZe(S0B>+qu0000L3?%{>6IE_xWpZb7VPth-bY)*nVQO!3B>+qu0000L3?%{>4o7lfWOZS5WnWEUYHxBS08AVJ000#XB?1@?O=)atbYXINUs7RiYb5|o8~^|S6$~W;7!OTpY-x01a(Q1ua$#;`Xe9tl8~^|S6$B*$7!6Z!VPj=qMr>(kXmoP`6$B*$7!p%(VPj=qMr>(kXmnplZ*_8W02Kr!0vHQZaA9L*UsqvlYjXe<3MB#<5mRtsV`X1gVQg!2Ur29ta&rJR0vHHQX>)UFZ*FrH0u=^KJOBUyH3S$0Y-w|J6#@Vi3?%{>1Zi|-Z6yFq8~^|S6$~W;7z#vXVRUF;L}7GgB>+qu0000L3?%{>4Mb&ObZB2qX>)UFZ*C<3OdJ3J02Kr!0vHNHX>xREUqoSaWhD|!j1n9i0000005t*_3PEgbVP8#QbY*fC0u=^KJOBUyH3S$0Y-w|J6#@Vi3?%{>1Zi|-Z6yFq8~^|SH3Aq5LTPezXkSolVPj<#1OOEbB?1@)b97;JWhDSi8~^|S6$~W;7zA{0cWxyBOdJ3J02ayx85|k>6eie092E>1H3R?#85jgkVQpm<3>L}-7L<J!&_X7PJ0=JmHUKCOS$1!3Ze<`uE+9i;XKZB{6hUlZZXiM~AX8{%aA9&}AWCvBAOIOG6$BLo6#@Vi02Krk0ssI2CYVbc6$%+O1ONsZ7z9~mVR97=7Rm({fCv_X2PWi2CYD4T7zh9W0001FpFkK0000000Gysc7B(md000000A!y)7zh9W0001-o<IN@EENP51Qh}R6#x|k6#@VN04B&&92E)~H3R?#85jjea&L8T6$}>21r~q^7VZWnlujnvOdJ>p00000001;V7zh9W00000@IMwdC<p)m00000G(Z>#00000008hm02wS51Qi4o0ss{N6$BLm0000c#8?~^3>h^900tQt22*rlbaitT3>L}-7L)@PxC17bRwj&995w(b2U2BpX>w&`7zROObZK^F02wS51Qi4o0ss{N6$BLm0000cj$9lS3>h^900tQt21jLXWMy&{3>L}-7LEcIvH~WqS|;3C95w(b1WjRVWf%rVWo=<>WdIp06$BLo6#@Vi02Krk0ssI2Chl(>6$}|Q1ONsZ7!y@)WMy(^a$#h3VRU6*O<`(pauo~~$^{m(CKk>TCctSXpj{j`EGP$BZ*OdGXL%S3L1SZYb#8QNZf5`)EENP51Qh}R6#x|k6#@VN049Kt0UQ+!88rj|1{oL*M{;3gbzyX6Urk|ZZ*mn37Rm({#8Vd79wxGg0Vb$%95!|+DpqB5WpZh5VRCsOO=V<hV`*+>J0MVXVr*$+AVFkpX>MtAbaG*IX>V>AC_!a%Z*F0AbZKK@Y#=5eL34C+Z*F0AbZKK@Y#>E$XK8L_WpZh5X8;*26$BLo6#@Vi02Krk0ssI2CaRbL92E>1H3R?#85j*sX>4h9VRCt2Qekdu6$}>21s3cE7W4%s>XZQ{wvquHHmm|D3|47lWgtOhZE130Y#0$ja%pE_WNBq`AV+0xWpZI`02wS51Qi4o0ss{N6$BLm0000coS*?56$}|Q1ONsZ7!OTpY-x01a(Q1ua$#;`XcY_=$^{nK2o|IUCf1w*Cis~F95$o^C=pdtAWmU+c_1iKWprtBWn?KB3{_JgL1}UzMsIRsWdIp06$BLo6#@Vi02Krk0ssI2CXA*592Eo^H3R?#85j*yaA9L*Uq)<cXJ~YD6$}>21s1*p7M=tq+M)p_?x6u37zhUd00000000;W0000000000762#+2LJ#7000007zh9W000000000PEENP51Qh}R6#x|k6#@VN04C750UQ+s88rj|1{oL<Q*dEpWnV^YX=iA3Ur29ta&r|77Rm({z9|;!5GH`J0Vd|B0UQ_z5;6b)000007zh9W00000000&MC<qcV00000000;W000000000002wS51Qi4o0ss{N6$BLm0000c%)S8}6$BYI1ONsZ7z<NyVPj=qS7B^xa}^90$^{n41s0eDCa${yCbYT%92f`+000000000O2mk;80000002Tl!2nqlI0000002l}W000000000087vh96$BLm02Kfg1Qh}R001WN#{nD_3K=y700tQt5mRtsV`X1gVQg!2Ur29ta&r|77Rm({jtmyg2PXc)0Vblr0UQ_z000000KiZ{7zh9W000000Du+%C<p)m0002MP(T<6000000001h02wS51Qi4o0ss{N6$BLm0000c-tPe%6$}|Q1ONsZI0#K?b8~5LZgT`|X>)W0X>?_66$}>24HkrB7K|n)vflwF(#ZiFHUKCCZeea12tjafY;12JF#s7X6$BLo6#@Vi02Krk0ssI2CcgIp92E>1H3R?#85jygWnpw^UqoSaWfcq-$^{md3Kp&gCV=$;CXn#~95&(vC<r(&I4?0dIWZUrFf=bRGcPbP02wS51Qi4o0ss{N6$BLm0000c`uhPK6$}|Q1ONsZ7!5>aVRUF;O=)v;X>V>73>L}-7U}{Pjsqr=`T-{F_yHU?ss$(#Q&dweF)%kEC_`^-b!}p4VJR30L2z$uY;Pbj02wS51Qi4o0ss{N6$BLm0000c^q~SA6$BYI1ONsZ7z#pZa&%~4L}7Gg6$}>21s0w&7P2HJq?!UI!u<gp7zhC1u!uka000;W0BrU2oBsd*762#+0N}8QKmY&$7zhAt_4J$m|Nj6PEENP51Qh}R6#x|k6#@VN04Chg0vr_#88rj|1{pXCL2PYdUrk|jWpV^;X>)W0X>?_66$}>A3Kr&T7L+a~l*Ixj$fE)rHUKCCZeea1Awg+!AVzO;V`U&oZgX^LbaixPAa7<MRApmmZf|UFXL$e_EENP51Qh}R6#x|k6#@VN04Cnu0vr_#88rj|1{o*|LTPezXkSolVPj<lb97;JWfcq-$^{n04HlXTCa%~5CdAVM95w_f4Io!#b95j_WpZs{Zh063AVEw387vh96$BLm02Kfg1Qh}R001Vyg998D3>h^900tQ-3qomfbZB2tY+++%1axnAZWRm`$^{noI~J%UCYt;LCYav>95w(b2U%}!Yh`kC7zjaPX>Mn9Z*Bk?EENP51Qh}R6#x|k6#@VN02YL_1s2K$CI}X$<pLA{02v$@3_(&-Pggo~V`yb<VHo%fFE1}IFF8R)K|w)LK|w)5K|w)FK|yyxLT5onK|yChLuWxjK|w)6LP0@IK|w)5LqS1FK|w)5LP0@EK|w)5LP0@6K|)PIK|w-yLP0@6OhHjWK~Q%@K|w@OL3cqxa6wH$K}UB)K|w(@L3cqxLP1SIK~6zKK|w=JL1#fhR6$8WK|)bOK|w@WK~X_LW<f<kK}B~$K|w)TK~X_LHbFr_K}mN(K|w)9K|w)5H&AvjFLyyfK~XSSK|w)5N<l$EK|xVLK|w)7K|w)5Qb9pMK|*IiK|w)GK|w)5QEhB_WJhRbRY!PeSu#~YHc)miFL^{bFE2PjK|w`EML|J9K|*IiK|w)9K|w)5K|w)5K|xVLK|w+=Vl!lQK|w)5K|(}0FE2SsFHkQpK|w)6LQ+9NK|w)TK|w)5LP0@6K|w)5K|w)AK|w)5V>41{WJgs&K|w(@FHkQpV^Df8FLyyfK~Z;AK|w)5NkKtDK|xVLK|w)6K|w)5M?pbBK|yapK|w-7Vn;D(STHeYWJgwcK|w-qFHkQpZ%}$KFLyyfK~YsvK|w)5M?pbBK|xVLK|w)5K|w)5LP0@6K}T#bT30YZK|w)5YfySGFF0yAFE2PjK|w`JML|J9K|*&yK|w)9K|w)5K|w)5K|yapK|w-8VOUBqVMaMcSy)nRK|w<}FHkQpIZ%2pFLyyfK~YsvK|w)5NkKtDK|xVLK|w)5K|w)5L{ULOK}Aw*Sy)nUSTHegV>3>0Vlp&AK|w@wFHkQpN>DQ|FLyyfK~YsvK|w)5NI^kCK|xVLK|w)5K|w)5LuWxjK}Aw*Sy)nUSTIs(WJgs&K|*RdFE2S!FJ><<K|w)6L_$$PK|w)hK|w)5LP0@6K|w`9K|w)TK|w)5LqS17K}9ieV>3>0Vlp*)K|w)5K}BjgFE1-WFJ><<K|w)6LQ+9NK|w)TK|w)5LP0@6K|w)5K|w)9K|w)5VOUaZVo^asK|w-yFJ><<aZocaFLyyfK~YUnK|w)5N<l$EK|xVLK|w)5K|w)5MNvUPK}Jq@SyxVMSTSU1Vn=j(STJaIWLQdiK|w)5HFh&EFLyyfL1#o~FJ><<K|w)6L1;liK|w)dK|w)5LP0@6K|w)5K|w)GK|w)5RWm|pSu$2;Rx(C&VKYrZYEUmPFLyyfK|w}AK|w)5Mo>2|FLyyfK~YIjK|w)5N<l$EK|xVLK|w)5K|w)5MQ1@lK}Jq@SyxVMSTI_1VOL~tWJWnjVl!5GV|PJ8c~CDeFLyyfK|w}AK|w)5RZurCFLyyfK~YIjK|w)5OF=<FK|xVLK|w)5K|w)5L{ULOK}Jq@SyxVMSTI_1VOL~tWJpaxK|w)DK|yyxLqS1EK|yChK|w)5K|w)6Q9(gLK}tj`FE2PjK|w`EML|J9K|?`7K|w)9K|w)5K|w)5K|we{K|w-JVOMx?WJgAMWmY*uV{JxtSu$rqX;3#WFE~UiFE2PjK|w`EML|J9K|?`7K|w)9K|w)5K|w)5K|wG<K|w-JVOMx?WJgAMWmY*;Sywf3K|w)5bx=1iFE2zZFE2PjK|w`EML|J9K|?`7K|w)9K|w)5K|w)5K|wS@K|w-DV{JxjWLHKoT2?tuSyym&V`o7@Hc&S&FL^{SFE2PjK|w`EML|J9K|@hNK|w)9K|w)5K|w)5K|)PIK|w-RVr^1vV{K%4SyxgqSy)nRSTHeYVQo2iK|*>jFE2S&FE1}IK|w)6LQ+9NK|w)TK|w)5LP0@6K|w)5K|w)BK|w)5QZiO`T1QrSK|w-AFE1}IW>7CLFLyyfK~YsvK|w)5M?pbBK|xVLK|w)5K|w)5LT5oiK}Jq6Sy)mrV|PJ8Vo)zHFE&&!FE2PjK|w`CML|J9K|*IiK|w)9K|w)5K|w)5K|xhPK|w-DV{JJxV?jYdK~7>XFE2PjK|x7DFi<ZqFLyyfK~YUnK|w)5NI^kCK|xVLK|w)5K|w)5LP0@6K}KwBSy)LyK|xtTLqS1DK|xtTK|w)5K|x7DML|JTK|yChLT5opK|yyxK|w)LK|(=6K|w)5K|w`EML|J9K|*&yK|w)9K|w)5K|w)5K|xVLK|w-KSywS^K|w)5K|xVLLP0@AK|w)5K|w)5K|wt|02m)|VRCVGWppiLaBwYQa&m8XAa-SPb7^mGAU7^BE-)GV6dV8m8~^|u000~S02}}S8~^|u000~S02}}S8~^|u000~S02}}S8~^|u000~S02}}S8~^|u000~S008$8002-yQZW"
                )
            )
        )


if __name__ == "__main__":  # pragma: no cover

    md = AstronautData().get()

    print(md.schema)
    print(md.shape)
