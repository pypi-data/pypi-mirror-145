from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from itertools import chain
import random
from typing import Optional, Union, List, Tuple, Sequence, Any
from abc import ABC, abstractmethod
import bisect

from icecream import ic

from MidiCompose.logic.harmony.interval import Interval, sequence_to_intervals
from MidiCompose.logic.harmony.key import Key
from MidiCompose.logic.harmony.note import Note, to_note, HasNotes, sequence_to_notes


class AbstractBaseFiguredNote(ABC):

    @property
    @abstractmethod
    def note(self) -> Note: pass

    @note.setter
    @abstractmethod
    def note(self, note) -> None: pass

    @property
    @abstractmethod
    def figure(self) -> List[int]: pass

    @figure.setter
    @abstractmethod
    def figure(self, value) -> None: pass

    @property
    @abstractmethod
    def index(self) -> int: pass

    @index.setter
    @abstractmethod
    def index(self,value) -> None: pass

    @property
    @abstractmethod
    def bass(self) -> Note: pass

    @property
    @abstractmethod
    def notes(self) -> List[Note]: pass

class BaseFiguredNoteIterator:
    def __init__(self, base_figure: BaseFiguredNote):
        self. _base_figure = base_figure
        self._index = 0
    def __next__(self):
        if self._index < len(self._base_figure.notes):
            return self._base_figure.notes[self._index]
        else:
            raise StopIteration


class BaseFiguredNote(AbstractBaseFiguredNote):

    def __init__(self,
                 note: Note | Any,
                 figure: Sequence[int],
                 index: int = 0):

        self.note = note
        self.figure = figure
        self.index = index

    @property
    def note(self) -> Note: return self._note

    @note.setter
    def note(self, note: Note|Any):
        try:
            self._note = to_note(note)
        except:
            raise

    @property
    def figure(self) -> List[int]: return self._figure

    @figure.setter
    def figure(self, figure: Sequence[int]):

        seq_of_ints: bool = all([isinstance(i,int) for i in figure])
        if not seq_of_ints:
            e = "Parameter `figure` must be given as a sequence of integers."
            raise ValueError(e)

        _figure = sorted(list(set(figure)))
        if _figure[0] != 0:
            _figure = [0] + _figure

        self._figure = _figure

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, index: int) -> None:


        _figure = self.figure

        if index >= len(_figure):
            e = f"Argument `{index}` given to Parameter `index` out of range for `figure` of length {len(_figure)}."
            raise ValueError(e)
        else:
            self._index = index

    @property
    def bass(self) -> Note:
        raise NotImplementedError

    @property
    def notes(self) -> List[Note]:
        return []

    def __iter__(self):
        return BaseFiguredNoteIterator(self)

    def __getitem__(self, item: int) -> Note:
        return self.notes[item]

    def __repr__(self):
        r = f"BaseFigure(note={self.note}, index={self.index}, figure={self.figure})"
        return r


class ChromaticFiguredNote(BaseFiguredNote):
    def __init__(self, note: Note | Any, figure: Sequence[int], index: int = 0):
        super().__init__(note=note, figure=figure, index=index)

    @property
    def bass(self) -> Note:
        return Interval(self.figure[self.index]).below(self.note)

    @property
    def notes(self) -> List[Note]:
        _notes = [self.bass + n for n in self.figure]
        return _notes

    def __repr__(self):
        r = f"ChromaticFigure(note={self.note}, figure={self.figure}, index={self.index}, notes={self.notes})"
        return r

class TonalFiguredNote(BaseFiguredNote):

    def __init__(self, note: Note | Any,
                 key: Key | Any,
                 figure: Sequence[int],
                 index: int = 0):
        super().__init__(note=note, figure=figure, index=index)
        self.key = key

    @property
    def key(self) -> Key: return self._key

    @key.setter
    def key(self, key):
        try:
            _key = Key(**Key.parse(key))
        except:
            raise

        if self.note not in _key:
            e = f"The indexed Note `{self.note}` is not in the given Key `{_key}`."
            raise ValueError(e)

        self._key = _key

    @property
    def bass(self) -> Note:
        _index,_figure,_key,_note = self.index,self.figure,self.key,self.note

        if _index == 0:
            bass = _note
        else:
            steps_above_bass = _figure[_index] - 1
            bass = _key.steps_below(_note, steps=steps_above_bass)

        return bass

    @property
    def notes(self) -> List[Note]:
        return [self.bass] +\
               [self.key.steps_above(note=self.bass,steps=n - 1) for n in self.figure[1:]]

    def __repr__(self):
        _note = self.note.as_letter()
        _key = self.key.tonic.as_letter(include_range=False) + " " + self.key.key_name
        return f"TonalFiguredNote('{_note}', index={self.index}, figure={self.figure[1:]}, key='{_key}', notes={self.notes})"


if __name__ == '__main__':
    NOTE = Note("C3")
    FIGURE = [3,5]
    KEY = Key("C")
    IDX = 1

    bf = BaseFiguredNote(note=NOTE, figure=FIGURE, index=IDX)
    print(bf)

    cf = ChromaticFiguredNote(note=NOTE, figure=FIGURE, index=IDX)
    print(cf)

    tf = TonalFiguredNote(note=NOTE, figure=FIGURE, index=IDX, key=KEY)
    print(tf)

    print(cf[1],tf[1:])