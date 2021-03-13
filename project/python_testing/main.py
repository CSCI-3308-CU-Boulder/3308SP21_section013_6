
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



#-----------< GLOBALS >-----------#


# toggle whether the image should be displayed to the screen
TOGGLE_SHOW_IMAGE = 1

# select which image, of those listed below, to select
image_selected = 1

TOGGLE_DRAW = 1

# format of images in this list is:
# [ [name, path], ... ]
image_pool =   [
                ['hedgehog', 'hedgehog.jpeg'],
                ['fabio', 'fabio.jpg'],
                ['lenna', 'lenna.png']
                                       ]


# Toggle generation and playback of audio
TOGGLE_MAKE_AUDIO = 1
volume = 0.4
duration = 5


img = image_pool[image_selected - 1]

# append testImages dir to paths
path = "testImages/"
for i in image_pool:
    i[1] = path + i[1]

# [ [ color, synth, attack, decay, vibrato_frequency, vibrato_variance, octave, pitch_1], ... ]
colorSynths = [
    [ 'red', SAWTOOTH_WAVE, 1.0, 1.0, 0.0, 0.0, 4, 'f'],
    [ 'blue', SINE_WAVE, 1.0, 1.0, 0.0, 0.0, 5, 'a'],
    [ 'green', TRIANGLE_WAVE, 1.0, 1.0, 0.0, 0.0, 4, 'e'],
    [ 'value', SQUARE_WAVE, 1.0, 1.0, 0.0, 0.0, 4, 'd'],
    [ 'alpha', SAWTOOTH_WAVE, 1.0, 1.0, 0.0, 0.0, 4, 'bb'],
    ]

print("Running...")


#----------------< IMAGE ANALYSIS DEFINITIONS >----------------#


# params: ( image pixel matrix , channel to keep )
# NOTE: destroys other channels
# returns pixel matrix of a single color
def __STRIP_CHANNELS__(mat, chan):
    ret_mat, row = [], []  # to store/build stripped mat
    for y in range(len(mat)):
        row = []
        for x in range(len(mat[y])):
            row.append(mat[y][x][chan])
        ret_mat.append(row)
    return np.array(ret_mat)


# params: ( image pixel matrix , channel to keep )
# NOTES: retains other empty channels in list as 0's
# returns pixel matrix of a single color
def __STRIP_INPLACE__(mat, chan):
    ret = mat.copy()
    if chan == 0:
        ret[:, :, 1] = 0
        ret[:, :, 2] = 0
    if chan == 1:
        ret[:, :, 0] = 0
        ret[:, :, 2] = 0
    if chan == 2:
        ret[:, :, 0] = 0
        ret[:, :, 1] = 0
    return ret

# params: ( image pixel matrix)
# returns: color channels variance
def __VAR__(full_mat):
    var = []




# params: ( image pixel matrix )
# returns: color channels center of mass
def __COM__(full_mat):
    w, h =__getImageDimensions__(full_mat)

    channels_COM = [] # to store return string

    # strip color channels from each other
    channels = [__STRIP_CHANNELS__(full_mat,0),__STRIP_CHANNELS__(full_mat,1),__STRIP_CHANNELS__(full_mat,2)]


    for channel in range(getChannels(full_mat)):
        print("Performing center of mass function on color channel {}...".format(channel))

        mat = channels[channel]

        # calculate Xbar, Ybar
        sum_over_columns = [sum(x) for x in zip(*mat)]
        sum_over_rows = [sum(x) for x in mat]
        x_weights, x_masses, y_weights, y_masses = [],[],[],[]
        for i in range(w):
            x_weights.append( i * sum_over_columns[i] ) # mass times position
            x_masses.append( sum_over_columns[i]  ) # mass
        x_bar = sum( x_weights ) / sum( x_masses )

        for i in range(h):
            y_weights.append( i * sum_over_rows[i] ) # mass times position
            y_masses.append( sum_over_rows[i]  ) # mass
        y_bar = sum( y_weights ) / sum( y_masses )

        # print("x_bar: {:.4f}\ny_bar: {:.4f}".format(x_bar,y_bar))
        channels_COM.append( [ int(round(x_bar)), int(round(y_bar)) ] )

    return channels_COM


# params: ( image pixel matrix )
# returns ( width, height )
def __getImageDimensions__(mat):
    w = len(mat[0])
    h = len(mat)
    return (w, h)

# params: ( image pixel matrix )
# returns no. of pixel color channels
def getChannels(image):
    if isgray(image):
        return len(image[0])
    else:
        return len(image[0][0])

# params: ( image pixel matrix )
# returns 1 if gray, else 0
def isgray(image):
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
        val_max = np.max(image)
        val_min = np.min(image)
        print("Average value: {:.2f}".format(mean))
        print("Max value: {:.2f}".format(val_max))
        print("Min value: {:.2f}".format(val_min))
        print("Range of value: {:.2f}\n".format(val_max - val_min))
        retStats.append([ 'gray', mean, (val_max-val_min) ])
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
            val_max = np.max(color[0])
            val_min = np.min(color[0])
            print("Average {}: {:.2f}".format(color[1], mean))
            print("Max {}: {:.2f}".format(color[1], val_max))
            print("Min {}: {:.2f}".format(color[1], val_min))
            print("Range {}: {:.2f}\n".format(color[1], (val_max - val_min)) )

            retStats.append([color[1], mean, (val_max - val_min)])


        avg_color = [np.sum(blue) / count, np.sum(green) / count, np.sum(red) / count]
        print("Average color value: [{:.2f}, {:.2f}, {:.2f}]".format(avg_color[0], avg_color[1], avg_color[2]))
        print("Range of color: {:.2f}".format( (np.max(pixel_sums)-np.min(pixel_sums)) )) # (a ratio of difference between colors)

        mean = np.mean(image)
        val_max = np.max(image)
        val_min = np.min(image)

        print("Average shade value: {:.2f}".format(mean))
        print("Max shade value: {:.2f}".format(val_max))
        print("Min shade value: {:.2f}".format(val_min))
        print("Range of shade value: {:.2f}\n".format(val_max-val_min))

        retStats.append([ 'shade', mean, (val_max-val_min) ])

    return retStats


#----------------< AUDIO GENERATION DEFINITIONS >----------------#


def initColorSynth( iden, analysis, color, synth, attack=1, decay=1, v_f=0, v_=0, octave=4, pitch_1='c' ):

    print(color + " tones being generated...")
    print("Analysis...\n{}\n".format(analysis))
    mixer.create_track(iden, synth, vibrato_frequency=v_f, vibrato_variance=v_v, attack=attack, decay=decay)

    presence = analysis[1]/255  # calculates the presence of each color in an image
                                # (normalize the mean to 0-1 to stuff into amplitude)
    mixer.add_note(iden, note=pitch_1, octave=octave, duration=duration, amplitude=presence)


#----------------< IMAGE PROCESSING >----------------#


# [ [name, path, pixelData], ... ]
img.append( cv2.imread(img[1]) )

# [ [channel attribute, mean, range, ...]
# imgAnal = analyze_image(img[0], img[2], img[1])

circles = __COM__(img[2])
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
# print(circles)

if TOGGLE_SHOW_IMAGE and TOGGLE_DRAW:
    w, h = __getImageDimensions__(img[2])
    for circle in range(getChannels(img[2])):
        image = cv2.circle(
                        img[2], (circles[circle][0],circles[circle][1]),
                        int( w/8 ),
                        colors[circle],
                        int( w/150 ) )


if TOGGLE_SHOW_IMAGE:
    showImage = img[2]
    width, height = __getImageDimensions__(img[2])
    if (width > 800) or (height > 800): # if image is larger than 800 pixels in either dimension
        factor = 0.2  # percent of original size
        width = int(showImage.shape[1] * factor)
        height = int(showImage.shape[0] * factor)
        dimensions = (width, height)
        # print("Resized image: {}, {}".format(width, height))

        showImage = cv2.resize(showImage, dimensions, interpolation = cv2.INTER_AREA)

    print("Image displayed!")
    cv2.imshow(img[0], showImage)

    cv2.imshow('B-RGB', __STRIP_INPLACE__(showImage, 0))
    cv2.imshow('G-RGB', __STRIP_INPLACE__(showImage, 1))
    cv2.imshow('R-RGB', __STRIP_INPLACE__(showImage, 2))


#----------------< AUDIO GENERATION >----------------#

if TOGGLE_MAKE_AUDIO:
    mixer = Mixer(44100, volume)

    # [ [ color, anal, synth, attack, decay, vibrato_frequency, vibrato_variance, octave, pitch_1], ... ]
    imgAnal = analyze_image(img[0], img[2], img[1])

    if isgray(img[2]): # only get value synth
        rs = colorSynths[3]
        anal = imgAnal[0]
        initColorSynth(0, anal, rs[0], rs[1], rs[2], rs[3], rs[4], rs[5], rs[6], rs[7])

    else: # get all color synths
        for i in range(4):
            rs = colorSynths[i]
            anal = imgAnal[i]
            initColorSynth( i-1, anal, rs[0], rs[1], rs[2], rs[3], rs[4], rs[5], rs[6], rs[7] )


    mixer.write_wav('audio.wav')
    samples = mixer.mix()


#----------------< AUDIO PLAYBACK >----------------#

if TOGGLE_MAKE_AUDIO:
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


#----------------< IMAGE MANAGEMENT >----------------#

if TOGGLE_SHOW_IMAGE:
    cv2.waitKey(0)
    cv2.destroyAllWindows()

