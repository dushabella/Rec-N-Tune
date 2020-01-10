from typing import Dict

""""

    Most popular scales for singing:

        C Major pentatonic (pentatonika C dur): C D E G A
        D Major pentatonic (pentatonika D dur): D E F# A H
        E Major pentatonic (pentatonika E dur): E F# G# B C#

    https://www.basicmusictheory.com/d-major-pentatonic-scale

"""

def generate_freq_table() ->Dict:
    """
    Generate the harmonics of 9 possible sets of notes ("octaves")

    https://pages.mtu.edu/~suits/notefreqs.html

    "Middle C" is C4
    """
    possible_notes = ["C", "Cis", "D", "Dis", "E", "F", "Fis", "G", "Gis", "A", "Ais", "B"]
    temp_freq = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87]
    notes = {} # notes[note] = frequency
    i = 0
    for i in range(9):
        k = 0

        for note in possible_notes:
            note_hlpr = note + "_" + str(i)

            if i == 0:
                notes[note_hlpr] = temp_freq[k]
            else:
                notes[note_hlpr] = temp_freq[k] * 2
            temp_freq[k] = notes[note_hlpr]

            print(note_hlpr + ": ", end=" ")
            print(notes[note_hlpr])
            k+=1

        print()
        i += 1
    return(notes)

# # 1:
# notes["C"] = 32.70
# notes["C#"] = 34.65
# notes["D"] = 36.71
# notes["D#"] = 38.89
# notes["E"] = 41.20
# notes["F"] = 43.65
# notes["F#"] = 46.25
# notes["G"] = 49.00
# notes["G#"] = 51.91
# notes["A"] = 55.00
# notes["A#"] = 58.27
# notes["B"] = 61.74
#
# # 4 (middle):
# notes["C_4"] = 261.6
# notes["C#_4"] = 277.2
# notes["D_4"] = 293.7
# notes["D#_4"] = 311.1
# notes["E_4"] = 329.6
# notes["F_4"] = 349.2
# notes["F#_4"] = 370.0
# notes["G_4"] = 392.0
# notes["G#_4"] = 415.3
# notes["A_4"] = 440.0
# notes["A#_4"] = 466.2
# notes["B_4"] = 493.9

generate_freq_table()