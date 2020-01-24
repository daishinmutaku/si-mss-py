#!/bin/sh

for i in `seq 10`; do
    $i = $i \* 1000
    echo $i
    nohup /home/omori.y/anaconda3/bin/python ./main.py $i &
#    nohup /Users/oomoriyumehiro/.pyenv/shims/python ./main.py $i &
done
