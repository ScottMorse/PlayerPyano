import numpy
import pyaudio
import time
from pymusician import Note
from random import random, randint

p = pyaudio.PyAudio()

SAMPLE_RATE = 22000
BASE_MODULATION = random() * 0.7

def sine(frequency, length):
    length = length * SAMPLE_RATE
    factor = (float(frequency) * (numpy.pi * 2) / SAMPLE_RATE)
    return numpy.sin(numpy.arange(length) * factor)

def create_sine(frequency,length):
    return [sine(frequency,length)]

OVERTONE_INTENSITY = 0.04 * random() + 0.02

all_overtone_ratios = (2,3,4,5,6,8,9,10,11,12,13,15,16)
clarinet_overtone_ratios = (3,5,9,11,13,15)
organ_overtone_ratios = (2,4,6,8,10,12,16)

OVERTONES_TO_USE = (all_overtone_ratios,clarinet_overtone_ratios,organ_overtone_ratios)[randint(0,2)]

def create_overtones(frequency,length):
    return [numpy.concatenate(create_sine(frequency * ratio,length)) * (
            OVERTONE_INTENSITY if ratio < 5 else OVERTONE_INTENSITY * 0.1) for ratio in OVERTONES_TO_USE]

NORMALIZE_VOLUME = 0.3

def create_tone_chunk(frequency, length, modulate=BASE_MODULATION):

    mod_freq1 = frequency - modulate
    mod_freq2 = frequency + modulate

    frequencies = [frequency,mod_freq1,mod_freq2]

    overtones = [create_overtones(freq,length) for freq in frequencies]
    sines = [create_sine(freq,length) for freq in frequencies]

    chunks = [sum([numpy.concatenate(sine) * NORMALIZE_VOLUME * (1/3) for sine in sines])]
    [chunks.extend([overtone for overtone in overtone_array]) for overtone_array in overtones]
    chunk = sum(chunks)
    
    return chunk

ATTACK = round(300 * random()) + 100

class Stream():

    def __init__(self):
        self.stream = p.open(format=pyaudio.paFloat32,
            channels=1, rate=SAMPLE_RATE, output=1)
    
    def play_notes(self,duration,*notes,fade=False):
        tone_chunks = [create_tone_chunk(note.frequency,duration) for note in notes]
        multiplier = 1 / len(tone_chunks)

        first = True
        for tone in tone_chunks:
            if first:
                chunk = tone * multiplier
                first = False
                continue
            chunk += tone * multiplier

        if fade:
            fade_in_frames = ATTACK
            fade_out_frames = 4000
        else:
            fade_in_frames = ATTACK
            fade_out_frames = 50

        fade_in = numpy.arange(0., 1., 1./fade_in_frames)
        fade_out = numpy.arange(1., 0., -1./fade_out_frames)

        chunk[:fade_in_frames] = numpy.multiply(chunk[:fade_in_frames], fade_in)
        chunk[-fade_out_frames:] = numpy.multiply(chunk[-fade_out_frames:], fade_out)

        self.stream.write(chunk.astype(numpy.float32).tostring())

if __name__ == '__main__':

    stream = Stream()

    stream.play_notes(1,Note("A",3),Note("C#",4),Note("E",4))

    stream.stream.close()

    