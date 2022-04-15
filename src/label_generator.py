import argparse
import os
import vad


def save_to_file(speech_intervals, speech_labels, filename):
    if len(speech_intervals) != len(speech_labels):
        print(f'Warning: intervals and labels are not the same length. Still writing to {filename} but you have to re-label it later')
        print('-' * 5)
    with open(filename, 'w') as f:
        for i, l in zip(speech_intervals, speech_labels):
            f.write(f'{i[0]}\t{i[1]}\t{l}\n')


def get_parser():
    parser = argparse.ArgumentParser(
        description='Analyze input wave-file and save detected speech interval to text file according to given format')
    parser.add_argument('input_wavs', metavar='INPUT_WAVES',
                        help='the full path to input wave file/directory')
    parser.add_argument('input_labels', metavar='INPUT_LABELS',
                        help='the full path to input labels text file')
    parser.add_argument('--aggressive', '-a', type=int, metavar='AGGRESSIVE', default=3, choices=range(4),
                        help='the aggressiveness of the VAD algorithm (0-3)')
    parser.add_argument('--sil', '-s', action='store_true', help='add sil labels')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = get_parser()

    with open(args.input_labels, 'r') as fp:
        if os.path.isdir(args.input_wavs):
            input_wavs = [os.path.join(args.input_wavs, f) for f in os.listdir(args.input_wavs) if f.endswith('.wav')]
            input_wavs.sort()
            lines = fp.readlines()
            assert len(input_wavs) == len(lines), 'Number of input files and labels must be equal'
            for wav, label in zip(input_wavs, lines):
                output_path = wav.replace('.wav', '.txt')
                intervals = vad.detect_voice(wav, args.aggressive)
                labels = label.strip().split()
                save_to_file(intervals, labels, output_path)
        elif os.path.isfile(args.input_wavs):
            output_path = args.input_wavs.replace('.wav', '.txt')
            intervals = vad.detect_voice(args.input_wavs, args.aggressive)
            labels = fp.readlines()[0].strip().split()
            save_to_file(intervals, labels, output_path)
