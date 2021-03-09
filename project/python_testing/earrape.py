
# Author: Spencer Stepanek and team 013_6
# CSCI_3308, Photophonic Web-App Project
# Created on 3/9/21


import math        #import needed modules
import pyaudio     #sudo apt-get install python-pyaudio

PyAudio = pyaudio.PyAudio     #initialize pyaudio
BITRATE = 5000     #number of frames per second/frameset.
FREQUENCY = 10000     #Hz, waves per second, 261.63=C4-note.
LENGTH = 5    #seconds to play sound

if FREQUENCY > BITRATE:
   BITRATE = FREQUENCY+100
NUMBEROFFRAMES = int(BITRATE * LENGTH)

RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''

#generating waves
for x in range(NUMBEROFFRAMES):
     WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))

for x in range(RESTFRAMES):
    WAVEDATA = WAVEDATA+chr(128)

print(WAVEDATA)

p = PyAudio()

stream = p.open(format = p.get_format_from_width(1),channels = 2, rate = BITRATE,output = True)

stream.write(WAVEDATA)
stream.stop_stream()
stream.close()
p.terminate()