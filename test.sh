#!/bin/sh

for i in `seq 10`; do
    nohup /home/omori.y/anaconda3/bin/python ./main.py &
done
