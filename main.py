"""
Author: Izabela Dusza
Created on January 2020

    Auto-tune style project for CBSP course.

    Load, record and visualize .wav file.
    Tune the notes of a recorded file.


"""

import scipy.io.wavfile as wavfile
import scipy.fftpack
from matplotlib import pyplot as plt
import scales
import autotune
import librosa



def read_wav(file_name: str):
    """
    Reads .wav file and prints some infos.
    If the file contains data from two signals,
    the average value is taken.

    :param file_name:

    :return fs: - Sample rate (int)
    :return data: - signal data (numpy.ndarray)
    :return N: - number of data samples
    :return secs: - duration time
    """
    fs, data = wavfile.read(file_name)

    print("Sample rate: ", fs)

    l_audio = len(data.shape)  # check if there's 1 or 2 channels
    print("Channels:", l_audio)
    if l_audio == 2:
        data = data.sum(axis=1) / 2

    N = len(data)
    print("Complete samples: ", N)
    print(data.size)

    secs = N / float(fs)
    print("Duration time: ", secs)

    Ts = 1.0 / fs  # sampling interval
    print("Timestep between samples: ", Ts)

    t = scipy.arange(0, secs, Ts)  # time vector as scipy arange field / numpy.ndarray

    return fs, data, N, secs, Ts, t


def FFT_quarter(data, N: int, t):
    """
    Makes Fast Fourier Transform on the signal to change the time domain to frequency domain.
    Then, takes the proper data for the further operations (that are not, let's say, "redundant")
    :param data: signal data
    :param N: number of data samples
    :return:
    """
    FFT = scipy.fft(data)
    FFT_side = FFT[range(N//2)] # one side FFT range
    freqs = scipy.fftpack.fftfreq(N, t[1]-t[0])
    freqs_side = freqs[range(N//2)] # one side frequency range

    return FFT, FFT_side, freqs, freqs_side


def draw(t, data, FFT, FFT_side, freqs, freqs_side, freqs_side_scale, FFT_side_scale):
    fig = plt.figure(figsize=[10, 7])
    gray = '#57506D'
    yellow = "#FFC726"
    caribbean = '#00C47F'

    plt.subplot(2, 1, 1)
    plt.plot(t, data, gray) # plotting the signal
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    # plt.subplot(2, 1, 2)
    # plt.plot(t, freqs, "g") # plotting the signal
    # plt.xlabel('Time')
    # plt.ylabel('Frequency (Hz)')
    #
    # plt.subplot(2, 1, 2)
    # FFT = abs(FFT)
    # p2 = plt.plot(freqs, FFT, "r") # plotting the complete fft spectrum
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Count dbl-sided')

    plt.subplot(2, 1, 2)
    p3 = plt.plot(freqs_side_scale, abs(FFT_side_scale), yellow, label="Notes") # showing where are the notes
    p4 = plt.plot(freqs_side, abs(FFT_side), gray, label="recorded") # plotting the positive fft spectrum
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count single-sided')

    plt.show()


def main():
    # _________________________________PARAMETERS__________________________________

    # NAME OF A FILE YOU WANT TO TUNE
    # input_filename = "song_records/Alvaro1.wav" # NAME OF A FILE YOU WANT TO TUNE
    input_filename = "records/synth.wav"

    # output_filename = "records/corrected_alvaro.wav"
    output_filename = "records/corrected_synth.wav"

    # _____________________________________________________________________________

    # prepare a full scale for plotting
    fs_s, data_s, N_s, secs_s, Ts_s, t_s = read_wav("records/scales/full_scale.wav") # scale frequencies generator
    FFT_scale, FFT_side_scale, freqs_scale, freqs_side_scale = FFT_quarter(data_s, N_s, t_s)  # scale frequencies generator


    # visualize input data
    print("Visualizing input...")
    fs, data, N, secs, Ts, t = read_wav(input_filename)
    FFT, FFT_side, freqs, freqs_side = FFT_quarter(data, N, t)
    draw(t, data, FFT, FFT_side, freqs, freqs_side, freqs_side_scale, FFT_side_scale)
    print()


    # auto-tune
    y, sr = librosa.load(input_filename)

    chosen_scale = scales.C_Major_pentatonic
    scale_dict = scales.fit_frequencies(chosen_scale)

    scale = [scale_dict[note] for note in scale_dict]
    scale.sort()
    print("_______Chosen scale_______")
    print(scale)

    corrected_y = autotune.correct(y, sr, scale)
    autotune.save_wav(output_filename, corrected_y, sr)
    print()


    # visualize output data
    print("Visualizing output...")
    fs, data, N, secs, Ts, t = read_wav(output_filename)
    FFT, FFT_side, freqs, freqs_side = FFT_quarter(data, N, t)
    draw(t, data, FFT, FFT_side, freqs, freqs_side, freqs_side_scale, FFT_side_scale)


if __name__ == "__main__":
    main()