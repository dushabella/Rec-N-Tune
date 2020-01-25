import librosa
import scales
import numpy as np
from typing import List


def correct(in_wave, sample_r: int, scale: List[float]): #->
    """
    Takes chunks of signal of a length "step",
    detects pitches with STFT,
    moves them to the closest frequency of a note.

    :param in_wave: input wave [numpy.darray]
    :param sample_r: sample rate
    :param scale: scale/set of notes
    :return:
    """
    step = int(sample_r / 10)
    print('Detected fq\t Corrected fq\t Correction factor')
    print('--------------------------------------------')
    for x in range(0, len(in_wave), step):
        # find STFT
        # Match to closest frequency
        # transpose
        # Append to self.OUTPUT_WAVE
        # Return output wave

        y = in_wave[x:x + step]
        f = __find_stft(y, sample_r)
        print("f:", f)

        diff_array = [np.abs(note - f) for note in scale]
        note = np.argmin(diff_array)
        print(f, end='\t')
        print(scale[note], end='\t')

    #     OUTPUT_WAVE[x:x + step] = _transpose(y, f, NOTES[note])
    #     # self.OUTPUT_WAVE = np.concatenate(self.OUTPUT_WAVE,self._transpose(y, f, self.NOTES[note]))
    #
    # print('-------------------------------------------')
    # return librosa.util.normalize(OUTPUT_WAVE)


# self.INPUT_WAVE = y
# self.INPUT_SR = sr
# self.SCALE = scale
# self._note = Notes.Notes(scale)
#
# self.NOTES = self._note.getScale()
# self.OUTPUT_WAVE = np.empty(shape=self.INPUT_WAVE.shape)



def __find_stft(y, sr: int) ->float:
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


# y, sr = librosa.load("input_records/Iza10.wav")
y, sr = librosa.load("output_records/synth.wav")

C_Major = scales.C_Major_pentatonic
scale_dict = scales.fit_frequencies(C_Major)

scale = [scale_dict[note] for note in scale_dict]
scale.sort()
print(scale)
scale.sort()

correct(y, sr, scale)