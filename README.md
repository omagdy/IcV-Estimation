
# IcV-Estimation
A program for estimating the intracranial volume of a patient from brain CT scans. The program uses a python script to integrate a [dicom to nii converter](https://github.com/rordenlab/dcm2niix)  with the [Ants](https://github.com/ANTsX/ANTs) tools-set for obtaining a brain mask using [OASIS](https://www.oasis-brains.org/) templates. 

The following steps demonstrate how to use the program:

 1. ## Build the container 
Use the following command to create the container:
```
docker-compose up -d icv_app
```
2. ## Insert input data
A folder containing CT scan files in the DICOM format should be inserted in the input volume which will be mounted by docker to the container from the following locations at the local driver :

For Windows:
```
\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes
```
For Linux:
```
/var/lib/docker/volumes
```
 - ## Run the program
Use the following command to get the output:
```
docker-compose exec icv_app bash -c "python main.py --pixel_spacing 0.5 --slice_thickness 1"
```
where pixel_spacing and slice_thickness are optional parameters that determine the voxel unit volume of the scan.

4. ## Output
The output result which is the following will be saved in the mounted output volume of the container:
 - A file with the IcV estimation
 - The brain mask file in NifTI format 
 - A PNG image of the overlay of the mask in three orthogonal sections 
