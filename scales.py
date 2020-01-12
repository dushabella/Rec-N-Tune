"""
Author: Izabela Dusza
Created on January 2020

    This script generates the frequencies of a given scale.
    Each scale contains of some notes. Any note has a fundamental frequency and its multifications.
    
    Exemplary scales (for singing):

        C Major pentatonic (pentatonika C dur): C D E G A
        D Major pentatonic (pentatonika D dur): D E F# A B
        E Major pentatonic (pentatonika E dur): E F# G# B C#

    https://www.basicmusictheory.com/d-major-pentatonic-scale
"""

from typing import Dict, List

# here are defined exemplary scales
C_Major_pentatonic = ["C", "D", "E", "G", "A"]
D_Major_pentatonic = ["D", "E", "Fis", "A", "B"]
E_Major_pentatonic = ["E", "Fis", "Gis", "B", "Cis"]

def fit_frequencies(scale: List[str], note_frequencies: Dict) ->Dict:
    """
    Fit the frequencies of a given notes to the notes that belongs to a chosen scale.
    """
    result = {}
    for note in scale:
        for key in note_frequencies:
            if note + "_" in key:
                # print(key)
                result[key] = note_frequencies[key]
        print()

    # result = sorted(result.items(), key=lambda x: x[1]) #sort ->list
    return(result)

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

            # print(note_hlpr + ": ", end=" ")
            # print(notes[note_hlpr])
            k+=1

        print()
        i += 1
    # notes = sorted(notes.items(), key=lambda x: x[1])
    # print(notes)
    return(notes)


def main():
    frequencies = generate_freq_table()
    fit_frequencies(E_Major_pentatonic, frequencies)

if __name__ == "__main__":
    main()