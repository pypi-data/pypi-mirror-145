from copy import copy, deepcopy
from dataclasses import dataclass, field
from itertools import count, chain
from typing import Sequence, Optional, Union, List, Tuple, Any

from icecream import ic

import MidiCompose.logic.harmony.note
from MidiCompose.logic.harmony.figure import AbstractBaseFiguredNote, TonalFiguredNote
from MidiCompose.logic.harmony.interval import Interval, IntervalRange
from MidiCompose.logic.harmony.key import Key
from MidiCompose.logic.harmony.note import Note, HasNotes, to_note
from MidiCompose.logic.melody.note_set import NoteSet


class Chord:
    """
    Sorted, unique set of notes with utility methods for generating harmonic progressions.
    """

    def __init__(self,
                 notes: Optional[Union[Note, Any]] = None,
                 force_unique: bool = True):

        self.force_unique = force_unique
        self.notes = notes  # calls setter

    @property
    def notes(self) -> List[Note]:
        return self._notes

    @notes.setter
    def notes(self, value):

        _notes = None
        if value:
            if isinstance(value, TonalFiguredNote):
                _notes = value.notes
            elif isinstance(value, Chord):
                _notes = value.notes
            else:
                # handle uniqueness
                is_unique = (len(set(value)) == len(value))
                if not is_unique:
                    if self.force_unique:
                        value = list(set(value))
                    else:
                        e = "All notes in a Chord must be unique. Set Chord.force_unique to True to automatically enforce \
                        uniqueness."
                        raise ValueError(e)

                # at least 2 notes
                if len(value) < 2:
                    e = "Chord must be given at least two notes."
                    raise ValueError(e)

                # all Note types
                _notes = list()
                for n in value:
                    if not isinstance(n, Note):
                        try:
                            n = Note(n)
                            _notes.append(n)
                        except:
                            raise
                    else:
                        _notes.append(n)

                # ascending order
                _notes = sorted(_notes)

        # self.notes is None
        else:
            _notes = []

        self._notes = _notes

    #### UTILITY METHODS ####

    def append_note(self, note: Note):
        if not isinstance(note, Note):
            e = "`item` must be a `Note` object."
            raise ValueError(e)

        _notes = self.notes
        _notes.append(note)
        _notes = sorted(_notes)
        self.notes = _notes

        return self

    def invert(self, direction: str = "up", n: int = 1):

        _notes = deepcopy(self.notes)

        for _ in range(n):

            if direction == "up":
                top = _notes[-1]
                bottom = _notes.pop(0)
                while bottom < top:
                    bottom += 12
                _notes.append(bottom)
            elif direction == "down":
                top = _notes.pop(-1)
                bottom = _notes[0]
                while top > bottom:
                    top -= 12
                _notes.insert(0, top)
            else:
                e = "`direction` must be either 'up' or 'down'."
                raise ValueError(e)
        chord = Chord(notes=_notes)

        return chord

    def compress_to_range(self,
                          a: Union[Note, Any],
                          b: Union[Note, Any]):
        """
        If not in given range, transpose outer notes such that Chord is in range.
        """
        try:
            notes = sorted([to_note(n) for n in [a, b]])
        except:
            raise

        val_range = range(notes[0].value, notes[-1].value + 1)

        _min = val_range.start
        _max = val_range.stop + 1
        compressed = []
        for n in self.notes:
            if n > _max:
                while n not in val_range:
                    n -= 12
                    if n < _min:
                        e = f"Note `{n.as_letter(include_range=False)}` cannot be compressed into range `({Note(_min)},{Note(_max)}`. "
                        raise ValueError(e)
                compressed.append(n)
            elif n < _min:
                while n not in val_range:
                    n += 12
                    if n > _max:
                        e = f"Note `{n.as_letter(include_range=False)}` cannot be compressed into range `({Note(_min)},{Note(_max)})`. "
                        raise ValueError(e)
                compressed.append(n)
            else:
                compressed.append(n)

        return Chord(compressed)

    def __getitem__(self, item: int):
        return self.notes[item]

    def __len__(self):
        return len(self.notes)

    def __contains__(self, item: Note):
        if item in self.notes:
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, Chord):
            if self.notes == other.notes:
                return True
            else:
                return False
        return False

    def __repr__(self):
        r = "Chord("
        for i, n in enumerate(self):
            if i == len(self) - 1:
                r += str(n.as_letter()) + ")"
            else:
                r += str(n.as_letter()) + ", "
        return r

