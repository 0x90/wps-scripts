#!/bin/bash
CLAVES=72000000
PARAMETRO="$1"
CRUNCH="software/./crunch"
PREFIJOS='\
600
629
654
676
605
630
655
677
606
633
656
678
607
634
657
679
608
635
658
680
609
636
659
685
610
637
660
686
615
638
661
687
616
639
662
688
617
645
663
689
618
646
664
690
619
647
665
691
620
648
666
692
622
649
667
693
625
650
669
695
626
651
670
696
627
652
671
697
628
653
675
699'
let CUANTOS_PREFIJOS=`echo "$PREFIJOS" | wc -l`
if [ "$PARAMETRO" = "" ]
then
	let CONT=1
else
	PREF=`echo "$PARAMETRO" | cut -c-3` #extraemos el prefijo del último número pasado como parámetro
	let CONT=`echo "$PREFIJOS" | grep -n "$PREF" | awk -F ':' '{print $1}'`
fi

while [ $CONT -le $CUANTOS_PREFIJOS ]
do
	PREFIJO_ACTUAL=`echo "$PREFIJOS" | sed -n ${CONT}p`
	if [ "$PARAMETRO" != "" ] #si se pasó algún parámetro (=sesión anterior)
	then
		"$CRUNCH" 9 9 0123456789 -t $PREFIJO_ACTUAL%%%%%% -s "$PARAMETRO" 2>/dev/null
		PARAMETRO=""
	else
		"$CRUNCH" 9 9 0123456789 -t $PREFIJO_ACTUAL%%%%%% 2>/dev/null
	fi
	let CONT=$CONT+1
done
