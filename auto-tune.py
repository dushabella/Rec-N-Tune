import scipy.io.wavfile as wavfile
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt
import scales

def read_wav(file_name: str):
    """
    Read .wav file and print some infos.
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

    return fs, data, N, secs, Ts

fs, data, N, secs, Ts = read_wav("input_records/Iza10.wav")
# fs, data, N, secs, Ts = read_wav("output_records/record.wav")


t = scipy.arange(0, secs, Ts) # time vector as scipy arange field / numpy.ndarray

FFT = abs(scipy.fft(data))
print("FFT: ", FFT)

FFT_side = FFT[range(N//2)] # one side FFT range
freqs = scipy.fftpack.fftfreq(N, t[1]-t[0])
fft_freqs = np.array(freqs)
freqs_side = freqs[range(N//2)] # one side frequency range
fft_freqs_side = np.array(freqs_side)

fig = plt.figure(figsize=[10, 7])
gray = '#57506D'

plt.subplot(2, 1, 1)
plt.plot(t, data, gray) # plotting the signal
plt.xlabel('Time')
plt.ylabel('Amplitude')

plt.subplot(2, 1, 2)
p2 = plt.plot(freqs, FFT, "r") # plotting the complete fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count dbl-sided')

# plt.subplot(2, 1, 2)
# p3 = plt.plot(freqs_side, abs(FFT_side), gray) # plotting the positive fft spectrum
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Count single-sided')

plt.show()

def main():
    E_Major_pentatonic = ["E", "Fis", "Gis", "B", "Cis"]
    frequencies = scales.generate_freq_table()
    scales.fit_frequencies(E_Major_pentatonic, frequencies)

if __name__ == "__main__":
    main()
# how to generate audio from numpy array:
# https://stackoverflow.com/questions/10357992/how-to-generate-audio-from-a-numpy-array