"""
Chris Francis (cfrancis@ucsd.edu)

Script to change instrument of a track in a midi file.

Usage:

python change_instrument.py INPUT_FILE_PATH TRACK_NUMBER INSTRUMENT_NUMBER OUTPUT_FILE_PATH

* INPUT_FILE_PATH: Path to the input midi file
* TRACK_NUMBER: Number of the track to change the instrument of (0-indexed)
* INSTRUMENT_NUMBER: Number of the instrument (MIDI program number) to change to
* OUTPUT_FILE_PATH: Path to the output midi file
"""

import muspy
import sys


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python change_instrument.py INPUT_FILE_PATH TRACK_NUMBER INSTRUMENT_NUMBER OUTPUT_FILE_PATH")
        sys.exit(1)

    input_path = sys.argv[1]
    track_number = int(sys.argv[2])
    instrument_number = int(sys.argv[3])
    output_path = sys.argv[4]

    assert(input_path.endswith(".mid"), "Input file must be a midi file")
    assert(output_path.endswith(".mid"), "Output file must be a midi file")

    midi = muspy.read_midi(input_path, backend='pretty_midi')
    assert(track_number < len(midi.tracks), "Track number out of range")

    midi.tracks[track_number].program = instrument_number
    muspy.write_midi(output_path, midi, backend='pretty_midi')

    # verify the change
    new_midi = muspy.read_midi(output_path, backend='pretty_midi')
    assert(new_midi.tracks[track_number].program == instrument_number, "Instrument change failed")
    