import subprocess
from arg_parser import input_parser
from icv_functions import (
    convert_dicom_to_nifti,
    extract_brain_segment,
    plot_mask_overlay,
    estimate_volume,
    output_icv_estimation,
    calculate_dice_score,
    clear_output_directories,
)


def main():

    args = input_parser().parse_args()
    TEST = args.test
    PIXEL_SPACING = args.pixel_spacing
    SLICE_THICKNESS = args.slice_thickness
    clear_output_directories()
    try:
        niftii_file = convert_dicom_to_nifti(TEST)
    except subprocess.CalledProcessError:
        print(
            "Error during converting DICOM data to Nifti. Make sure input data is available."
        )
        return
    try:
        mask_file = extract_brain_segment(niftii_file)
    except subprocess.CalledProcessError:
        print("Error during brain segmentation.")
        return
    icv = estimate_volume(mask_file, PIXEL_SPACING, SLICE_THICKNESS)
    output_icv_estimation(icv)
    plot_mask_overlay(mask_file, niftii_file)
    if TEST:
        calculate_dice_score(mask_file)


if __name__ == "__main__":
    main()
