import librosa
import matplotlib.pyplot as plt
import numpy as np


# x, sr = librosa.load('input_records/Iza10.wav')
y, sr = librosa.load(librosa.util.example_audio_file())
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

plt.subplot(211)
plt.imshow(pitches[:100, :], aspect="auto", interpolation="nearest", origin="bottom")

plt.subplot(212)
plt.plot(pitches)
plt.show()

print(pitches, magnitudes)

plt.imshow(pitches[:100, :], aspect="auto", interpolation="nearest", origin="bottom")