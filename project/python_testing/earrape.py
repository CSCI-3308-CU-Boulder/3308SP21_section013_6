
# Author: Spencer Stepanek and team 013_6
# CSCI_3308, Photophonic Web-App Project
# Created on 3/9/21

from tones import SINE_WAVE, SAWTOOTH_WAVE
from tones.mixer import Mixer

volume = 0.5

# Set sample rate and volume
mixer = Mixer(44100, volume)

# Create two monophonic tracks that will play simultaneously
# Set initial values for note attack, decay and vibrato frequency
# (these can be changed again at any time, see documentation for tones.Mixer
mixer.create_track(0, SAWTOOTH_WAVE, vibrato_frequency=0.5, vibrato_variance=0.0, attack=0.01, decay=0.1)
mixer.create_track(1, SINE_WAVE, attack=0.01, decay=0.1)
mixer.create_track(2, SINE_WAVE, attack=0.01, decay=0.1)
mixer.create_track(3, SINE_WAVE, vibrato_frequency=0.03, vibrato_variance=0.01, attack=0.01, decay=0.1)

mixer.add_note(0, note='f', octave=4, duration=2.0, endnote='ab')
mixer.add_note(1, note='db', octave=5, duration=2.0, endnote='f')
mixer.add_note(2, note='ab', octave=2, duration=2.0)
mixer.add_note(3, note='ab', octave=3, duration=1.0)

mixer.add_note(3, note='gb', octave=3, duration=1.0)

mixer.add_note(0, note='ab', octave=4, duration=2.0)
mixer.add_note(1, note='f', octave=5, duration=2.0)
mixer.add_note(2, note='db', octave=2, duration=2.0)
mixer.add_note(3, note='gb', octave=3, duration=2.0)

mixer.write_wav('gen.wav')

# Mix all tracks into a single list of samples scaled from 0.0 to 1.0, and
# return the sample list
samples = mixer.mix()

