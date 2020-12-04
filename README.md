# chorder 0.1.2

## Installation

`chorder` is a chord detection and reharmonize tool for `.mid` files. You can download `chorder` using pip:

```shell
pip install chorder
```

To check if `chorder` is successfully installed, type `python` in the terminal, and do the following:

```python
>>> from chorder import Chord
>>> Chord()
Chord(root_pc=None, quality=None, bass_pc=None)
```
## Documentation
### Chord

The `Chord` class is the basic building block for the whole chorder package. A `Chord` instance has four attributes, including:
 - `root_pc`
     - the pitch class of a chord's root note
     - is an integer ranging from 0 to 11
 - `quality`, the quality of a chord (the complete list of quality)
     - the quality of a chord
     - is a string
     - the complete list of qualities covered in `chorder` can be found at `Chord.standard_qualities`
 - `bass_pc`
     - the pitch class of a chord's bass note
     - is an integer ranging from 0 to 11
 - `scale`
     - the scale of the chord
     - is a list of strings representing the note names of each pitch class from 0 to 11
     - if a scale is not specified, a default scale is used, which is in `Chord.default_scale`

#### `Chord.__init__(self, args=None, scale=None)`
##### Parameters
 - `args`: `None` or `str` or `tuple`, optional
     - `None`: implies constructing an empty chord
     - `str`: a chord symbol, such as `'Bbmaj7'`
     - `tuple`: a tuple consisting of `(root_pc, quality, bass_pc)
 - `scale`: `list`, optional
     - specify the scale the chord uses
     - will use `Chord.default_scale` if left as `None`

#### `Chord.root(self)`
Returns the root note name of a chord based on the chord's scale.

#### `Chord.bass(self)`
Returns the bass note name of a chord based on the chord's scale.

#### `Chord.bass(self)`
Returns if any attributes of a chord is `None`. This can help filtering empty chords.

#### `Chord.transpose(self, key)`
Transposes a chord to C-based relative chord. For example, `Chord('Bb7').transpose(3)` should return `Chord('G7')`.
##### Parameters
 - `key`: `int`
     - the pitch class of the key
     - ranges from 0 to 11

### DeChorder
`DeChorder` is a class that consists of static methods related to chord recognition. To utilize this class, the midi information has to be in the form of [miditoolkit](https://github.com/YatingMusic/miditoolkit) objects.

#### `Dechorder.get_bass_pc(notes, start=0, end=1e7)`
Returns the pitch class of bass note among the notes between the time range of `start` and `end`.
##### Parameters
 - `notes`: list
     - the group of notes
     - notes are in the form of `miditoolkit.midi.containers.Note`
 - `start`: int
     - the start tick of the notes to be considered
     - set it to `notes[0].start` for now, as this feature will later be updated
 - `end`: int
     - the end tick of the notes to be considered
     - set it to `notes[-1].end` for now, as this feature will later be updated

#### `Dechorder.get_chord_quality(notes, start=0, end=1e7, consider_bass=False)`
Returns the chord among the notes between the time range of `start` and `end`.
##### Parameters
 - `notes`: list
     - the group of notes
     - notes are in the form of `miditoolkit.midi.containers.Note`
 - `start`: int
     - the start tick of the notes to be considered
     - set it to `notes[0].start` for now, as this feature will later be updated
 - `end`: int
     - the end tick of the notes to be considered
     - set it to `notes[-1].end` for now, as this feature will later be updated
 - `consider_bass`: `bool
     - decreases the likelihood of chords with non-chord tones as bass to be chosen as the answer

#### `Dechorder.dechord(midi_obj, scale=None)`
Returns a list of chords by beat.
##### Parameters
 - `midi_obj`: `miditoolkit.midi.parser.MidiFile`
     - the midi object to extract chord symbols from
 - `scale`: `list`
     - the list of note names for each pitch class
     - must be a list of strings