#!/bin/sh

for i in 2 4 6 8 10; do
    /Users/oomoriyumehiro/.pyenv/shims/python ./main.py 8 $i  > "result_${i}.csv" &
done
