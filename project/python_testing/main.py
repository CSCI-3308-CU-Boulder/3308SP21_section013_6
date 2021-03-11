
#--------------------------------------------------------
#
#
# Author: Spencer Stepanek and team 013_6
# CSCI_3308, Photophonic Web-App Project
# Created on 2/16/21
#
#
# Tones Docs: https://github.com/eriknyquist/tones
# OpenCV Docs: https://docs.opencv.org/master/index.html
#
#
#--------------------------------------------------------



import numpy as np
import cv2
from tones import SINE_WAVE, SAWTOOTH_WAVE, TRIANGLE_WAVE, SQUARE_WAVE
from tones.mixer import Mixer
import pyaudio
import wave

#-----------< IMAGE GLOBALS >-----------#


show = 0
image_selected = 2

# [ [name, path, pixelData], ... ]
image_pool =   [
                ['fabio', 'fabio.jpg'],
                ['lenna', 'lenna.png']
                                       ]

img = image_pool[image_selected - 1]


#-----------< AUDIO GLOBALS >-----------#


volume = 0.1
duration = 5

# [ [ color, synth, attack, decay, vibrato_frequency, vibrato_variance, octave, pitch_1], ... ]
colorSynths = [
    [ 'red', SAWTOOTH_WAVE, 1.0, 1.0, 0.0, 0.0, 4, 'f'],
    [ 'blue', SINE_WAVE, 1.0, 1.0, 0.0, 0.0, 5, 'a'],
    [ 'green', TRIANGLE_WAVE, 1.0, 1.0, 0.0, 0.0, 4, 'e'],
    [ 'value', SQUARE_WAVE, 1.0, 1.0, 0.0, 0.0, 4, 'd'],
    [ 'alpha', SAWTOOTH_WAVE, 1.0, 1.0, 0.0, 0.0, 4, 'bb'],
    ]


#----------------< IMAGE ANALYSIS DEFINITIONS >----------------#


def getChannels(img):
    return len(img[0])

def isgray(imgpath):
    image = cv2.imread(imgpath)
    if len(image.shape) < 3: return True
    if image.shape[2]  == 1: return True
    b,g,r = image[:,:,0], image[:,:,1], image[:,:,2]
    if (b==g).all() and (b==r).all(): return True
    return False

def analyze_image(name, image, path):

    retStats = [] # return stats

    if isgray(path):
        print("\n----- Analyzing {} in grayscale -----".format(name))
        mean = np.mean(image)
        max = np.max(image)
        min = np.min(image)
        print("Average value: {:.2f}".format(mean))
        print("Max value: {:.2f}".format(max))
        print("Min value: {:.2f}".format(min))
        print("Range of value: {:.2f}\n".format(max - min))
        retStats.append([ 'gray', mean, (max-min) ])
    else:
        print("\n----- Analyzing {} in BGR color -----".format(name))
        blue = []
        green = []
        red = []
        count = 0
        pixel_sums = []
        for row in image:
            for pixel in row:
                count += 1
                blue.append(pixel[0])
                green.append(pixel[1])
                red.append(pixel[2])
                pixel_sums.append( ( (pixel[0]/3) + (pixel[1]/3) + (pixel[2]/3) ) )

        for color in [ [blue, "blue"], [green, "green"], [red, "red"] ]:
            mean = np.mean(color[0])
            max = np.max(color[0])
            min = np.min(color[0])
            print("Average {}: {:.2f}".format(color[1], mean))
            print("Max {}: {:.2f}".format(color[1], max))
            print("Min {}: {:.2f}".format(color[1], min))
            print("Range {}: {:.2f}\n".format(color[1], (max - min)) )

            retStats.append([color[1], mean, (max - min)])



        avg_color = [np.sum(blue) / count, np.sum(green) / count, np.sum(red) / count]
        print("Average color value: [{:.2f}, {:.2f}, {:.2f}]".format(avg_color[0], avg_color[1], avg_color[2]))
        print("Range of color: {:.2f}".format( (np.max(pixel_sums)-np.min(pixel_sums)) )) # (a ratio of difference between colors)

        mean = np.mean(image)
        max = np.max(image)
        min = np.min(image)

        print("Average shade value: {:.2f}".format(mean))
        print("Max shade value: {:.2f}".format(max))
        print("Min shade value: {:.2f}".format(min))
        print("Range of shade value: {:.2f}\n".format(max-min))

        retStats.append([ 'shade', mean, (max-min) ])

    return retStats


#----------------< AUDIO GENERATION DEFINITIONS >----------------#


def initColorSynth( id, color, synth, attack, decay, v_f, v_v, octave, pitch_1 ):

    print(color + " tones being generated...")
    mixer.create_track(id, synth, vibrato_frequency=v_f, vibrato_variance=v_v, attack=attack, decay=decay)

    mixer.add_note(id, note=pitch_1, octave=octave, duration=duration)


#----------------< IMAGE PROCESSING >----------------#


# [ [name, path, pixelData], ... ]
img.append( cv2.imread(img[1]) )

# [ [attribute, mean, range, ...]
imgAnal = analyze_image(img[0], img[2], img[1])
print("Image stats ([attribute, mean, range, ...]):\n {}\n".format(imgAnal))

if show:
    cv2.imshow(img[1], img[2])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#----------------< AUDIO GENERATION >----------------#


mixer = Mixer(44100, volume)

# [ [ color, synth, attack, decay, vibrato_frequency, vibrato_variance, octave, pitch_1], ... ]

if isgray(img[1]): # only get value synth
    rs = colorSynths[3]
    initColorSynth(0, rs[0], rs[1], rs[2], rs[3], rs[4], rs[5], rs[6], rs[7])

    # initColorSynth(0, rs[0], rs[1], rs[2] * (255 - mean), rs[3], rs[4], rs[5], rs[6], rs[7])

    # TO DO:
    #
    #
    # PASS INITCOLORSYNTH A LIST OF STATISTICS ON IMAGE FOR AUDIO GEN
    #
    # for use as seen above in line 142

else: # get all color synths
    for i in range(4):
        rs = colorSynths[i]
        initColorSynth( i-1, rs[0], rs[1], rs[2], rs[3], rs[4], rs[5], rs[6], rs[7] )

mixer.write_wav('audio.wav')
samples = mixer.mix()


#----------------< AUDIO PLAYBACK >----------------#


print("Interpretation playing back now...")

# Set chunk size of 1024 samples per data frame
chunk = 1024
wf = wave.open('audio.wav', 'rb')
p = pyaudio.PyAudio()

# Open a .Stream object to write the WAV file to
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True) # indicates playback as opposed to recording

data = wf.readframes(chunk)
while data != '':
    stream.write(data)
    data = wf.readframes(chunk)

stream.close()
p.terminate()