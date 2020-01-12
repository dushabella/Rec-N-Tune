"""
Author: Izabela Dusza
Created on January 2020

    Record .wav file

"""

import sounddevice as sd
from scipy.io.wavfile import write

def record(fs: int, seconds: float, name: str) ->None:
    """
    Record the sound and save it in a .wav file.

    :param fs: Sample rate
    :param seconds: Duration of recording
    :param name: Name of output record
    """
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    print("Recording...")
    sd.wait()  # Wait until recording is finished
    print("Record is finished")
    write('output_records/' + name + '.wav', fs, myrecording)  # Save as WAV file

def main():
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    record(fs, seconds, "record")

if __name__ == "__main__":
    main()