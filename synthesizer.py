import numpy
import pyaudio
import time
from pymusician import Note

p = pyaudio.PyAudio()

SAMPLE_RATE = 22000
BASE_MODULATION = 0.2

def sine(frequency, length):
    length = length * SAMPLE_RATE
    factor = (float(frequency) * (numpy.pi * 2) / SAMPLE_RATE)
    return numpy.sin(numpy.arange(length) * factor)

def create_sine(frequency,length):
    return [sine(frequency,length)]

overtone_ratios = (2,3,4,5,6,8,9,10,11,12,13,15,16)
def create_overtones(frequency,length):
    return [numpy.concatenate(create_sine(frequency * ratio,length)) * (
            0.005 if ratio < 5 else 0.0005) for ratio in overtone_ratios]

def create_tone_chunk(frequency, length, modulate=BASE_MODULATION):
    fundamental = create_sine(frequency,length)
    overtones = create_overtones(frequency,length)

    string1 = create_sine(frequency - modulate,length)
    string2 = create_sine(frequency + modulate,length)
    string1_ov = create_overtones(frequency - modulate,length)
    string2_ov = create_overtones(frequency + modulate, length)
    
    chunk = numpy.concatenate(fundamental) * 0.3 * (1/3)
    chunk += numpy.concatenate(string1) * 0.3 * (1/3)
    chunk += numpy.concatenate(string2) * 0.3 * (1/3)

    for overtone in overtones:
        chunk += overtone
    
    for overtone in string1_ov:
        chunk += overtone
    
    for overtone in string2_ov:
        chunk += overtone
    
    return chunk

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
            fade_in_frames = 500
            fade_out_frames = 2000
        else:
            fade_in_frames = 100
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