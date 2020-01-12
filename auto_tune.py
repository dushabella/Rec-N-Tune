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

    print(type(fs))
    print(type(signal))

def find_peaks(signal, fs, max_hz=950, min_hz=75, analysis_win_ms=40, max_change=1.005, min_change=0.995):
    """
    Find sample indices of peaks in time-domain signal
    :param max_hz: maximum measured fundamental frequency
    :param min_hz: minimum measured fundamental frequency
    :param analysis_win_ms: window size used for autocorrelation analysis
    :param max_change: restrict periodicity to not increase by more than this ratio from the mean
    :param min_change: restrict periodicity to not decrease by more than this ratio from the mean
    :return: peak indices
    """
    N = len(signal)
    min_period = fs // max_hz
    max_period = fs // min_hz

    # compute pitch periodicity
    sequence = int(analysis_win_ms / 1000 * fs)  # analysis sequence length in samples
    periods = compute_periods_per_sequence(signal, sequence, min_period, max_period)

    # simple hack to avoid octave error: assume that the pitch should not vary much, restrict range
    mean_period = np.mean(periods)
    max_period = int(mean_period * 1.1)
    min_period = int(mean_period * 0.9)
    periods = compute_periods_per_sequence(signal, sequence, min_period, max_period)

    # find the peaks
    peaks = [np.argmax(signal[:int(periods[0]*1.1)])]
    while True:
        prev = peaks[-1]
        idx = prev // sequence  # current autocorrelation analysis window
        if prev + int(periods[idx] * max_change) >= N:
            break
        # find maximum near expected location
        peaks.append(prev + int(periods[idx] * min_change) +
                np.argmax(signal[prev + int(periods[idx] * min_change): prev + int(periods[idx] * max_change)]))
    return np.array(peaks)


def compute_periods_per_sequence(signal, sequence, min_period, max_period):
    """
    Computes periodicity of a time-domain signal using autocorrelation
    :param sequence: analysis window length in samples. Computes one periodicity value per window
    :param min_period: smallest allowed periodicity
    :param max_period: largest allowed periodicity
    :return: list of measured periods in windows across the signal
    """
    offset = 0  # current sample offset
    periods = []  # period length of each analysis sequence

    while offset < N:
        fourier = fft(signal[offset: offset + sequence])
        fourier[0] = 0  # remove DC component
        autoc = ifft(fourier * np.conj(fourier)).real
        autoc_peak = min_period + np.argmax(autoc[min_period: max_period])
        periods.append(autoc_peak)
        offset += sequence
    return periods


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