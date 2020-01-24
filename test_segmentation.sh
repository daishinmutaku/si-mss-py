#!/bin/bash

start_time=`date +%s`

### 時間測定したい処理
for i in 1 2 3; do
    for j in 32; do
        for k in 8 16 24 32 40 48 56 64; do
            nohup /home/omori.y/anaconda3/bin/python ./main.py $i $j $k > "./CSV/size_max2/Segmentation/N32/result_seg_r${i}_N${k}.csv"
        done
    done
done

end_time=`date +%s`

time=$((end_time - start_time))

echo $time

