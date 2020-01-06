# coding: utf-8

from Algorithm import meanshift_segmentation as mss
from SI import selective_inference as si
from mpmath import mp

def main():
    mp.dps = 1000
    result = mss.segmentation()
    si.inference(result)

if __name__ == "__main__":
    main()
