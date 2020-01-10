from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_wav('input_records/Iza9_total_fail.wav')
play(sound)