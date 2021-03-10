
# Author: Spencer Stepanek and team 013_6
# CSCI_3308, Photophonic Web-App Project
# Created on 2/16/21


import numpy as np
import cv2
from tones import SINE_WAVE, SAWTOOTH_WAVE
from tones.mixer import Mixer


show = 0
test_count = 1

# [ [name, path, pixelData], ... ]
image_pool = [ ['fabio', 'fabio.jpg'], ['lenna', 'lenna.png'] ]
img = image_pool[test_count - 1]


volume = 0.5
duration = 5

# [ [ color, synth, attack, decay, vibrato_frequency, vibrato_variance, octave, pitch_1], ... ]
colorSynths = [ [ 'red', SAWTOOTH_WAVE, 1.0, 1.0, 0.0, 0.0, 4, 'f'] ]


#----------------< IMAGE PROCESSING >----------------#

def getChannels(img):
    return len(img[0])

def isgray(imgpath):
    img = cv2.imread(imgpath)
    if len(img.shape) < 3: return True
    if img.shape[2]  == 1: return True
    b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
    if (b==g).all() and (b==r).all(): return True
    return False

def get_avg_colors(name, image, path):
    if isgray(path):
        print("\n ---- Analyzing {} in grayscale ---- ".format(name))
        mean = np.mean(image)
        max = np.max(image)
        min = np.min(image)
        print("Average value: {:.2f}".format(mean))
        print("Max value: {:.2f}".format(max))
        print("Min value: {:.2f}".format(min))
        print("Range of value: {:.2f}\n".format(max - min))
    else:
        print("\n ---- Analyzing {} in BGR color ---- ".format(name))
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
        # print(pixel_sums)

        for color in [ [blue, "blue"], [green, "green"], [red, "red"] ]:
            mean = np.mean(color[0])
            max = np.max(color[0])
            min = np.min(color[0])
            print("Average {}: {:.2f}".format(color[1], mean))
            print("Max {}: {:.2f}".format(color[1], max))
            print("Min {}: {:.2f}".format(color[1], min))
            print("Range {}: {:.2f}\n".format(color[1], (max - min)) )

        avg_color = [np.sum(blue) / count, np.sum(green) / count, np.sum(red) / count]
        print("Average color value: [{:.2f}, {:.2f}, {:.2f}]".format(avg_color[0], avg_color[1], avg_color[2]))
        print("Range of color: {:.2f}".format( (np.max(pixel_sums)-np.min(pixel_sums)) )) # (a ratio of difference between colors)

        mean = np.mean(image)
        max = np.max(image)
        min = np.min(image)
        print("Average shade value: {:.2f}".format(mean))
        print("Max shade value: {:.2f}".format(max))
        print("Min shade value: {:.2f}".format(min))
        print("Range of shade value: {:.2f}\n".format(max - min))


#----------------< AUDIO GENERATION >----------------#


def initColorSynth( color, synth, attack, decay, vibrato_frequency, vibrato_variance, octave, pitch_1 ):
    print("Boing! initColorSynth() called.")



#----------------< IMAGE PROCESSING >----------------#


# [ [name, path, pixelData], ... ]
img.append( cv2.imread(img[1]) )
get_avg_colors(img[0], img[2], img[1])

if show:
    cv2.imshow(img[1], img[2])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#----------------< AUDIO GENERATION >----------------#


mixer = Mixer(44100, volume)

rs = colorSynths[0]
initColorSynth( rs[0], rs[1], rs[2], rs[3], rs[4], rs[5], rs[6], rs[7] )

# for i in range(getChannels(img)):
#     initColorSynth()

#
# mixer.create_track(0, SAWTOOTH_WAVE, vibrato_frequency=0.5, vibrato_variance=0.0, attack=0.01, decay=0.1)
# mixer.create_track(1, SINE_WAVE, attack=0.01, decay=0.1)
# mixer.create_track(2, SINE_WAVE, attack=0.01, decay=0.1)
# mixer.create_track(3, SINE_WAVE, vibrato_frequency=0.03, vibrato_variance=0.01, attack=0.01, decay=0.1)
#
# mixer.add_note(0, note='f', octave=4, duration=2.0, endnote='ab')
# mixer.add_note(1, note='db', octave=5, duration=2.0, endnote='f')
# mixer.add_note(2, note='ab', octave=2, duration=2.0)
# mixer.add_note(3, note='ab', octave=3, duration=1.0)
#
# mixer.add_note(3, note='gb', octave=3, duration=1.0)
#
# mixer.add_note(0, note='ab', octave=4, duration=2.0)
# mixer.add_note(1, note='f', octave=5, duration=2.0)
# mixer.add_note(2, note='db', octave=2, duration=2.0)
# mixer.add_note(3, note='gb', octave=3, duration=2.0)

mixer.write_wav('gen.wav')

samples = mixer.mix()
