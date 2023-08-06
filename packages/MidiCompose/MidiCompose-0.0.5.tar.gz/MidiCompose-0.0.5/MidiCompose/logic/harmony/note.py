from __future__ import annotations

from copy import deepcopy
import random
from typing import Union, Optional, List, Sequence, Set, Any
from icecream import ic
from typing_extensions import runtime_checkable, Protocol

from MidiCompose.logic.harmony import note_mapping as nm
from MidiCompose.utilities import temp_seed, ctx_random_seed


class Note:
    """Represents a midi-value from_note.

    A midi from_note is Fundamentally represented by an integer between 0 and 127.

    Attributes
    ----
    value : `int`
        Integer value representing midi-from_note.

    signature : `int`
        Integer value of midi-from_note, compressed to the bottom octave.
    """

    def __init__(self, note: Union[int, str], accidental: Optional[str] = None):
        """
        :param note: - Either an integer between (0-127)
                     - or a letter-representation between ("C-2" and "G8")
        """
        self.value: int = note  # calls setter
        self.accidental = accidental  # calls setter

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v: Union[int, str]):

        if type(v) == int:
            if v not in range(128):
                msg = "`item` must be within range (0-127) if being passed as an integer."
                raise ValueError(msg)
            else:
                self._value = v

        elif type(v) == str:
            self._value = int(nm.letter_to_value(v))

        else:
            msg = "Invalid argument. `item` must be a valid integer or string representation of a item."
            raise ValueError(msg)

    @property
    def accidental(self):
        return self._accidental

    @accidental.setter
    def accidental(self, v: Optional[str] = None):
        if v not in {None, "sharp", "flat"}:
            msg = f"Invalid argument for `Note.accidental`. `accidental` must be one of {{None,'sharp','flat'}}. Given {v} "
            raise ValueError(msg)
        else:
            self._accidental = v

    @property
    def signature(self) -> int:
        """
        Returns the integer "signature" of the from_note, regardless of range.

        That is {C-2,C0,C4,...} = 0
        """
        return self.value % 12

    #### UTILITY METHODS ####
    def as_letter(self,
                  accidental: Optional[str] = None,
                  include_range: bool = True) -> str:
        """
        Returns letter representation of Note.
        """
        letter = nm.value_to_letter(value=self.value,
                                    accidental=accidental)

        if not include_range:
            if letter[1] in ["#","b"]:
                letter = letter[:2]
            else:
                letter = letter[0]


        return letter

    def to_register(self, register: int):
        """
        Returns the same from_note in the specified range.

        :param register: Integer between (-2,8)
        """
        if register not in range(-2, 9):
            e = f"`register` must be between (-2,8)"
            raise ValueError(e)

        _note = deepcopy(self)

        _reg = register + 2
        _val = (_note.value % 12) + (_reg * 12)
        _note = Note(_val)

        return _note

        #### SPECIAL METHODS ####

    def to_range(self,
                 a: Note,
                 b: Note,
                 selection_criteria: str = "random",
                 seed: int = None) -> Note:
        """

        :param a:
        :param b:
        :param selection_criteria: {"lowest","highest","random"}
        :param seed: random seed for reproducibility
        :return:
        """
        try:
            a,b = to_note(a),to_note(b)
        except:
            raise

        _note = self
        _sig = _note.signature

        range_ = Note.range(a,b)
        if _note in range_:
            return _note

        notes_in_range = sorted([n for n in range_ if n.signature == _sig])
        if len(notes_in_range) == 0:
            e = f"Note {_note.as_letter(include_range=False)} does not exist between {a} and {b}."
            raise ValueError(e)
        elif selection_criteria == "lowest":
            note = notes_in_range[0]
        elif selection_criteria == "highest":
            note = notes_in_range[-1]
        elif selection_criteria == "random":
            with ctx_random_seed(seed):
                note = random.choice(notes_in_range)

        return note

    def nearest_neighbors(self,
                          note: Union[int,str,Any],
                          direction: Optional[str] = None):
        """

        :param note:
        :param direction: Either "UPPER" or "LOWER". If None, returns both.
        :return:
        """

        try:
            _note = to_note(note)
        except:
            raise

        if _note.signature == self.signature:
            return self

        _sig = _note.signature

        _upper = self
        while _upper.signature != _sig:
            _upper += 1
        _lower = self
        while _lower.signature != _sig:
            _lower -= 1

        if direction:
            if direction.upper() == "UPPER":
                return _upper
            elif direction.upper() == "LOWER":
                return _lower
            else:
                e = "Argument `direction` takes one of: ['UPPER','LOWER',None]"
                raise ValueError(e)

        else:
            return _lower,_upper

    #### STATIC METHODS ####

    @staticmethod
    def range(a,b):
        """
        Returns list of notes between a and b (inclusive). Order is preserved.
        """
        try:
            _a = to_note(a)
            _b = to_note(b)
        except:
            raise

        if _a == _b:
            notes = [_a]
        elif _a < _b:
            notes = []
            for i in range(_a.value,_b.value + 1):
                notes.append(Note(i))
        else:
            notes = []
            for i in range(_a.value,_b.value-1,-1):
                notes.append(Note(i))

        return notes

    def __eq__(self, other):
        if type(other) == int:
            if self.value == other:
                return True
            else:
                return False
        else:
            if self.value == other.value:
                return True
            else:
                return False

    def __hash__(self):
        return hash(self.value)

    def __lt__(self, other):
        if type(other) == int:
            if self.value < other:
                return True
            else:
                return False

        elif type(other) == Note:
            if self.value < other.value:
                return True
            else:
                return False

    def __gt__(self, other):
        if type(other) == int:
            if self.value > other:
                return True
            else:
                return False

        else:
            if self.value > other.value:
                return True
            else:
                return False

    def __le__(self, other):
        if type(other) == int:
            if self.value <= other:
                return True
            else:
                return False
        else:
            if self.value <= other.value:
                return True
            else:
                return False

    def __ge__(self, other):
        if type(other) == int:
            if self.value >= other:
                return True
            else:
                return False
        else:
            if self.value >= other.value:
                return True
            else:
                return False

    def __ne__(self, other):
        if self.value != other.value:
            return True
        else:
            return False

    def __add__(self, other):
        if type(other) == int:
            value = self.value + other
        else:
            value = self.value + other.value
        try:
            return Note(value)
        except:
            msg = f"The value `{value}` produced by the operation resulted in an invalid midi-value."
            raise ValueError(msg)

    def __sub__(self, other):
        if type(other) == int:
            value = self.value - other
        else:
            value = self.value + other.value

        return Note(value)

    def __repr__(self):
        r = f"Note({self.as_letter()})"
        return r


@runtime_checkable
class HasNotes(Protocol):

    def notes(self) -> Sequence[Note]:
        ...

#### VALIDATORS ####

def to_note(note_like) -> Note:
    _valid_type = (isinstance(note_like, Note)) or \
                  (isinstance(note_like, int)) or \
                  (isinstance(note_like, str))
    if not _valid_type:
        e = "Note instances can be constructed from {Note,int,str} objects."
        raise TypeError(e)

    if isinstance(note_like, Note):
        _n = note_like
    else:
        try:
            _n = Note(note_like)
        except:
            e = f"Unable to interpret `{note_like}` as a Note-like object."
            raise ValueError(e)

    return _n

def sequence_to_notes(s: Sequence) -> List[Note]:
    _notes = []
    for n in s:
        try:
            _notes.append(to_note(n))
        except:
            e = "Invalid sequence of Note-like objects."
            raise ValueError(e)
    return _notes