# Import librearies
import pydicom
import numpy as np
import matplotlib.pyplot as plt
import cv2
from dicomObject import dicomObject
import pathlib
import os

# Define main function
def main():
    # Set dicom root directory and export directories
    root = 'path_to_dicoms'
    destination = 'output_dir'
    dcm_root_directory = root + 'dicom'
    output_dir_8bit = destination + '/8bit/'
    output_dir_16bit = destination + '16bit/'
    json_output_dir = destination + 'json/'
    data_root = pathlib.Path(dcm_root_directory)

    # Create folders
    if not os.path.exists(output_dir_8bit):
        os.makedirs(output_dir_8bit)
    
    if not os.path.exists(output_dir_16bit):
        os.makedirs(output_dir_16bit)

    if not os.path.exists(json_output_dir):
        os.makedirs(json_output_dir)
    

    # Create list of dcm files
    # This line is searching for files:
    all_dcm_paths = list(data_root.glob('*.dcm'))

    all_dcm_paths = [str(path) for path in all_dcm_paths]
    number_of_files = len(all_dcm_paths)

    # Go trough all dcm files and export
    for i, dicom_file in enumerate(all_dcm_paths):
        # Progress bar
        print("Done: {}/{}".format(i+1,number_of_files))

        # Load dcm
        my_dicom_object = dicomObject()
        my_dicom_object.importDicom(dicom_file)

        # Generate name
        name = dicom_file.split('/')[-1]
        name = name.split('.')[0]
        
        # Save data
        if (my_dicom_object.checkForTags()):
            my_dicom_object.exportDicomTo8Png(output_dir_8bit + name + '.png')
            my_dicom_object.exportDicomTo16Png(output_dir_16bit + name + '.png')
            my_dicom_object.exportDicomJSONData(json_output_dir + name + '.json')

   
# Call for main
if __name__== "__main__":
  main()
