param fichier := "bin-packing-difficile-hard.bpa" ;

param C := read fichier as "1n" skip 1 use 1;
param Size := read fichier as "2n" skip 1 use 1;
set Objets := {1 to Size by 1} ;
set Boites := {1 to Size by 1} ;
set tmp[<i> in Objets] := {read fichier as "<1n>" skip 1 + i use 1};
param taille [<i> in Objets] := ord(tmp[i],1,1);
var x[Objets*Boites] binary;
var y[Boites] binary;

minimize y: sum<i> in Boites: y[i];
subto useBoite : forall<j> in Boites: forall<i> in Objets : x[i,j] <= y[j];
subto capaBoite : forall<j> in Boites: sum<i> in Objets : taille[i] * x[i,j] <= C;
subto limAffect : forall<i> in Objets: sum<j> in Boites : x[i,j] == 1;
