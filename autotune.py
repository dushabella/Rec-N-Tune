import librosa
import numpy as np
import math
import scales
from typing import List


def correct(in_wave, sample_r: int, scale: List[float]):
    """
    Takes chunks of signal of a length "step",
    detects pitches with STFT,
    moves them to the closest frequency of a note.

    :param in_wave: input wave [numpy.darray]
    :param sample_r: sample rate
    :param scale: scale/set of notes
    :return: output wave
    """
    step = int(sample_r / 10)
    print(in_wave)
    print('__________________________________________________________________')
    print('Detected frequency \t | \t Closest frequency \t | \t Correction')
    print('__________________________________________________________________')
    for x in range(0, len(in_wave), step):

        # find STFT
        y = in_wave[x:x + step]
        f = _find_stft(y, sample_r)
        print("f:", f, end='\t')

        # create the array of differences between "almost note" and "note" \
        # and match to closest frequency
        diff_array = [np.abs(note - f) for note in scale]
        note = np.argmin(diff_array)
        print(scale[note], end='\t')

        # shift
        out_wave = np.empty(shape=in_wave.shape)
        out_wave[x:x + step] = _shift(y, sample_r, f, scale[note])

    return librosa.util.normalize(out_wave)


def _find_stft(y, sr: int) ->float:
    """
    Finds STFT (Short Time Fourier Transform).

    :param y: data [numpy.darray]
    :param sr: sample rate
    :return: frequency with maximum amplitude in the interval
    """

    yD = librosa.stft(y, sr)
    arr = np.argmax(yD, axis=0)
    fq = np.mean(arr)

    return fq


def _shift(y, sr: int, f0: float, f: float):
    """
    Shift the signal
    :param y: data [numpy.darray]
    :param sr: sample rate
    :param f0: old frequency
    :param f: new frequency
    :return:
    """
    # Calculate the steps to be shifted based on the old and new frequencies
    steps = _step(f0, f)
    print(steps)
    yT = librosa.effects.pitch_shift(y, sr, steps)

    return yT


def _step(f0: float, f: float):
    """
    Counts steps for shifting
    https://en.wikipedia.org/wiki/Semitone
    https://pl.wikipedia.org/wiki/P%C3%B3%C5%82ton

    :param f0: old frequency
    :param f: new frequency
    :return: How many (fractional) half-steps to shift y
    """
    semitones = 12 # number of semitones in octave

    if int(f0) == 0:
        return f0
    res = semitones * math.log(f / f0, 2)

    # base = math.pow(2, 1.0 / semitones)
    # if int(f0) == 0:
    #     return f0
    # res = math.log(f / f0, base)

    return res


def save_wav(file_name: str, signal, sr: int):
    librosa.output.write_wav(file_name, signal, sr)

def main():
    y, sr = librosa.load("song_records/Alvaro1.wav")
    # y, sr = librosa.load("records/synth.wav")

    chosen_scale = scales.C_Major_pentatonic
    scale_dict = scales.fit_frequencies(chosen_scale)

    scale = [scale_dict[note] for note in scale_dict]
    scale.sort()
    print(scale)

    corrected_y = correct(y, sr, scale)

    save_wav("records/corrected_alvaro.wav", corrected_y, sr)
    # save_wav("records/corrected_synth.wav", corrected_y, sr)

if __name__ == "__main__":
    main()