import librosa
import numpy as np


def correct(self):
    step = int(self.INPUT_SR / 20)
    print('Detected fq\tCorrected fq\tCorrection factor')
    print('--------------------------------------------')
    for x in range(0, len(self.INPUT_WAVE), step):
        # find STFT
        # Match to closest frequency
        # transpose
        # Append to self.OUTPUT_WAVE
        # Return output wave

        y = self.INPUT_WAVE[x:x + step]
        f = __find_stft(y)

        diff_array = [np.abs(note - f) for note in self.NOTES]
        note = np.argmin(diff_array)
        print(f, end='\t')
        print(self.NOTES[note], end='\t')

        self.OUTPUT_WAVE[x:x + step] = self._transpose(y, f, self.NOTES[note])
        # self.OUTPUT_WAVE = np.concatenate(self.OUTPUT_WAVE,self._transpose(y, f, self.NOTES[note]))

    print('-------------------------------------------')
    return librosa.util.normalize(self.OUTPUT_WAVE)




def __find_stft(y, sr):
    """
    Finds STFT (Short Time Fourier Transform).

    :param y: data
    :param sr: sample rate
    :return: frequency with maximum amplitude in the interval

    """

    yD = librosa.stft(y, sr)
    arr = np.argmax(yD, axis=0)
    fq = np.mean(arr)

    return fq


# y, sr = librosa.load("input_records/Iza10.wav")
y, sr = librosa.load("input_records/synth.wav")
find_stft(y, sr)
