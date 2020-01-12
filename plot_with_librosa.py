"""
    Display sound signals with librosa
"""

import matplotlib.pyplot as plt
import librosa
import librosa.display as disp

# shift the pitch
y_sh = librosa.effects.pitch_shift(y, sr, n_steps=-6)


def plotWave(y, sr, y_shifted):
    gray = '#57506D'
    yellow = "#FFC726"

    plt.figure()
    plt.subplot(2, 1, 1)
    disp.waveplot(y, sr=sr, color=gray)
    plt.title('Monophonic waveplot')

    plt.subplot(2, 1, 2)
    disp.waveplot(y, sr=sr)
    disp.waveplot(y_shifted, sr=sr, color=yellow)
    plt.title('Stereo')

    plt.show()


def plotHarmPers(y, sr, y_shifted):
    y_harm, y_perc = librosa.effects.hpss(y)
    plt.subplot(2, 1, 1)
    disp.waveplot(y_harm, sr=sr, alpha=0.25)
    disp.waveplot(y_perc, sr=sr, color='r', alpha=0.5)
    plt.title('Harmonic + Percussive')

    plt.subplot(2, 1, 2)
    y_harm_sh, y_perc_sh = librosa.effects.hpss(y)
    disp.waveplot(y_harm_sh, sr=sr, alpha=0.25)
    disp.waveplot(y_perc_sh, sr=sr, color='r', alpha=0.5)
    plt.title('Harmonic + Percussive (shifted)')
    plt.tight_layout()
    plt.show()


def plotSpec(y, sr):
    plt.figure()
    yD = librosa.stft(y, n_fft=sr)
    disp.specshow(librosa.amplitude_to_db(yD), y_axis='log', x_axis='time')
    plt.title('Power Spectrogram')
    plt.show()


def plotChroma(y, sr):
    plt.figure()
    cD = librosa.feature.chroma_stft(y, n_fft=sr)
    disp.specshow(cD, y_axis='chroma', x_axis='time')
    plt.title('Chromatograph')
    plt.show()


def main():
    y, sr = librosa.load("input_records/Iza10.wav")

    plotWave(y, sr, y_sh)
    # plotHarmPers(y, sr, y_sh)
    # plotSpec(y, sr)
    # plotChroma(y, sr)

if __name__ == "__main__":
    main()