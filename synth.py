"""
    Synthesize a simple sound of a given frequency.
"""
from synthesizer import Player, Synthesizer, Waveform, Writer
import scales

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

chord = [170.000,  329.628, 570.000]
wave = synthesizer.generate_chord(chord, 3.0)
writer.write_wave("output_records/synth.wav", wave)

# # generate the sound of a full scale of notes
# scale_dict = scales.fit_frequencies(scales.full_scale)
# scale = [scale_dict[note] for note in scale_dict]
# scale.sort()
# wave = synthesizer.generate_chord(scale, 3.0)
# writer.write_wave("records/scales/full_scale.wav", wave)

# # generate the sound for C major pentatonic
# scale_dict = scales.fit_frequencies(scales.C_Major_pentatonic)
# scale = [scale_dict[note] for note in scale_dict]
# scale.sort()
# wave = synthesizer.generate_chord(scale, 3.0)
# writer.write_wave("records/scales/C_major.wav", wave)

# # generate the sound for D major pentatonic
# scale_dict = scales.fit_frequencies(scales.D_Major_pentatonic)
# scale = [scale_dict[note] for note in scale_dict]
# scale.sort()
# wave = synthesizer.generate_chord(scale, 3.0)
# writer.write_wave("records/scales/D_major.wav", wave)

# # generate the sound for E major pentatonic
# scale_dict = scales.fit_frequencies(scales.E_Major_pentatonic)
# scale = [scale_dict[note] for note in scale_dict]
# scale.sort()
# wave = synthesizer.generate_chord(scale, 3.0)
# writer.write_wave("records/scales/E_major.wav", wave)