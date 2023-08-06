import contextlib
from abc import ABC, abstractmethod
from copy import copy, deepcopy
from dataclasses import dataclass
from itertools import cycle
from pprint import pprint
from typing import Dict, Union, Sequence, Any, List
import random

from icecream import ic
from mido import MidiFile, Message, bpm2tempo, MetaMessage

from MidiCompose.logic.harmony.figure import TonalFiguredNote
from MidiCompose.logic.harmony.key import Key, KeySchema

from itertools import chain

# EVOLVING TRIADS
from MidiCompose.logic.harmony.note import Note
from MidiCompose.logic.harmony.chord import Chord

from typing_extensions import Protocol

class HasNotes(Protocol):
    notes: List[Note]

class ChordTransformer:
    def __init__(self, chord: HasNotes) -> None:
        self.original: Chord = Chord(chord)
        self.current: Chord = Chord(chord)


    def __repr__(self):
        _orig = self.original
        _current = self.current
        r = f"ChordTransformer(original={_orig}, current={self.current})"
        return r

class DefaultFilters:

    def n_voices(self, other: HasNotes) -> int:
        """
        Retain same number of notes
        """
        return len(set(other.notes))


if __name__ == '__main__':
    ch = TonalFiguredNote("C3",Key("C MAJOR"),figure=[3,5])
    print(ch)

    cg = ChordTransformer(ch)
    filters = [
        ("keep_voices",[0,1]),
        ("include_interval")
    ]
    print(cg)