"""
Author: Izabela Dusza
Created on January 2020

    Auto-tune style project for CBSP course.

    Load, record and play .wav file.
    Tune the notes of a recorded file.

    The project is still far away from finish.

    TODO:
        1) Finish a python prototype
            detect_pitches - function which indicates us the pitches and returns:
                                pitch - the pitch values [Hz]
                                pitch_position - the place where the pitch is
                            (https://essentia.upf.edu/reference/std_PitchMelodia.htm)
            spectral_flux, windowing
            shift_pitch() - function for shifting the detected frequency (which is an "almost note") to the note frequency
            reconstruct_sound() - function with stuff like IFFT (Inverse Fast Fourier Transform) to create the .wav file of a corrected signal
        2) Do user-friendly mobile app with usage of the interface from adobe xd graphic design project

"""

import scipy.io.wavfile as wavfile
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt
import scales
import play_sound


"""

"""
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
    Does Fast Fourier Transform on the signal to change the time domain to frequency domain.
    Then, takes the proper data for the further operations (that are not, let's say, "redundant")
    :param data: signal data
    :param N: number of data samples
    :return:
    """
    FFT = scipy.fft(data) #abs(scipy.fft(data))
    print("FFT: ", FFT)
    FFT_side = FFT[range(N//2)] # one side FFT range
    freqs = scipy.fftpack.fftfreq(N, t[1]-t[0])
    print("freqs: ", freqs)
    freqs_side = freqs[range(N//2)] # one side frequency range
    # fft_freqs_side = np.array(freqs_side)

    return FFT, FFT_side, freqs, freqs_side

def frequency_table(sample_len):
    """
    Returns a numpy array that represents a frequencies of the notes
    :param freq_len: amount of frequency samples of recording
    :return res: frequency table of a type 'numpy.ndarray'
    """
    E_Major_pentatonic = ["E", "Fis", "Gis", "B", "Cis"]
    frequencies = scales.generate_freq_table()
    frequencies_of_scale = scales.fit_frequencies(E_Major_pentatonic, frequencies)

    frequencies = sorted(frequencies.items(), key=lambda x: x[1])
    max_frequency = int(frequencies[-1][1])
    # print("last:", frequencies[-1][1])

    frequencies_of_scale = sorted(frequencies_of_scale.items(), key=lambda x: x[1])  # sort ->list

    res = np.zeros(sample_len)
    for element in frequencies_of_scale:
        el = int(element[1])
        el = int(el * sample_len / max_frequency - 1)
        res[el] = 1
    return res

def reconstruct_sound():
    print("chora")
    tx = np.fft.fft(a)
    itx = np.fft.ifft(tx)


def draw(t, data, FFT, FFT_side, freqs, freqs_side, freq_of_notes):
    fig = plt.figure(figsize=[10, 7])
    gray = '#57506D'
    yellow = "#FFC726"

    plt.subplot(2, 1, 1)
    plt.plot(t, data, gray) # plotting the signal
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    # plt.subplot(2, 1, 2)
    # plt.plot(t, freqs, "g") # plotting the signal
    # plt.xlabel('Time')
    # plt.ylabel('Frequency (Hz)')

    # plt.subplot(2, 1, 2)
    # FFT = abs(FFT)
    # p2 = plt.plot(freqs, FFT, "r") # plotting the complete fft spectrum
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Count dbl-sided')

    plt.subplot(2, 1, 2)
    p3 = plt.plot(freqs_side, abs(FFT_side), gray, label = "recorded") # plotting the positive fft spectrum
    gain = np.max(abs(FFT_side))
    print(abs(FFT_side))
    p4 = plt.plot(freqs_side, freq_of_notes*gain/10, yellow, label="Notes") # the plot shows where are the notes
    print( "fr_size", freqs_side.shape)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count single-sided')

    plt.show()

def detectPitch(fs: int, signal):
    """
    Detects pitches in frequency domain signal, using autocorelation tool

    :param fs: sampling frequency
    :param signal: (type of numpy.ndarray) the array which is a "single - sided" frequency representation of a sound
            "single sided" means only a quarter part of a full set of frequencies which you can obtain with FFT
    """

    # input signal visualization
    caribbean = '#00C47F'

    p3 = plt.plot(signal, caribbean, label = "recorded") # plotting the positive fft spectrum
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count single-sided')

    plt.show()


def main():
    fs, data, N, secs, Ts, t = read_wav("input_records/Iza10.wav")
    # fs, data, N, secs, Ts, t = read_wav("output_records/record.wav")

    FFT, FFT_side, freqs, freqs_side = FFT_quarter(data, N, t)

    samples = abs(FFT_side).shape
    samples = str(samples)
    samples = samples[1:-2]
    samples = int(samples)
    print(samples)
    freq_of_notes = frequency_table(samples)

    signal = abs(FFT_side)
    detectPitch(fs, signal)

    # draw(t, data, FFT, FFT_side, freqs, freqs_side, freq_of_notes)

if __name__ == "__main__":
    main()
# how to generate audio from numpy array:
# https://stackoverflow.com/questions/10357992/how-to-generate-audio-from-a-numpy-array
