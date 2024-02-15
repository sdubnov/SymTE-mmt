# Evaluating Co-Creativity using Total Information Flow

## Content

- [Setup](#setup)
- [Experiments](#experiments)
- [Utility Scripts](#utility-scripts)
- [Acknowledgement](#acknowledgement)

## Setup

Create the environment.

```sh
conda env create -f environment.yml
```

Activate the environment.

```sh
conda activate mtmt
```

Run setup script.

```sh
python scripts/setup.py
```

## Experiments

### Generate results

* Make sure to place the X, Y and XY MIDI files in `data/X/X/`, `data/Y/Y/` and `data/XY/XY/` respectively. The X, Y, XY files for a sample should have the same filename. 

* Run `scripts/compute_info_flow.py`

```sh
python compute_info_flow.py OUTPUT_FILE_PATH
```

OUTPUT_FILE_PATH is the file path where the results will be stored as a `.pkl` file. The path should include the name of the file. You can save them in `results/`. 

Example:
```sh
python compute_info_flow.py results/example.pkl
```

### Visualize experiment results

* Open `notebooks/visualize.ipynb` to visualize results. The notebook has code to visualize the experiments used in the paper. The `results/` directory has sample results for these experiments, so you don't have to run the `compute_info_flow.py` script with data. 

## Utility Scripts

Three utility scripts have been provided in the `scripts/` directory:

1. `change_instrument.py`: Script to change instrument of a track in a midi file.
2. `combine_midi.py`: Script to combine 2 midi tracks into a single midi file.
3. `split_midi.py`: Script to split a midi file into 2 separate midi files, each containing a single track.

Usage instructions for these scripts are documented inside the files.

## Acknowledgment

This repository uses the official implementation of "Multitrack Music Transformer" (ICASSP 2023).

__Multitrack Music Transformer__<br>
Hao-Wen Dong, Ke Chen, Shlomo Dubnov, Julian McAuley and Taylor Berg-Kirkpatrick<br>
_Proceedings of the IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)_, 2023<br>
[[homepage](https://salu133445.github.io/mmt/)]
[[paper](https://arxiv.org/pdf/2207.06983.pdf)]
[[code](https://github.com/salu133445/mmt)]
[[reviews](https://salu133445.github.io/pdf/mmt-icassp2023-reviews.pdf)]

