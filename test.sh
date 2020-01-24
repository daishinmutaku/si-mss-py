#!/bin/sh

for i in `seq 10`; do
    `expr $i \* 1000`
    nohup /home/omori.y/anaconda3/bin/python ./main.py $i &
done
