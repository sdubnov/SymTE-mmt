"""
Chris Francis (cfrancis@ucsd.edu)

Script to combine 2 midi tracks into a single midi file.

Usage:

python combine_midi.py INPUT_FILE_1 INPUT_FILE_2 OUTPUT_FILE_PATH

* INPUT_FILE_1: Path to the first midi file
* INPUT_FILE_2: Path to the second midi file
* OUTPUT_FILE_PATH: Path to the output midi file
"""

import muspy
import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python combine_midi.py INPUT_FILE_1 INPUT_FILE_2 OUTPUT_FILE_PATH")
        sys.exit(1)

    input_path_1 = sys.argv[1]
    input_path_2 = sys.argv[2]
    output_path = sys.argv[3]

    assert(input_path_1.endswith(".mid"), "Input file 1 must be a midi file")
    assert(input_path_2.endswith(".mid"), "Input file 2 must be a midi file")
    assert(output_path.endswith(".mid"), "Output file must be a midi file")

    track_1 = muspy.read_midi(input_path_1, backend='pretty_midi')
    track_2 = muspy.read_midi(input_path_2, backend='pretty_midi')
    assert(len(track_1.tracks) == 1, "Input file 1 must contain a single track")
    assert(len(track_2.tracks) == 1, "Input file 2 must contain a single track")
    track_1.tracks.extend(track_2.tracks)
    muspy.write_midi(output_path, track_1, backend='pretty_midi')

