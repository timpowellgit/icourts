
#!/bin/bash
for i in 1 5 10 15 20 25 30 40 50 75 100 125 150 200
  do
     python lda.py --num_topics $i >> ecr_mallet_lda_topics1to200.txt
 done