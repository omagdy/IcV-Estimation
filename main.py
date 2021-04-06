import subprocess
from arg_parser import input_parser
from icv import (
    convert_dicom_to_nifti,
    extract_brain_segment,
    plot_mask_overlay,
    estimate_volume,
    output_icv_estimation,
)


def main():

    args = input_parser().parse_args()
    TEST = args.test
    PIXEL_SPACING = args.pixel_spacing
    SLICE_THICKNESS = args.slice_thickness
    try:
        niftii_file = convert_dicom_to_nifti(TEST)
    except subprocess.CalledProcessError:
        print("DICOM data is missing.")
        return
    try:
        mask_file = extract_brain_segment(niftii_file)
    except subprocess.CalledProcessError:
        print("Brain templates are missing.")
        return
    icv = estimate_volume(mask_file, PIXEL_SPACING, SLICE_THICKNESS)
    output_icv_estimation(icv)
    plot_mask_overlay(mask_file, niftii_file)


if __name__ == "__main__":
    main()
