class Chord:
    default_scale = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
    note_conversion_table = {
        'B#': 'C',
        'Db': 'C#',
        'D#': 'Eb',
        'Fb': 'E',
        'E#': 'F',
        'Gb': 'F#',
        'Ab': 'G#',
        'A#': 'Bb',
        'Cb': 'B'
    }
    note_to_pc = {note: pc for note, pc in zip(default_scale, [i for i in range(12)])}

    standard_qualities = ['M', 'm', 'o', '+', '7', 'M7', 'm7', 'o7', '/o7', 'sus2', 'sus4']
    quality_conversion_table = {
        'maj': 'M',
        'min': 'm',
        'dim': 'o',
        'aug': '+',
        'dom': '7',
        'Mm7': '7',
        'maj7': 'M7',
        'MM7': 'M7',
        'min7': 'm7',
        'mm7': 'm7',
        'dim7': 'o7',
        'd7': 'o7',
        'hd7': '/o7',
        'o/7': '/o7'
    }
    qualities = standard_qualities + list(quality_conversion_table.keys())

    def __init__(self, args=None, scale=None):
        if args is None:
            self.root_pc = None
            self.quality = None
            self.bass_pc = None
        elif type(args) == str:
            self.root_pc, self.quality, self.bass_pc = Chord.parse_chord_symbol(args)
        elif type(args) == tuple and len(args) == 3:
            self.root_pc, self.quality, self.bass_pc = args

        if scale is None:
            self.scale = Chord.default_scale
        elif type(scale) == list:
            self.scale = scale

    def __repr__(self):
        quality_string = '\'' + self.quality + '\'' if self.quality is not None else None
        return f'Chord(root_pc={self.root_pc}, quality={quality_string}, bass_pc={self.bass_pc})'

    def __str__(self):
        if self.root_pc is None or self.quality is None or self.bass_pc is None:
            return 'None'
        return f'{self.root()}{self.quality}{f"/{self.bass()}" if self.root_pc != self.bass_pc else ""}'

    def __eq__(self, other):
        if type(other) != Chord:
            return False
        else:
            return self.root_pc == other.root_pc and self.quality == other.quality and self.bass_pc == other.bass_pc

    def __ne__(self, other):
        return not self == other

    def root(self):
        return self.scale[self.root_pc] if self.root_pc is not None else None

    def bass(self):
        return self.scale[self.bass_pc] if self.bass_pc is not None else None

    def is_complete(self):
        return self.root_pc is not None and self.quality is not None and self.bass_pc is not None

    def transpose(self, key):
        if not self.is_complete():
            return Chord(str(self))
        else:
            new_root = (self.root_pc - key + 12) % 12
            new_bass = (self.bass_pc - key + 12) % 12

            return Chord((new_root, self.quality, new_bass), scale=self.scale)

    @staticmethod
    def parse_chord_symbol(chord_string):
        if chord_string is None or chord_string == 'None':
            return None, None, None

        current_index = 0
        root_note = None
        if chord_string[:2] in Chord.default_scale:
            root_note = chord_string[:2]
            current_index += 2
        elif chord_string[:2] in Chord.note_conversion_table.keys():
            root_note = Chord.note_conversion_table[chord_string[:2]]
            current_index += 2
        elif chord_string[:1] in Chord.default_scale:
            root_note = chord_string[:1]
            current_index += 1
        elif chord_string[:1] in Chord.note_conversion_table.keys():
            root_note = Chord.note_conversion_table[chord_string[:1]]
            current_index += 1
        root_pc = Chord.note_to_pc[root_note] if root_note in Chord.note_to_pc.keys() else None

        quality = None
        if chord_string[current_index:current_index + 4] in Chord.qualities:
            quality = chord_string[current_index:current_index + 4]
            current_index += 4
        elif chord_string[current_index:current_index + 3] in Chord.qualities:
            quality = chord_string[current_index:current_index + 3]
            current_index += 3
        elif chord_string[current_index:current_index + 2] in Chord.qualities:
            quality = chord_string[current_index:current_index + 2]
            current_index += 2
        else:
            quality = chord_string[current_index:current_index + 1]
            current_index += 1
        if quality is not None and quality not in Chord.standard_qualities:
            quality = Chord.quality_conversion_table[quality]

        bass_note = chord_string[current_index + 1:]
        if bass_note not in Chord.default_scale and bass_note != '':
            bass_note = Chord.note_conversion_table[bass_note]
        bass_pc = root_pc if bass_note == '' else Chord.note_to_pc[bass_note]

        return root_pc, quality, bass_pc
