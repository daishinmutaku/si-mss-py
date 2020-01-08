# coding: utf-8
import time
from Algorithm import meanshift_segmentation as mss
from SI import selective_inference as si
from mpmath import mp
from IO import csv_writer
import artificial_data as data
import param


def main():
    mp.dps = 1000
    # for i in range(param.EXPERIMENT_NUM):
    start = time.time()
    experiment()
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

def experiment():
    data.init_X_origin()
    result = mss.segmentation()
    selective_p = si.inference(result)
    csv_writer.csv_write([selective_p])


if __name__ == "__main__":
    main()
