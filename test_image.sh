#!/bin/bash

### 時間測定したい処理
for i in 100 96 92 88 8480; do
    for j in 32 64 128; do
#        /Users/oomoriyumehiro/.pyenv/shims/python ./main.py $i $j
        nohup /home/omori.y/anaconda3/bin/python ./main.py $i $j &
    done
done
