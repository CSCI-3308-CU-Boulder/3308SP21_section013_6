
# Author: Spencer Stepanek and team 013_6
# CSCI_3308, Photophonic Web-App Project
# Created on 3/9/21


from pippi import dsp

sound1 = dsp.read('sound1.wav')
sound2 = dsp.read('sound2.flac')

# Mix two sounds
both = sound1 & sound2

# Apply a skewed hann Wavetable as an envelope to a sound
enveloped = sound * dsp.win('hann').skewed(0.6)

# Or just a sine envelope via a shortcut method on the `SoundBuffer`
enveloped = sound.env('sine')

# Synthesize a 10 second graincloud from the sound,
# with grain length modulating between 20ms and 2s
# over a triangle shaped curve.
cloudy = enveloped.cloud(10, grainlength=dsp.win('tri', dsp.MS*20, 2))
