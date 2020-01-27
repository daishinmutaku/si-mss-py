# coding: utf-8
import time
from Algorithm import meanshift_segmentation as mss
from SI import selective_inference as si
from IO import csv_writer
import image_data as data
import param


def main():
    for i in range(param.EXPERIMENT_NUM):
        start = time.time()
        experiment(i + param.START_I)
        elapsed_time = time.time() - start
        if param.DO_DEBUG:
            print("elapsed_time:{0}".format(elapsed_time) + "[sec]")


def experiment(i):
    data.init_X_origin(i)
    si.init_interval()
    param.INFERENCE_FLAG = False
    result = mss.segmentation()
    # if param.DO_DEBUG:
        # print(result)
    si.inference_ready(result)
    if param.DO_SI:
        param.INFERENCE_FLAG = True
        _ = mss.segmentation()
        selective_p = si.generate_selective_p()
        if selective_p > 0:
            print(selective_p)
            if param.IS_LOCAL:
                csv_writer.csv_write([selective_p])
        else:
            print("error", selective_p)


if __name__ == "__main__":
    main()
