from pymusician import Chord, Note
from random import randint

CHORD_QUALITIES = {
    'major': (
        'maj',
        ('min7','dom7')[randint(0,1)],
        'min',
        ('maj','maj7')[randint(0,1)],
        'dom7',
        'min',
        'dim'
    ),
    'minor': (
            'min',
            'dim',
            'maj',
            'min',
            ('min7','dom7','+','7b9')[randint(0,2)],
            'maj7',
            'maj'
        ),
    'dorian': (
        'min7',
        'min',
        'maj',
        'maj',
        'min7',
        'dim',
        'maj'
    )
}

standard_prog = {
    1: (2,3,4,5,6,7),
    2: (3,4,5,5,5,5,7),
    3: (6,6,6,4),
    4: (1,1,2,5,5,5,7),
    5: (6,1,1,1,1),
    6: (2,2,4,5,5,7,),
    7: (6,1)
}

epic_prog = {
    1: (7,6),
    7: (6,1),
    6: (7,7,5),
    5: (1,1,1,6)
}

pop_prog_1 = {
    1: (5,),
    5: (6,),
    6: (4,),
    4: (1,)
}

PROGRESSIONS = (standard_prog,epic_prog,pop_prog_1)

SWING = randint(0,1)

ARPEGGIATION_PATTERNS_TRIAD = (
    (0,1,2,1),
    (0,2,1,0),
    (2,0,1,0),
    (2,1,0,1),
    (0,2,0,1),
)

ARPEGGIATION_PATTERNS_SEVENTH = (
    (0,1,2,3),
    (3,2,1,0),
    (0,3,2,1),
    (0,3,1,2),
)

def arpeggiate_8ths(chord,prev_note,harm_rhythm,pattern=None):
    note_groups = []
    harmony_notes = []
    prev_harm_note = None
    for note in chord:
        note.octave = 2
        if prev_harm_note:
            if prev_harm_note.hard_pitch < note.hard_pitch:
                note.octave += 1
        harmony_notes.append(note)
        prev_harm_note = note
    if not prev_note:
        if len(chord.spelling) == 3:
            pattern = ARPEGGIATION_PATTERNS_TRIAD[randint(0,len(ARPEGGIATION_PATTERNS_TRIAD) - 1)]
        else:
            pattern = ARPEGGIATION_PATTERNS_SEVENTH[randint(0,len(ARPEGGIATION_PATTERNS_SEVENTH) - 1)]
        for i in range(harm_rhythm // 64): # 64 to divide harmonic rhythm into eigth notes
            mel_note = chord.spelling[pattern[i]]
            if i >= len(pattern):
                i -= len(pattern)
            mel_note.octave = 4
            if SWING:
                if i % 2 == 0:
                    mel_note.rhythm = '3t'
                else:
                    mel_note.rhythm = '4t'
            else:
                mel_note.rhythm = '4'
            note_group = list(harmony_notes)
            note_group.append(mel_note)
            note_groups.append(note_group)
    else:
        for i in range(harm_rhythm // 64):
            note_group = list(harmony_notes)
            prev_hard_pitch = prev_note.hard_pitch
            for cnote in chord:
                cnote.octave = prev_note.octave
                up_or_down_range = (range(prev_hard_pitch - (2,4)[randint(0,1)], prev_hard_pitch),range(prev_hard_pitch + 1,prev_hard_pitch + (3,5)[randint(0,1)]))[randint(0,1)]
                if cnote.hard_pitch in up_or_down_range:
                    mel_note = cnote
                    break
            else:
                for cnote in chord:
                    cnote.octave = prev_note.octave + 1
                    up_or_down_range = (range(prev_hard_pitch - (2,4)[randint(0,1)], prev_hard_pitch),range(prev_hard_pitch + 1,prev_hard_pitch + (3,5)[randint(0,1)]))[randint(0,1)]
                    if cnote.hard_pitch in up_or_down_range:
                        mel_note = cnote
                        break
                else:
                    for cnote in chord:
                        cnote.octave = prev_note.octave - 1
                        up_or_down_range = (range(prev_hard_pitch - (2,4)[randint(0,1)], prev_hard_pitch),range(prev_hard_pitch + 1,prev_hard_pitch + (3,5)[randint(0,1)]))[randint(0,1)]
                        if cnote.hard_pitch in up_or_down_range:
                            mel_note = cnote
                            break
                    else:
                        mel_note = chord.spelling[randint(0,len(chord.spelling) - 1)]
                        mel_note.octave = prev_note.octave
            if SWING:
                if i % 2 == 0:
                    mel_note.rhythm = '3t'
                else:
                    mel_note.rhythm = '4t'
            else:
                mel_note.rhythm = '4'

            if mel_note.name == prev_note.name:
                disallow = randint(0,9)
                if disallow:
                    new_note = chord.spelling[0]
                    while new_note.name == mel_note.name:
                        new_note = chord.spelling[randint(0,len(chord.spelling) - 1)]
                    new_note.octave = mel_note.octave
                    new_note.rhythm = mel_note.rhythm.flags
                    mel_note = new_note
            if mel_note.octave < 3:
                mel_note.octave += 1
            if mel_note.octave > 5:
                mel_note.octave -= 1
            note_group.append(mel_note)
            note_groups.append(note_group)
            prev_note = mel_note
    return note_groups

def flurry_up_sextuplets(chord,prev_note,harm_rhythm,pattern=None):
    note_groups = []
    harmony_notes = []
    prev_harm_note = None
    for note in chord:
        note.octave = 2
        if prev_harm_note:
            if prev_harm_note.hard_pitch < note.hard_pitch:
                note.octave += 1
        harmony_notes.append(note)
        prev_harm_note = note
    

MELODIC_IDEA_STRATEGIES = (arpeggiate_8ths,)

def random_melodic_idea():
    return MELODIC_IDEA_STRATEGIES[randint(0,len(MELODIC_IDEA_STRATEGIES) - 1)]