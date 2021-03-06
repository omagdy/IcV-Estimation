import os
import glob
import subprocess
import numpy as np
import nibabel as nib
from nilearn.plotting import plot_roi


root_dir = "/app/"
input_dir = root_dir + "input/"
output_dir = root_dir + "output/"
templates_dir = "./brain_templates/"
test_dir = "./test_data/"
nifti_o_dir = root_dir + "nifti_converted_output/"
ants_o_dir = root_dir + "brain_extraction/"


def convert_dicom_to_nifti(test=False):
    if test:
        input_location = test_dir
    else:
        input_location = input_dir
    dcmn2niix_o_name = "outputfile"
    dcmn2niix_cmd = [
        "dcm2niix",
        "-z",
        "y",
        "-x",
        "y",
        "-f",
        dcmn2niix_o_name,
        "-o",
        nifti_o_dir,
        input_location,
    ]
    subprocess.run(dcmn2niix_cmd, check=True, text=True)
    niftii_file = nifti_o_dir + dcmn2niix_o_name + "_Eq_1.nii.gz"
    return niftii_file


def extract_brain_segment(niftii_file):
    ants_o_name = "output"
    brain_extraction_output = ants_o_dir + ants_o_name
    brain_template = templates_dir + "T_template0.nii.gz"
    probability_mask = (
        templates_dir + "T_template0_BrainCerebellumProbabilityMask.nii.gz"
    )
    registration_mask = (
        templates_dir + "T_template0_BrainCerebellumRegistrationMask.nii.gz"
    )
    brain_extraction_cmd = [
        "antsBrainExtraction.sh",
        "-d",
        "3",
        "-a",
        niftii_file,
        "-e",
        brain_template,
        "-m",
        probability_mask,
        "-f",
        registration_mask,
        "-o",
        brain_extraction_output,
    ]
    subprocess.run(brain_extraction_cmd, check=True, text=True)
    mask_file = brain_extraction_output + "BrainExtractionMask.nii.gz"
    cp_cmd = ["cp", mask_file, output_dir + "."]
    subprocess.run(cp_cmd, check=True, text=True)
    return mask_file


def plot_mask_overlay(mask_file, niftii_file):
    mask = nib.load(mask_file)
    head = nib.load(niftii_file)
    overlay_image_file = output_dir + "mask_overlay.png"
    plot_roi(
        mask,
        head,
        draw_cross=False,
        title="Mask Overlays",
        output_file=overlay_image_file,
    )


def estimate_volume(mask_file, PIXEL_SPACING, SLICE_THICKNESS):
    mask_array = np.array(nib.load(mask_file).get_fdata())
    n_voxels = np.sum(mask_array)
    VOLUME_PER_VOXEL = PIXEL_SPACING * PIXEL_SPACING * SLICE_THICKNESS
    volume_mm3 = n_voxels * VOLUME_PER_VOXEL
    volume_ml = volume_mm3 / 1000
    return volume_ml


def output_icv_estimation(volume_ml):
    volume_file = output_dir + "icv_estimation.txt"
    f = open(volume_file, "w")
    f.write("Estimated Intracranial Volume: {} ml".format(volume_ml))
    f.close()


def calculate_dice_score(mask_file):
    v = 1
    dice_file = output_dir + "dice_score.txt"
    ground_truth_mask_file = test_dir + "test_brain_mask.nii.gz"
    ground_truth_mask = np.array(nib.load(ground_truth_mask_file).get_fdata())
    new_mask = np.array(nib.load(mask_file).get_fdata())
    dice = (
        np.sum(new_mask[ground_truth_mask == v])
        * 2.0
        / (np.sum(ground_truth_mask) + np.sum(new_mask))
    )
    f = open(dice_file, "w")
    f.write("Dice Score against the test mask is {}".format(dice))
    f.close()


def clear_output_directories():
    directories = [output_dir, ants_o_dir, nifti_o_dir]
    for directory in directories:
        files = glob.glob(directory + "*")
        for f in files:
            os.remove(f)
