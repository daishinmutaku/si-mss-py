#!/bin/bash

### 時間測定したい処理
for i in 5 6 7 8 9 10; do
    for j in 128 96 64 48 32 16; do
        nohup /home/omori.y/anaconda3/bin/python ./main.py $i $j > "./result_img_hs${i}_hr${j}.out" &
    done
done
