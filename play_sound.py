"""
Author: Izabela Dusza
Created on January 2020

    Play .wav file

"""

from pydub import AudioSegment
from pydub.playback import play

def play_wav(file_name: str) ->None:
    sound = AudioSegment.from_wav(file_name)
    play(sound)

def main():
    play_wav('input_records/Iza9_total_fail.wav')

if __name__ == "__main__":
    main()