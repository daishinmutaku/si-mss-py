# coding: utf-8
import time
from Algorithm import meanshift_segmentation as mss
from SI import selective_inference as si
from SI import selection_event as se
from IO import csv_writer
import image_data as data
import param


def main():
    for i in range(param.EXPERIMENT_NUM):
        start = time.time()
        experiment(i + param.START_I)
        elapsed_time = time.time() - start
        if param.IS_LOCAL:
            print("elapsed_time:{0}".format(elapsed_time) + "[sec]")


def experiment(i):
    data.init_X_origin(i)
    se.init_vecA()
    result = mss.segmentation()
    if param.IS_LOCAL:
        print(result)
    if param.DO_INFERENCE:
        selective_p = si.inference(result)
        if selective_p > 0:
            if param.IS_LOCAL:
                csv_writer.csv_write([selective_p])
            else:
                print(selective_p)


if __name__ == "__main__":
    main()
