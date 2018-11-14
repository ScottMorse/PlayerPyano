from pymusician import Chord, Note

standard_progression = {
    1: (2,3,4,5,6,7),
    2: (3,4,5,5,5,5,7),
    3: (6,6,6,4),
    4: (2,5,5,5,7),
    5: (6,1,1,1,1),
    6: (2,2,4,5,5,7,),
    7: (6,1)
}

def arpeggiate_8ths(chord,prev_note,harm_rhythm,pattern=None):
    note_groups = []
    harmony_notes = []
    for note in chord:
        note.octave = 3
        harmony_notes.append(note)
    if not prev_note:
        for i in range(harm_rhythm // 64):
            if i >= len(chord.spelling):
                i -= len(chord.spelling)
            mel_note = chord.spelling[i]
            mel_note.octave = 4
            mel_note.rhythm = '4'
            note_group = list(harmony_notes)
            note_group.append(mel_note)
            note_groups.append(note_group)
    else:
        for i in range(harm_rhythm // 64):
            if i >= len(chord.spelling):
                i -= len(chord.spelling)
            mel_note = chord.spelling[i]
            mel_note.octave = 4
            mel_note.rhythm = '4'
            note_group = list(harmony_notes)
            note_group.append(mel_note)
            note_groups.append(note_group)
    return note_groups