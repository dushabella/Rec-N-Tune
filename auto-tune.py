"""
TODO:
read, play, FFT,
(divide)
write
"""

from __future__ import print_function
import scipy.io.wavfile as wavfile
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt
import scales

# scales.generate_freq_table()

fs, data = wavfile.read("input_records/Iza10.wav")
# fs, data = wavfile.read('output_records/record.wav')

print("Sample rate: ", fs)
l_audio = len(data.shape)
print("Channels:", l_audio)
if l_audio == 2:
    data = data.sum(axis=1) / 2
N = data.shape[0]
print ("Complete Samplings N", N)
secs = N / float(fs)
print ("secs", secs)
Ts = 1.0/fs # sampling interval in time
print ("Timestep between samples Ts", Ts)
t = scipy.arange(0, secs, Ts) # time vector as scipy arange field / numpy.ndarray
FFT = abs(scipy.fft(data))
FFT_side = FFT[range(N//2)] # one side FFT range
freqs = scipy.fftpack.fftfreq(data.size, t[1]-t[0])
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
p3 = plt.plot(freqs_side, abs(FFT_side), gray) # plotting the positive fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count single-sided')


plt.show()

# how to generate audio from numpy array:
# https://stackoverflow.com/questions/10357992/how-to-generate-audio-from-a-numpy-array