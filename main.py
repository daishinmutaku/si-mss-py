import artificial_data as data
import meanshift_segmentation as mss

def main():
    vecX = data.generateImageVector();
    print(vecX)
    result = mss.filtering(vecX)
    print(result)


if __name__ == "__main__":
    main()
