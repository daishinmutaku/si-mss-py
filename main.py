import artificial_data as data
from Algorithm import meanshift_segmentation as mss
from SI import selective_inference as si
from mpmath import mp

mp.dps = 1000

def main():
    vecX = data.generateImageVector();
    result = mss.filtering(vecX)
    si.inference(vecX, result)

if __name__ == "__main__":
    main()
