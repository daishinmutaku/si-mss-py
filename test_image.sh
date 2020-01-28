#!/bin/bash

### 時間測定したい処理
for i in 13; do
    for j in 32; do
        /Users/oomoriyumehiro/.pyenv/shims/python ./main.py $i $j
#        nohup /home/omori.y/anaconda3/bin/python ./main.py $i $j &
    done
done
