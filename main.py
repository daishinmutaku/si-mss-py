# coding: utf-8

from Algorithm import meanshift_segmentation as mss
from SI import selective_inference as si
from mpmath import mp
from IO import csv_writer
import param
import artificial_data as data

def main():
    mp.dps = 1000
    experiment()

def experiment():
    data.init_X_origin()
    result = mss.segmentation()
    selective_p = si.inference(result)
    csv_writer.csv_write([selective_p])

if __name__ == "__main__":
    main()
