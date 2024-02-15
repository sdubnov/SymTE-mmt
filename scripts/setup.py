import os
import sys

def check_exit_status(message, *status):
    """
    Check the exit status of a command and print an error message if it failed
    """
    for s in status:
        if s != 0:
            print(message)
            sys.exit(1)

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
    setup_exp_folder()
    setup_data_folder()



