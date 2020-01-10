import sounddevice as sd
from scipy.io.wavfile import write

def record(fs: int, seconds: float, name: str) ->None:
    """
    Record and save the sound.

    Function parameters:
        fs - Sample rate
        seconds - Duration of recording
        name - Name of output record
    """
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    print("Recording...")
    sd.wait()  # Wait until recording is finished
    print("Record is finished")
    write('output_records/' + name + '.wav', fs, myrecording)  # Save as WAV file

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

record(fs, seconds, "record")

