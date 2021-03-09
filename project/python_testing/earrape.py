
# Author: Spencer Stepanek and team 013_6
# CSCI_3308, Photophonic Web-App Project
# Created on 3/9/21

from tones import SINE_WAVE, SAWTOOTH_WAVE
from tones.mixer import Mixer

# Create mixer, set sample rate and amplitude
mixer = Mixer(44100, 0.5)

# Create two monophonic tracks that will play simultaneously
# Set initial values for note attack, decay and vibrato frequency
# (these can be changed again at any time, see documentation for tones.Mixer
mixer.create_track(0, SAWTOOTH_WAVE, vibrato_frequency=0.5, vibrato_variance=0.0, attack=0.01, decay=0.1)
mixer.create_track(1, SINE_WAVE, attack=0.01, decay=0.1)

# Add a 1-second tone on track 0, slide pitch from c# to f#)
mixer.add_note(0, note='f', octave=4, duration=2.0, endnote='ab')

# Add a 1-second tone on track 1, slide pitch from f# to g#)
mixer.add_note(1, note='db', octave=5, duration=2.0, endnote='f')


mixer.add_note(0, note='ab', octave=4, duration=2.0)
mixer.add_note(1, note='f', octave=5, duration=2.0)

# Mix all tracks into a single list of samples and write to .wav file
mixer.write_wav('tones.wav')

# Mix all tracks into a single list of samples scaled from 0.0 to 1.0, and
# return the sample list
samples = mixer.mix()

