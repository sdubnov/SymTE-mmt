"""
Chris Francis (cfrancis@ucsd.edu)

Script to split a midi file into 2 separate midi files, each containing a single track.

Usage:

python split_midi.py INPUT_FILE OUTPUT_FILE_1 OUTPUT_FILE_2 [OUTPUT_FILE_3]

* INPUT_FILE: Path to the input midi file
* OUTPUT_FILE_1: Path to the first output midi file (track 1)
* OUTPUT_FILE_2: Path to the second output midi file (track 2)
* OUTPUT_FILE_3: Path to the third output midi file (both tracks)
"""
import muspy
import sys

if __name__ == "__main__":
    if len(sys.argv) not in [4, 5]:
        print("Usage: python split_midi.py INPUT_FILE OUTPUT_FILE_1 OUTPUT_FILE_2 [OUTPUT_FILE_3]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path_1 = sys.argv[2]
    output_path_2 = sys.argv[3]
    output_path_3 = sys.argv[4] if len(sys.argv) == 5 else None
    
    assert(input_path.endswith(".mid"), "Input file must be a midi file")
    assert(output_path_1.endswith(".mid"), "Output file 1 must be a midi file")
    assert(output_path_2.endswith(".mid"), "Output file 2 must be a midi file")
    if output_path_3 is not None:
        assert(output_path_3.endswith(".mid"), "Output file 3 must be a midi file")

    music = muspy.read_midi(input_path, backend='pretty_midi')
    
    xy = music.copy()
    xy.tracks = [music.tracks[0].copy(), music.tracks[1].copy()]

    x = music.copy()
    x.tracks = [music.tracks[0].copy()]

    y = music.copy()
    y.tracks = [music.tracks[1].copy()] 

    muspy.write_midi(output_path_1, x, backend='pretty_midi')
    muspy.write_midi(output_path_2, y, backend='pretty_midi')
    if output_path_3 is not None:
        muspy.write_midi(output_path_3, xy, backend='pretty_midi')