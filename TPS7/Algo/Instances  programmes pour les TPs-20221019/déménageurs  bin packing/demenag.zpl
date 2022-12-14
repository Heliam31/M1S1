param C := 9;
set Objets := {0 to 23 by 1} ;
set Boites := {0 to 23 by 1} ;
param taille[Objets] := <0> 6, <1> 6, <2> 5, <3> 5, <4> 5, <5> 4, <6> 4, <7> 4, <8> 4, <9> 2, <10> 2, <11> 2, <12> 2,<13> 3, <14> 3, <15> 7, <16> 7, <17> 5, <18> 5, <19> 8, <20> 8, <21> 4, <22> 4, <23> 5;
var x[Objets*Boites] binary;
var y[Boites] binary;
minimize y: sum<i> in Boites: y[i];
subto useBoite : forall<j> in Boites: forall<i> in Objets : x[i,j] <= y[j];
subto capaBoite : forall<j> in Boites: sum<i> in Objets : taille[i] * x[i,j] <= C;
subto limAffect : forall<i> in Objets: sum<j> in Boites : x[i,j] == 1;