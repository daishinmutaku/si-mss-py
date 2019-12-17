import artificial_data as data
import meanshift_segmentation as mss
import selective_inference as si

def main():
    vecX = data.generateImageVector();
    result = mss.filtering(vecX)

    H = si.generate_eta_mat(result)
    C = si.generate_c_mat(H)


if __name__ == "__main__":
    main()
