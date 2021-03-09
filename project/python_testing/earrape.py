
# Author: Spencer Stepanek and team 013_6
# CSCI_3308, Photophonic Web-App Project
# Created on 3/9/21


import pyaudio     #sudo apt-get install python-pyaudio
import numpy as np

p = pyaudio.PyAudio()

volume = 0.06     # range [0.0, 1.0]
fs = 44100       # sampling rate in Hz, int
duration = 1.0   # duration of audio in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play. May repeat with different volume values (if done interactively)
stream.write(volume*samples)

stream.stop_stream()
stream.close()

p.terminate()