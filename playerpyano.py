import synthesizer
from pymusician import Note,Chord,Interval,Mode
import ideas
from random import randint,random

stream = synthesizer.Stream()

TEMPO = randint(50,250)

TEMPO = 60

KEY_ROOTS = ('Ab','A','Bb','B','C','Db','D','Eb','E','F','Gb','G')

KEY_QUAL = ('major','minor','dorian','whole tone')[randint(0,3)]

KEY = Mode(KEY_ROOTS[randint(0,11)],KEY_QUAL)

CHORD_QUALS = ideas.CHORD_QUALITIES[KEY_QUAL]

HARMONIC_RHYTHM = (str(randint(2,3)))

HARMONIC_RHYTHM_VALUE = Note('A',0,HARMONIC_RHYTHM).rhythm.value

HARMONIC_DURATION = (60 / TEMPO) * (HARMONIC_RHYTHM_VALUE / 128)

HARMONIC_METHOD = ideas.PROGRESSIONS[randint(0,len(ideas.PROGRESSIONS) - 1)]

romans = [1]
prev_roman = 1
for i in range(100):
    if KEY_QUAL == 'whole tone':
        options = ideas.anything_goes_6[prev_roman]
    else:
        options = HARMONIC_METHOD[prev_roman]
    next_roman = options[randint(0,len(options) - 1)]
    romans.append(next_roman)
    if i > 50 and next_roman == 1:
        break
    prev_roman = next_roman

chords = []
for roman in romans:
    index = roman - 1
    chords.append(Chord(KEY.spelling[index].name + CHORD_QUALS[index]))

RHYTHMIC_PERIOD = HARMONIC_RHYTHM_VALUE * len(chords)

melodic_ideas = []
prev_note = None
for chord in chords:
    melodic_ideas.append(ideas.random_melodic_idea()(chord,prev_note,HARMONIC_RHYTHM_VALUE,KEY))
    prev_note = melodic_ideas[-1][-1][-1]

idea_count = 1
fade = False
for idea in melodic_ideas:
    melody_count = 1
    for melodic_group in idea:
        duration = (60 / TEMPO) * (melodic_group[-1].rhythm.value / 128)
        if melody_count == len(idea) and idea_count == len(melodic_ideas):
            duration *= 3
            fade = True
        stream.play_notes(duration,*melodic_group,fade=fade)
        melody_count += 1
    idea_count += 1

stream.stream.close()