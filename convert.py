import os, sys, random
from pyxform.pyxform.builder import create_survey_from_path

# Download directory
download_dir = 'xforms/'

def convert(upload_path):
    path_to_excel_file = upload_path
    survey = create_survey_from_path(path_to_excel_file)
    download_path = download_dir + str(int(random.random()*1000000000000))
    os.mkdir(download_path)
    path_to_xform = os.path.join(download_path, survey.get_name() + ".xml")
    survey.print_xform_to_file(path_to_xform, False)
    return path_to_xform
