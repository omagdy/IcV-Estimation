import subprocess
from flask import Flask, request
from multiprocessing import Process
from minio_client import minio_input_data_download, minio_results_upload
from minio_client import minio_input_data_download, minio_results_upload
from icv import (
    convert_dicom_to_nifti,
    extract_brain_segment,
    plot_mask_overlay,
    estimate_volume,
    output_icv_estimation,
    clear_output_directories,
)

app = Flask(__name__)

app.run(debug=True)

@app.route("/run_icv", methods=["POST", "GET"])
def run_icv():
    if request.method == "POST":
        minio_url = request.form.get("minio_url")
        minio_access_key = request.form.get("minio_access_key")
        minio_secret_key = request.form.get("minio_secret_key")
        pixel_spacing = request.form.get("pixel_spacing", default=0.5)
        slice_thickness = request.form.get("slice_thickness", default=1)
    else:
        minio_url = request.args.get("minio_url")
        minio_access_key = request.args.get("minio_access_key")
        minio_secret_key = request.args.get("minio_secret_key")
        pixel_spacing = request.args.get("pixel_spacing", default=0.5)
        slice_thickness = request.args.get("slice_thickness", default=1)

    if not (minio_url and minio_access_key and minio_secret_key):
        return "Minio Server Parameters are missing."

    p = Process(target=async_icv_job, args=(minio_url, minio_access_key, minio_secret_key, pixel_spacing, slice_thickness))
    p.start()
    p.join()

    return "Brain Segmentation Process has started."


def async_icv_job(minio_url, access_key, secret_key, pixel_spacing, slice_thickness):

    check = minio_input_data_download(minio_url, access_key, secret_key)
    if not check:
        return
    check = run_icv_process(pixel_spacing, slice_thickness)
    if not check:
        return
    minio_results_upload(minio_url, access_key, secret_key)


def run_icv_process(pixel_spacing, slice_thickness):
    clear_output_directories()
    try:
        niftii_file = convert_dicom_to_nifti()
    except subprocess.CalledProcessError:
        print(
            "Error during converting DICOM data to Nifti. Make sure input data is available."
        )
        return False
    try:
        mask_file = extract_brain_segment(niftii_file)
    except subprocess.CalledProcessError:
        print("Error during brain segmentation.")
        return False
    icv = estimate_volume(mask_file, pixel_spacing, slice_thickness)
    output_icv_estimation(icv)
    plot_mask_overlay(mask_file, niftii_file)
    return True
