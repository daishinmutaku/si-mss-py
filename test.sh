#!/bin/sh

for i in `seq 20`; do
    nohup /home/omori.y/anaconda3/bin/python ./main.py $i 500 &
#    nohup /Users/oomoriyumehiro/.pyenv/shims/python ./main.py $i 2 &
done
