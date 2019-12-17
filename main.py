import artificial_data as data
import meanshift_segmentation as mss

def main():
    vecX = data.generateImageVector();
    mss.mss()


if __name__ == "__main__":
    main()
