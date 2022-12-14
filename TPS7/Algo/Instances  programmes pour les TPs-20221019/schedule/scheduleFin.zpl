param fichier := "shift-scheduling.zplread" ;
do print fichier ;
#shift-scheduling_lecture-donnees.zpl

####################
# Horizon = nb days

param horizon := read fichier as "2n" comment "#" match "^h";
do print "horizon : ", horizon, " jours" ;


############################################
# Sets of days, week-ends, services, staff :

set Days := {0..horizon-1} ;
# All instances start on a Monday
# planning horizon is always a whole number of weeks (h mod 7 = 0)
set WeekEnds := {1..horizon/7} ;
do print card(WeekEnds), " week-ends :" ;
do print WeekEnds ;

set Services := { read fichier as "<2s>" comment "#" match "^d" } ;
do print card(Services), " services" ; 

set Personnes := { read fichier as "<2s>" comment "#" match "^s" } ;
do print card(Personnes) , " personnels" ;


############
# Parameters

param duree[Services] := read fichier as "<2s> 3n" comment "#" match "^d";
# do forall <t> in Services  do print "durée ", t, " : ", duree[t] ;

param ForbiddenSeq[Services*Services] :=
	read fichier as "<2s,3s> 4n" comment "#"  match "c" default 0 ;


param MaxTotalMinutes[Personnes] :=
  read fichier as "<2s> 3n" comment "#" match "^s"  ;
param MinTotalMinutes[Personnes] :=
  read fichier as "<2s> 4n" comment "#" match "^s"  ;
param MaxConsecutiveShifts[Personnes] :=
  read fichier as "<2s> 5n" comment "#" match "^s"  ;
param MinConsecutiveShifts[Personnes] :=
  read fichier as "<2s> 6n" comment "#" match "^s"  ;
param MinConsecutiveDaysOff[Personnes] :=
  read fichier as "<2s> 7n" comment "#" match "^s"  ;
param MaxWeekends[Personnes] :=
  read fichier as "<2s> 8n" comment "#" match "^s"  ;

param MaxShift[Personnes*Services] :=
  read fichier as "<2s,3s> 4n" comment "#" match "^m" default 0 ;

param requirement[Days*Services] :=
  read fichier as "<2n,3s> 4n" comment "#" match "^r" ;

param belowCoverPen[Days*Services] :=
  read fichier as "<2n,3s> 5n" comment "#" match "^r" ;

param aboveCoverPen[Days*Services] :=
  read fichier as "<2n,3s> 6n" comment "#" match "^r" ;

param dayOff[Personnes*Days] :=
  read fichier as "<2s,3n> 4n" comment "#" match "^f" default 0 ;

# penalité si jour "pas off" = "on"
param prefOff[Personnes*Days*Services] :=
  read fichier as "<2s,3n,4s> 5n" comment "#" match "^n" default 0 ;

# penalité si jour "pas on" = "off"
param prefOn[Personnes*Days*Services] :=
  read fichier as "<2s,3n,4s> 5n" comment "#" match "^y" default 0 ;

# do print "Services" ;
# do forall <s> in Services do print s, duree[s] ;
# do forall <s1,s2> in Services*Services with ForbiddenSeq[s1,s2] == 1
#   do print s1, s2, ForbiddenSeq[s1,s2] ;
# do print "Staff" ; 
# do forall <p> in Personnes
#   do print p, MaxTotalMinutes[p], MinTotalMinutes[p],
#     MaxConsecutiveShifts[p], MinConsecutiveShifts[p],
#     MinConsecutiveDaysOff[p], MaxWeekends[p] ;
# do print "Days Off" ;
# do forall<p,d> in Personnes * Days with dayOff[p,d] == 1 do print p,d,dayOff[p,d] ;
# do print "Pref Shifts On" ;
# do forall<p,d,s> in Personnes * Days * Services
#   with prefOn[p,d,s] >= 1 do print p,d,s,prefOn[p,d,s] ;
# do print "Pref Shifts Off" ;
# do forall<p,d,s> in Personnes * Days * Services
#   with prefOff[p,d,s] >= 1 do print p,d,s,prefOff[p,d,s] ;
# do print "Cover" ;
# do forall<d,s> in Days * Services
#   do print d,s,requirement[d,s], belowCoverPen[d,s], aboveCoverPen[d,s] ;



###########
# Variables

var assigned[Personnes*Days*Services] binary ;
var y[Days * Services] integer >= 0;
var z[Days * Services] integer >= 0;
var pen[Days * Services] integer >= 0;

minimize objectif : sum<d> in Days : sum<s> in Services: (y[d,s] + z[d,s]+pen[d,s]);
subto somEcart : forall<d> in Days : forall<s> in Services: 
    (sum<p> in Personnes: assigned[p, d, s]) - y[d,s] + z[d,s] == requirement[d,s];
subto penalites : forall<d> in Days: forall<s> in Services: pen[d,s] == y[d,s] * aboveCoverPen[d,s] + z[d,s] * belowCoverPen[d,s] + (sum<p> in Personnes: assigned[p,d,s]*prefOff[p,d,s]) + (sum<p> in Personnes:(1-assigned[p,d,s])*prefOn[p,d,s]);
subto  servDay : forall<p> in Personnes: forall<d> in Days: (sum<s> in Services: assigned [p, d, s]) <= 1;
subto Vacances : forall<p> in Personnes: forall<d> in Days: forall<s> in Services: assigned[p,d,s] <= 1-dayOff[p,d];
subto LimSh : forall<p> in Personnes: forall<s> in Services: (sum<d> in Days: assigned[p,d,s]) <= MaxShift[p,s];
subto MinDuree : forall<p> in Personnes: (sum<d> in Days: (sum<s> in Services: duree[s]*assigned[p,d,s])) >= MinTotalMinutes[p];
subto MaxDuree : forall<p> in Personnes: (sum<d> in Days: (sum<s> in Services: duree[s]*assigned[p,d,s])) <= MaxTotalMinutes[p];
subto JourConsMax: forall<p> in Personnes: forall<d> in Days with (d< horizon - MaxConsecutiveShifts[p]): forall<s> in Services: (sum<n> in {0..MaxConsecutiveShifts[p]}: assigned[p,d+n,s])<=MaxConsecutiveShifts[p];
subto InterditSeq: forall<p> in Personnes: forall<s1> in Services: forall<s2> in Services: forall<d> in Days with (d<horizon-1): assigned[p,d,s1] + ForbiddenSeq[s1,s2] + assigned[p,d+1,s2] <= 2;
subto JourConsOff: forall<p> in Personnes: forall <s> in Services: forall<d> in Days with (d<horizon - MinConsecutiveShifts[p]): assigned[p,d,s] + assigned[p,d+MinConsecutiveShifts[p],s] - (3-MinConsecutiveDaysOff[p]) <= (sum<i> in {d+1..d+MinConsecutiveDaysOff[p]-1}: assigned[p,i,s]);
