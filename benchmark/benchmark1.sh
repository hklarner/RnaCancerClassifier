#!/bin/bash


gringo='/home/klarner/Tools/Potassco/gringo-4.4.0-x86-linux/gringo'
clasp='/home/klarner/Tools/Potassco/clasp-3.1.1/clasp-3.1.1-x86-linux'

echo "rows cols healthy time_first time_all solutions" > benchmark1_results.csv


for rows in `seq 10 10 500`
do
   for cols in `seq 10 10 500`
   do
      for healthy in `seq 0.3 0.3 0.9`
      do
         echo -n "working on rows=$rows cols=$cols healthy=$healthy ... "
         
         echo "vector_index    = matrix(seq(1:$rows),$rows,1)"                               > benchmark1_tmp.r
         echo "vector_annots   = matrix(rbinom($rows,1,$healthy),$rows,1)"                   >> benchmark1_tmp.r
         echo "matrix_profiles = matrix(sample(0:1,$rows*$cols, replace=TRUE),$rows,$cols)"  >> benchmark1_tmp.r
         echo 'matrix_complete = cbind(vector_index, vector_annots, matrix_profiles)'        >> benchmark1_tmp.r
         echo "miRNAs = sprintf(\"g%d\",seq(1:$cols))"                                       >> benchmark1_tmp.r
         echo 'colnames = c("ID", "Annots", miRNAs)'                                         >> benchmark1_tmp.r 
         echo 'colnames(matrix_complete) = colnames'                                         >> benchmark1_tmp.r
         echo 'write.table(matrix_complete, "benchmark1_tmp.csv", sep=", ", row.names=FALSE, quote=FALSE)' >> benchmark1_tmp.r
         
         Rscript benchmark1_tmp.r
         python benchmark1.py
         $gringo benchmark1_tmp.asp | $clasp --opt-mode=optN --quiet=1 > benchmark1_tmp.txt
         
         if grep -Fxq "UNSATISFIABLE" benchmark1_tmp.txt
         then
            # unsatisfiable
            echo "unsatisfiable."
         else
            # satisfiable
            time_first=$(cat benchmark1_tmp.txt | sed -n 's?.*1st Model:[ ]*\([0-9.]\+\)s.*$?\1?p')
            time_all=$(cat benchmark1_tmp.txt | sed -n 's?[ ]*CPU Time[ ]*:[ ]*\([0-9.]\+\)s[ ]*$?\1?p')
            solutions=$(cat benchmark1_tmp.txt | sed -n 's?[ ]*Optimal[ ]*:[ ]*\([0-9]\+\)[ ]*$?\1?p')
            echo "$rows $cols $healthy $time_first $time_all $solutions" >> benchmark1_results.csv
            echo "done."
         fi
         
         trap "echo Exited!; exit;" SIGINT SIGTERM
         
      done
   done
done

   
