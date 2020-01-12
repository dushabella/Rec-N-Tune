"""
    Find pitches using autocorrelation.
"""

%matplotlib inline
import numpy, scipy, matplotlib.pyplot as plt, IPython.display as ipd
import librosa, librosa.display
import stanford_mir; stanford_mir.init()

x, sr = librosa.load('input_records/iza10.wav')
ipd.Audio(x, rate=sr)