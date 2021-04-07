from minio import Minio
from icv import (
    input_dir,
    output_dir,
)


def minio_input_data_download(minio_url, access_key, secret_key):
    client = Minio(
        minio_url,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False,
    )
    server_input_bucket = "dicom-input-data"
    found = client.bucket_exists(server_input_bucket)
    if not found:
        print("Input bucket does not exist.")
        return False
    objects = client.list_objects(server_input_bucket)
    for obj in objects:
        client.fget_object(
            server_input_bucket, obj.object_name, input_dir + str(obj.object_name)
        )
    return True


def minio_results_upload(minio_url, access_key, secret_key):
    client = Minio(
        minio_url,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False,
    )
    server_output_bucket = "output-data"
    found = client.bucket_exists(server_output_bucket)
    if not found:
        client.make_bucket(server_output_bucket)
    results = [
        "icv_estimation.txt",
        "mask_overlay.png",
        "outputBrainExtractionMask.nii.gz",
    ]
    for result in results:
        client.fput_object(server_output_bucket, result, output_dir + result)
