from pymusician import Chord, Note
from random import randint
import math

CHORD_QUALITIES = {
    'major': (
        ('maj','6')[randint(0,1)],
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
            ('min7','dom7','+','7b9')[randint(0,3)],
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
    ),
    'whole tone': (
        ('+','dom7b5')[randint(0,1)],
        ('+','dom7b5')[randint(0,1)],
        ('+','dom7b5')[randint(0,1)],
        ('+','dom7b5')[randint(0,1)],
        ('+','dom7b5')[randint(0,1)],
        ('+','dom7b5')[randint(0,1)],
    ),
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

pop_prog_2 = {
    1: (7,),
    7: (6,),
    6: (4,),
    4: (1,)
}

one_to_four = {
    1: (4,),
    4: (1,),
}

pop_prog_3 = {
    1: (3,),
    3: (4,),
    4: (6,),
    6: (1,)
}

three_six_two_five = {
    1: (6,),
    6: (2,),
    2: (5,),
    5: (1,3,),
    3: (2,)
}

anything_goes_6 = {
    1: (2,3,4,5,6),
    2: (1,3,4,5,6),
    3: (1,2,4,5,6),
    4: (1,2,3,5,6),
    5: (1,2,3,4,6),
    6: (1,2,3,4,5),
}

PROGRESSIONS = (standard_prog,epic_prog,pop_prog_1,pop_prog_2,pop_prog_3,three_six_two_five, one_to_four)
PROGRESSIONS = (standard_prog,)

SWING = True if not randint(0,5) else False

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

TRIPLET = randint(0,1)
TRIPLET = 1

ARPEGGIATE_HARMONY = randint(0,1)

NEIGHBORLY_RANDOMNESS = randint(1,20)

def create_harmony(chord,harm_rhythm):
    harmony_notes = []
    prev_harm_note = None
    for note in chord:
        note.octave = 3
        if prev_harm_note:
            if prev_harm_note.hard_pitch < note.hard_pitch:
                note.octave += 1
        harmony_notes.append(note)
        prev_harm_note = note
    return harmony_notes

if randint(0,1):
    RHYTHMIC_DIVISIONS = ("4t","3t")
else:
    RHYTHMIC_DIVISIONS = ("3","4","5")

RHYTHMIC_DOUBLERS = {
    "3": "4",
    "4": "5",
    "3t": "4t",
}

def produce_notes(chord,prev_note,harm_rhythm,key_mode,pattern=None):
    note_groups = []
    harmony_notes = create_harmony(chord,harm_rhythm)

    rhythmic_divisions = RHYTHMIC_DIVISIONS

    rhythm_remainder = harm_rhythm

    chord_note_names = [note.name for note in chord]
    key_note_names = [note.name for note in key_mode]

    arp_patt = None

    if not prev_note:
        arp_patt = ARPEGGIATION_PATTERNS_TRIAD if len(chord.spelling) == 3 else ARPEGGIATION_PATTERNS_SEVENTH
        arp_patt = arp_patt[randint(0,len(arp_patt) - 1)]

    xi = 0
    while rhythm_remainder > 0:

        if arp_patt:
            if xi >= len(arp_patt):
                xi -= len(arp_patt) * (xi // len(arp_patt))

        if not prev_note:
            mel_note = chord.spelling[arp_patt[xi]]
            mel_note.octave = 4

        else:
            #!!PLEASE REFACTOR THIS, ME
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

        rhythm = rhythmic_divisions[randint(0,len(rhythmic_divisions) - 1)]
        mel_note.rhythm = rhythm

        rhythm_remainder -= math.floor(mel_note.rhythm.value)
        
        if ARPEGGIATE_HARMONY:
            note_group = [(harmony_notes[randint(0,len(harmony_notes) - 1)]) for x in range(2)]
        else:
            note_group = list(harmony_notes)

        if rhythm in RHYTHMIC_DOUBLERS:
            neighbored = True if not randint(0,NEIGHBORLY_RANDOMNESS) else False
            mel_hard_pitch = mel_note.hard_pitch
            mel_note.rhythm = RHYTHMIC_DOUBLERS[rhythm]

            direction = (-1,1)[randint(0,1)]

            attempt_note = Note.from_hard_pitch(mel_hard_pitch + direction).enharmonic("b")

            if attempt_note.name in key_note_names:
                neighbor = attempt_note
            else:
                neighbor = Note.from_hard_pitch(mel_hard_pitch + direction * 2)
            neighbor.rhythm = RHYTHMIC_DOUBLERS[rhythm]

            multi_group = [mel_note,neighbor]

            for i in range(2):
                note_group_copy = list(note_group)
                note_group_copy.append(multi_group[i])
                multi_group[i] = note_group_copy
            note_groups.extend(multi_group)
        else:
            note_group.append(mel_note)
            note_groups.append(note_group)

        prev_note = mel_note
        xi += 1
    return note_groups

# def arpeggiate(chord,prev_note,harm_rhythm,key_mode,pattern=None):
#     note_groups = []
#     harmony_notes = create_harmony(chord,harm_rhythm)
#     if not prev_note:
#         if len(chord.spelling) == 3:
#             pattern = ARPEGGIATION_PATTERNS_TRIAD[randint(0,len(ARPEGGIATION_PATTERNS_TRIAD) - 1)]
#         else:
#             pattern = ARPEGGIATION_PATTERNS_SEVENTH[randint(0,len(ARPEGGIATION_PATTERNS_SEVENTH) - 1)]
#         rhythmic_divider = 64
#         if TRIPLET:
#             rhythmic_divider *= (2/3)
#         for i in range(round(harm_rhythm / rhythmic_divider)): # 64 to divide harmonic rhythm into eighth notes
#             if i >= len(pattern):
#                 i -= len(pattern) * (i // len(pattern))
#             mel_note = chord.spelling[pattern[i]]
#             mel_note.octave = 4
#             if SWING and not TRIPLET:
#                 if i % 2 == 0:
#                     mel_note.rhythm = '3t'
#                 else:
#                     mel_note.rhythm = '4t'
#             elif not TRIPLET:
#                 mel_note.rhythm = '4'
#             else:
#                 mel_note.rhythm = '4t'
#             note_group = list(harmony_notes)
#             if ARPEGGIATE_HARMONY:
#                 [note_group.append(harmony_notes[randint(0,len(harmony_notes) - 1)]) for x in range(2)]
#             note_group.append(mel_note)
#             note_groups.append(note_group)
#     else:
#         rhythmic_divider = 64
#         if TRIPLET:
#             rhythmic_divider *= (2/3)
        
#         for i in range(round(harm_rhythm / rhythmic_divider)):
#             note_group = list(harmony_notes)
#             if ARPEGGIATE_HARMONY:
#                 note_group.append(harmony_notes[randint(0,len(harmony_notes) - 1)])
#             prev_hard_pitch = prev_note.hard_pitch
#             for cnote in chord:
#                 cnote.octave = prev_note.octave
#                 up_or_down_range = (range(prev_hard_pitch - (2,4)[randint(0,1)], prev_hard_pitch),range(prev_hard_pitch + 1,prev_hard_pitch + (3,5)[randint(0,1)]))[randint(0,1)]
#                 if cnote.hard_pitch in up_or_down_range:
#                     mel_note = cnote
#                     break
#             else:
#                 for cnote in chord:
#                     cnote.octave = prev_note.octave + 1
#                     up_or_down_range = (range(prev_hard_pitch - (2,4)[randint(0,1)], prev_hard_pitch),range(prev_hard_pitch + 1,prev_hard_pitch + (3,5)[randint(0,1)]))[randint(0,1)]
#                     if cnote.hard_pitch in up_or_down_range:
#                         mel_note = cnote
#                         break
#                 else:
#                     for cnote in chord:
#                         cnote.octave = prev_note.octave - 1
#                         up_or_down_range = (range(prev_hard_pitch - (2,4)[randint(0,1)], prev_hard_pitch),range(prev_hard_pitch + 1,prev_hard_pitch + (3,5)[randint(0,1)]))[randint(0,1)]
#                         if cnote.hard_pitch in up_or_down_range:
#                             mel_note = cnote
#                             break
#                     else:
#                         mel_note = chord.spelling[randint(0,len(chord.spelling) - 1)]
#                         mel_note.octave = prev_note.octave
            
#             neighbored = True if not randint(0,NEIGHBORLY_RANDOMNESS) else False
#             chord_note_names = [note.name for note in chord]
#             key_note_names = [note.name for note in key_mode]

#             if SWING and not TRIPLET:
#                 if i % 2 == 0:
#                     mel_note.rhythm = '3t'
#                 else:
#                     mel_note.rhythm = '4t'
#             elif not TRIPLET:
#                 mel_note.rhythm = '4'
#             else:
#                 mel_note.rhythm = '4t'

#             if mel_note.name == prev_note.name:
#                 disallow = randint(0,9)
#                 if disallow:
#                     new_note = chord.spelling[0]
#                     while new_note.name == mel_note.name:
#                         new_note = chord.spelling[randint(0,len(chord.spelling) - 1)]
#                     new_note.octave = mel_note.octave
#                     new_note.rhythm = mel_note.rhythm.flags
#                     mel_note = new_note
#             if mel_note.octave < 4:
#                 mel_note.octave += 1
#             if mel_note.octave > 6:
#                 mel_note.octave -= 1

#             if neighbored and not SWING and not TRIPLET:
#                 mel_hard_pitch = mel_note.hard_pitch
#                 direction = (-1,1)[randint(0,1)]
#                 if mel_note.rhythm.flags == '4':
#                     mel_note.rhythm = '5'
#                 attempt_note = Note.from_hard_pitch(mel_hard_pitch + direction)
#                 if attempt_note.name in key_note_names:
#                     neighbor = attempt_note
#                 else:
#                     neighbor = Note.from_hard_pitch(mel_hard_pitch + direction * 2)
#                 neighbor.rhythm = '5'
#                 multi_group = [mel_note,neighbor]
#                 for i in range(2):
#                     note_group_copy = list(note_group)
#                     note_group_copy.append(multi_group[i])
#                     multi_group[i] = note_group_copy
#                 note_groups.extend(multi_group)
#             else:
#                 note_group.append(mel_note)
#                 note_groups.append(note_group)
#             prev_note = mel_note
#     return note_groups
    

MELODIC_IDEA_STRATEGIES = (produce_notes,)

def random_melodic_idea():
    return MELODIC_IDEA_STRATEGIES[randint(0,len(MELODIC_IDEA_STRATEGIES) - 1)]