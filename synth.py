"""
    Synthesize a simple sound of a given frequency.
"""
from synthesizer import Player, Synthesizer, Waveform, Writer

player = Player()
player.open_stream()
synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)

# Play A4
player.play_wave(synthesizer.generate_constant_wave(440.0, 1.0))

# Play C major
chord = [261.626,  329.628, 391.996]
player.play_wave(synthesizer.generate_chord(chord, 1.0))

# Play exemplary "almost" chord
# C_4
chord = [270.000,  329.628, 370.000]
player.play_wave(synthesizer.generate_chord(chord, 2.0))

# write
writer = Writer()

chord = [270.000,  329.628, 370.000]
wave = synthesizer.generate_chord(chord, 3.0)
writer.write_wave("output_records/your.wav", wave)