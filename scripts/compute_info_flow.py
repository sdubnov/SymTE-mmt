"""
Chris Francis (cfrancis@ucsd.edu)

Script to compute Information Flow for a dataset

Usage:

python compute_info_flow.py OUTPUT_FILE_PATH

* OUTPUT_FILE_PATH: Path of the .pkl file to save the results to
"""

import os
import sys
import numpy as np
import pickle as pkl
import scipy.stats as stats
from scipy.special import softmax

def check_exit_status(message, *status):
    """
    Check the exit status of a command and print an error message if it failed
    """
    for s in status:
        if s != 0:
            print(message)
            sys.exit(1)


def convert_files():
    # get filenames
    x_status = os.system("find data/X/X -type f -name *.mid -o -name *.xml | cut -c 10- | sort > data/X/original-names.txt")
    y_status = os.system("find data/Y/Y -type f -name *.mid -o -name *.xml | cut -c 10- | sort > data/Y/original-names.txt")
    xy_status = os.system("find data/XY/XY -type f -name *.mid -o -name *.xml | cut -c 12- | sort > data/XY/original-names.txt")

    # check exit status
    check_exit_status("Error: Could not get filenames", x_status, y_status, xy_status)

    # make directories if they don't exist
    x_status = os.system("mkdir -p data/X/processed/json")
    y_status = os.system("mkdir -p data/Y/processed/json")
    xy_status = os.system("mkdir -p data/XY/processed/json")

    # check exit status
    check_exit_status("Error: Could not make json directories", x_status, y_status, xy_status)

    # convert files to json
    x_status = os.system("python mmt/convert_lmd_full.py -n data/X/original-names.txt -i data/X/X/ -o data/X/processed/json/")
    y_status = os.system("python mmt/convert_lmd_full.py -n data/Y/original-names.txt -i data/Y/Y/ -o data/Y/processed/json/")
    xy_status = os.system("python mmt/convert_lmd_full.py -n data/XY/original-names.txt -i data/XY/XY/ -o data/XY/processed/json/")

    # check exit status
    check_exit_status("Error: Could not convert files to json", x_status, y_status, xy_status)

    # make directories if they don't exist
    x_status = os.system("mkdir -p data/X/processed/notes") 
    y_status = os.system("mkdir -p data/Y/processed/notes")
    xy_status = os.system("mkdir -p data/XY/processed/notes")

    # check exit status
    check_exit_status("Error: Could not make notes directories", x_status, y_status, xy_status)

    # extract notes from json
    x_status = os.system("python mmt/extract.py -d X")
    y_status = os.system("python mmt/extract.py -d Y")
    xy_status = os.system("python mmt/extract.py -d XY")

    # check exit status
    check_exit_status("Error: Could not extract notes from json", x_status, y_status, xy_status)

    # add all files for test
    x_status = os.system("python mmt/split.py -d X -v 0 -t 1")
    y_status = os.system("python mmt/split.py -d Y -v 0 -t 1")
    xy_status = os.system("python mmt/split.py -d XY -v 0 -t 1")

    # check exit status
    check_exit_status("Error: Could not add files to test", x_status, y_status, xy_status)

def reset_directories():
    # remove processed directories if they exist
    x_status = os.system("rm -r -f data/X/processed")
    y_status = os.system("rm -r -f data/Y/processed")
    xy_status = os.system("rm -r -f data/XY/processed")

    # check exit status
    check_exit_status("Error: Could not remove processed directories", x_status, y_status, xy_status)

    # remove original-names.txt
    x_status = os.system("rm -f data/X/original-names.txt")
    y_status = os.system("rm -f data/Y/original-names.txt")
    xy_status = os.system("rm -f data/XY/original-names.txt")

    # check exit status
    check_exit_status("Error: Could not remove original-names.txt", x_status, y_status, xy_status)

    # remove samples directories
    x_status = os.system("rm -r -f exp/X/ape/samples")
    y_status = os.system("rm -r -f exp/Y/ape/samples")
    xy_status = os.system("rm -r -f exp/XY/ape/samples")

    # check exit status
    check_exit_status("Error: Could not remove samples directories", x_status, y_status, xy_status)


def make_files_consistent():
    super_set = set([s.split('.')[0] for s in os.listdir('data/X/X/')] +
                    [s.split('.')[0] for s in os.listdir('data/Y/Y/')] +
                    [s.split('.')[0] for s in os.listdir('data/XY/XY/')])

    file_nums = {}

    for dir in ['X', 'Y', 'XY']:
        file_nums[dir] = [s.split('.')[0] for s in os.listdir('data/' + dir + '/processed/notes/')]

    to_be_deleted = super_set - set(file_nums['X']).intersection(set(file_nums['Y']), set(file_nums['XY']))

    print("Removing", len(to_be_deleted), "files")

    for dir in ['X', 'Y', 'XY']:
        for file in to_be_deleted:
            try:
                os.remove('data/' + dir + '/' + dir + '/' + file + '.mid')
            except Exception as e:
                print(e)

    return len(to_be_deleted)

def generate():
    # read test-names.txt
    with open("data/X/processed/test-names.txt", "r") as f:
        x_test_names = [line.strip() for line in f.readlines()]
    with open("data/Y/processed/test-names.txt", "r") as f:
        y_test_names = [line.strip() for line in f.readlines()]
    with open("data/XY/processed/test-names.txt", "r") as f:
        xy_test_names = [line.strip() for line in f.readlines()]
    for x, y, xy in zip(x_test_names, y_test_names, xy_test_names):
        assert x == y == xy

    # check if exp/X/ape/samples/ exists, make if not
    x_status = os.system("mkdir -p exp/X/ape/samples")
    y_status = os.system("mkdir -p exp/Y/ape/samples")
    xy_status = os.system("mkdir -p exp/XY/ape/samples")

    # check exit status
    check_exit_status("Error: Could not make samples directories", x_status, y_status, xy_status)

    # generate samples and logits
    n_samples = len(x_test_names)
    x_status = os.system("python mmt/generate.py -d X -o exp/X/ape -g 0 -ns {}".format(n_samples))
    y_status = os.system("python mmt/generate.py -d Y -o exp/Y/ape -g 0 -ns {}".format(n_samples))
    xy_status = os.system("python mmt/generate.py -d XY -o exp/XY/ape -g 0 -ns {}".format(n_samples))

    # check exit status
    check_exit_status("Error: Could not generate samples", x_status, y_status, xy_status)

    return x_test_names

def read_logits(folder):
    """
    The logits folder (eg. /exp/X/ape/samples/logits/) will have files like:
    0_16-beat-continuation-beat_logits.npy
    0_16-beat-continuation-duration_logits.npy
    0_16-beat-continuation-instrument_logits.npy
    0_16-beat-continuation-pitch_logits.npy
    0_16-beat-continuation-position_logits.npy
    0_16-beat-continuation-type_logits.npy
    1_16-beat-continuation-beat_logits.npy
    1_16-beat-continuation-duration_logits.npy
    1_16-beat-continuation-instrument_logits.npy
    1_16-beat-continuation-pitch_logits.npy
    1_16-beat-continuation-position_logits.npy
    1_16-beat-continuation-type_logits.npy
    .
    .
    .
    n_16-beat-continuation-beat_logits.npy
    n_16-beat-continuation-duration_logits.npy
    n_16-beat-continuation-instrument_logits.npy
    n_16-beat-continuation-pitch_logits.npy
    n_16-beat-continuation-position_logits.npy
    n_16-beat-continuation-type_logits.npy

    This function will read the logits and return a dictionary of the form:
    {0 : 
        {"type" : np.array(),
        "beat" : np.array(),
        "position" : np.array(),
        "pitch" : np.array(),
        "duration" : np.array(),
        "instrument" : np.array()},
    1 :
        {"type" : np.array(),
        "beat" : np.array(),
        "position" : np.array(),
        "pitch" : np.array(),
        "duration" : np.array(),
        "instrument" : np.array()},
    .
    .
    .
    n : 
        {"type" : np.array(),
        "beat" : np.array(),
        "position" : np.array(),
        "pitch" : np.array(),
        "duration" : np.array(),
        "instrument" : np.array()}
    }
    """
    filenames = os.listdir(folder)
    sample_ids = [int(fname.split('_')[0]) for fname in filenames]
    logits = {id: dict() for id in sample_ids}

    for fname in filenames:
        if fname.endswith(".npy"):
            id = int(fname.split('_')[0])
            l_type = fname.split('-')[-1].split('_')[0]
            logits[id][l_type] = np.load(os.path.join(folder, fname)).squeeze()
    
    return logits

def read_truth(folder):
    """
    The npy folder (eg. /exp/X/ape/samples/npy/) will have files like:
    0_truth.npy
    1_truth.npy
    .
    .
    .
    n_truth.npy 

    in addition to the generated files.

    This function will read the truth files and return a dictionary of the form:
    {0 : np.array(),
    1 : np.array(),
    .
    .
    .
    n : np.array()}
    """
    filenames = os.listdir(folder)
    
    truths = dict()
    for fname in filenames:
        if fname.endswith("_truth.npy"):
            id = int(fname.split('_')[0])
            truths[id] = np.load(os.path.join(folder, fname))

    return truths

def calc_entropy(logits, truth):
    """
    Given logits[i] of the form:

    {"type" : np.array(),
    "beat" : np.array(),
    "position" : np.array(),
    "pitch" : np.array(),
    "duration" : np.array(),
    "instrument" : np.array()}

    and truth[i] of the form: np.array(),

    this function will compute the entropy each of the 6 positions in the tuple representation:

    { "type" : entropy,
      "beat" : entropy,
      "position" : entropy,
      "pitch" : entropy,
      "duration" : entropy,
      "instrument" : entropy}
    """
    # select notes from truth after the first 32 elements
    selected_truth = truth[32:]

    # select rows from logits corresponding to the selected notes
    selected_logits = {l_type : logits[l_type][:len(selected_truth)] 
                       for l_type in logits.keys()}

    # convert logits to probabilities
    probs = {l_type : softmax(selected_logits[l_type], axis=-1) for l_type in selected_logits.keys()}

    # compute entropy: mean of entropies
    entropies = {l_type : stats.entropy(probs[l_type], base=2, axis=-1).mean() for l_type in probs.keys()}

    return entropies
    
def compute_info_flow(output_file_path, test_names):
    # compute Info Flow
    x_logits = read_logits("exp/X/ape/samples/logits")
    y_logits = read_logits("exp/Y/ape/samples/logits")
    xy_logits = read_logits("exp/XY/ape/samples/logits")
    x_truth = read_truth("exp/X/ape/samples/npy")
    y_truth = read_truth("exp/Y/ape/samples/npy")
    xy_truth = read_truth("exp/XY/ape/samples/npy")

    info_flow = {}
    
    for key, filename in zip(sorted(x_logits.keys()), test_names):
        H_X = calc_entropy(x_logits[key], x_truth[key])
        H_Y = calc_entropy(y_logits[key], y_truth[key])
        H_XY = calc_entropy(xy_logits[key], xy_truth[key])

        info_flow[filename] = {}
        for l_type in sorted(H_X.keys()):
            info_flow[filename][l_type] = H_X[l_type] + H_Y[l_type] - H_XY[l_type]

    # save the results
    with open(output_file_path, "wb") as f:
        pkl.dump(info_flow, f)

if __name__ == '__main__':
    """
    Main function
    """
    # Check if the output file name is provided
    if len(sys.argv) < 2:
        print("Usage: python compute_info_flow.py OUTPUT_FILE_PATH" + \
              "\n\n(OUTPUT_FILE_PATH is the .pkl file path to save results to)")
        sys.exit(0) 

    # Get the output file name
    output_file_path = sys.argv[1]

    # check data directory
    if not os.path.exists("data/X/X") or \
        not os.path.exists("data/Y/Y") or \
            not os.path.exists("data/XY/XY"):
        print("Error: data/X/X/, data/Y/Y/, or data/XY/XY/ does not exist")
        sys.exit(1)
    
    # check if the directories contain .mid files
    if len(os.listdir("data/X/X")) == 0 or \
        len(os.listdir("data/Y/Y")) == 0 or \
            len(os.listdir("data/XY/XY")) == 0:
        print("Error: data/X/X/, data/Y/Y/, or data/XY/XY/ does not contain files")
        sys.exit(1)

    reset_directories()
    convert_files()

    n_deleted = make_files_consistent()

    if n_deleted > 0:
        reset_directories()
        convert_files()

    test_names = generate()

    compute_info_flow(output_file_path, test_names)
