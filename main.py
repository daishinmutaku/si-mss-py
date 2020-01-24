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
        if param.IS_LOCAL:
            start = time.time()
            experiment(i)
            elapsed_time = time.time() - start
            print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
        else:
            experiment(i + param.START_I)


def experiment(i):
    data.init_X_origin(i)
    param.DO_INFERENCE = False
    result = mss.segmentation()
    si.inference_ready(result)
    param.DO_INFERENCE = True
    _ = mss.segmentation()
    selective_p = si.generate_selective_p()
    if selective_p > 0:
        if param.IS_LOCAL:
            csv_writer.csv_write([selective_p])
        else:
            print(selective_p)


if __name__ == "__main__":
    main()
