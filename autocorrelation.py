"""
    Find pitches using autocorrelation.

    The following code is based on https://musicinformationretrieval.com/autocorrelation.html
"""

# matplotlib inline
import numpy as np
import scipy
import matplotlib.pyplot as plt
import IPython.display as ipd
import librosa, librosa.display
# import stanford_mir, stanford_mir.init()

x, sr = librosa.load('input_records/Iza10.wav')
ipd.Audio(x, rate=sr)


# plt.figure(figsize=(14, 5))
# librosa.display.waveplot(x, sr)
# plt.xlabel('Time')
# plt.ylabel('Amplitude')
# plt.title('Waveplot')
# plt.show()

# # autocorrelation produces a symmetric signal, so we only care about the "right half"
# r = np.correlate(x, x, mode='full')[len(x)-1:]
# print(x.shape, r.shape)

r = librosa.autocorrelate(x, max_size=None)
plt.figure(figsize=(14, 5))
plt.plot(r)#[:200])
plt.title("Autocorrelation")
plt.show()

# The autocorrelation always has a maximum at zero, i.e. zero lag. We want to identify  \
# the maximum outside of the peak centered at zero. Therefore, we might choose only to  \
# search within a range of reasonable pitches:
midi_hi = 120.0
midi_lo = 12.0
f_hi = librosa.midi_to_hz(midi_hi)
f_lo = librosa.midi_to_hz(midi_lo)
t_lo = sr/f_hi
t_hi = sr/f_lo

print(f_lo, f_hi)
print(t_lo, t_hi)

# Set invalid pitch candidates to zero:
r[:int(t_lo)] = 0
r[int(t_hi):] = 0
plt.figure(figsize=(14, 5))
plt.plot(r)#[:1400])
plt.show()

# find the location of the maximum
t_max = r.argmax()
print("Maximum pitch location: ", t_max)
f_max = r.max()
print("Maximum pitch: ", f_max)

# Finally, estimate the pitch in Hertz:
float(sr)/t_max

# Indeed, that is very close to the true frequency of C6:
librosa.midi_to_hz(84)
