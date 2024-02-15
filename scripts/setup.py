import os
from compute_info_flow import check_exit_status

def setup_environment():
    status = os.system("conda env create -f environment.yml")
    check_exit_status("Error: Couldn't create environment", status)

def setup_exp_folder():
    # make directories if they don't exist
    x_status = os.system("mkdir -p exp/X")
    y_status = os.system("mkdir -p exp/Y")
    xy_status = os.system("mkdir -p exp/XY")
    check_exit_status("Error: Couldn't create exp folders", x_status, y_status, xy_status)

    #download pretrained model and train-args
    download_status = os.system("gdown '15ji-jGE4GICLMpEwlPRXb-Dv_RYqKunH' --folder --output exp/X/")
    check_exit_status("Error: Couldn't download pretrained model", download_status)

    # copy to exp/Y/ and exp/XY/
    y_status = os.system("cp -R exp/X/* exp/Y/")
    xy_status = os.system("cp -R exp/X/* exp/XY/")
    check_exit_status("Error: Couldn't copy pretrained model to exp/Y/ and exp/XY/", y_status, xy_status)

def setup_data_folder():
    # make directories if they don't exist
    x_status = os.system("mkdir -p data/X")
    y_status = os.system("mkdir -p data/Y")
    xy_status = os.system("mkdir -p data/XY")
    check_exit_status("Error: Couldn't create data folders", x_status, y_status, xy_status)

if __name__ == "__main__":
    setup_environment()
    setup_exp_folder()
    setup_data_folder()



