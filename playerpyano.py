import synthesizer
import pyglet
from pymusician import Note,Chord,Interval,Mode
import ideas
from random import randint,random

stream = synthesizer.Stream()

TEMPO = randint(60,300)

KEY_ROOTS = ('Ab','A','Bb','B','C','Db','D','Eb','E','F','Gb','G')

KEY_QUAL = ('major','minor','dorian')[randint(0,2)]

KEY_QUAL = 'dorian'

KEY = Mode(KEY_ROOTS[randint(0,11)],KEY_QUAL)

CHORD_QUALS = ideas.CHORD_QUALITIES[KEY_QUAL]

HARMONIC_RHYTHM = (str(randint(2,3)))

HARMONIC_RHYTHM_VALUE = Note('A',0,HARMONIC_RHYTHM).rhythm.value

HARMONIC_DURATION = (60 / TEMPO) * (HARMONIC_RHYTHM_VALUE / 128)

HARMONIC_METHOD = ideas.PROGRESSIONS[randint(0,1)]

#standard progression cycle
romans = [1]
prev_roman = 1
for i in range(50):
    options = HARMONIC_METHOD[prev_roman]
    next_roman = options[randint(0,len(options) - 1)]
    romans.append(next_roman)
    if i > 30 and next_roman == 1:
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
    melodic_ideas.append(ideas.random_melodic_idea()(chord,prev_note,HARMONIC_RHYTHM_VALUE))
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

# harmony = [(Chord('C'),Chord('G'))]
# HARMONIC_RHYTHM = ('3')
# HARMONIC_RHYTHM_VALUE = Note('A',0,HARMONIC_RHYTHM).rhythm.value
# VOICING = (0,1,2)

# chord_count = melody_length // HARMONIC_RHYTHM_VALUE
# harmonic_rhythm_positions = [i * HARMONIC_RHYTHM_VALUE for i in range(chord_count)]

# n = 1
# rhythmic_position = 0
# chord_position = 0
# fade = False
# for note in melody:
#     duration = (60 / TEMPO) * (note.rhythm.value / 128)
#     if rhythmic_position == harmonic_rhythm_positions[chord_position + 1]:
#         chord_position += 1
#     chord = net_chords[chord_position]
#     harmony_notes = []
#     for cnote in chord:
#         cnote.octave = 3
#         harmony_notes.append(cnote)
#     if n == len(melody):
#         duration *= 2
#         fade = True
#     stream.play_notes(duration,note,*harmony_notes,fade=fade)
#     rhythmic_position += note.rhythm.value
#     n += 1

# i = 1
# fade = False
# for melNote in melody:
#     duration = (60 / TEMPO) * (melNote.rhythm.value / 128)
#     if i == len(melody):
#         duration *= 2
#         fade = True
#     stream.play_notes(duration,melNote,*harmony_notes,fade=fade)
#     i += 1

stream.stream.close()