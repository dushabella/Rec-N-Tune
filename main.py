"""
Author: Izabela Dusza
Created on January 2020

    Auto-tune style project for CBSP course.

    Load, record and play .wav file.
    Tune the notes of a recorded file.

    The project is still far away from finish.

    TODO:
        1) Finish a python prototype
            find_periods - compute periods per sewuence for the purposes of finding pitches
            detect_pitches - function which indicates us the pitches and returns:
                                pitch - the pitch values [Hz]
                                pitch_position - the place where the pitch is
                            (https://essentia.upf.edu/reference/std_PitchMelodia.htm)
            spectral_flux, windowing
            shift_pitch() - function for shifting the detected frequency (which is an "almost note") to the note frequency
            reconstruct_sound() - function with stuff like IFFT (Inverse Fast Fourier Transform) to create the .wav file of a corrected signal
        2) Do user-friendly mobile app with usage of the interface from adobe xd graphic design project

"""

