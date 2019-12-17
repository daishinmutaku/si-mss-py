import artificial_data as data
import meanshift_segmentation as mss

def main():
    vecX = data.generateImageVector();
    mss.filtering(vecX)


if __name__ == "__main__":
    main()
