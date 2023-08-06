import random
from typing import Optional, Union, Sequence, List

import numpy as np

from MidiCompose.logic.harmony.note import Note
from MidiCompose.logic.harmony.interval import Interval
from MidiCompose.utilities import temp_seed


class NoteSetIterator:
    def __init__(self, note_set):
        self._NoteSet = note_set
        self._index = 0

    def __next__(self) -> Note:
        if self._index < len(self._NoteSet):
            result = self._NoteSet[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration


class NoteSet:
    """
    Set of ordered unique `Note` objects with utility functions for generating and sampling.
    """

    def __init__(self,
                 notes: Optional[Union[Sequence[Note], Sequence[int]]] = None,
                 force_unique: bool = False,
                 verbose: bool = False,
                 accidental: Optional[str] = None):

        self.force_unique = force_unique  # must be called before `notes` setter
        self.notes = notes  # calls setter

        self.verbose = verbose
        self.accidental = accidental

    @property
    def notes(self) -> List[Note]:
        return self._notes

    @notes.setter
    def notes(self, value):

        if value is None:  # return object array with size 0
            self._notes = list()

        else:
            value_typeset = set([type(v) for v in value])

            # validate uniqueness
            value_set = set(value)
            if len(value_set) != len(value):
                if self.force_unique:
                    value = [v for v in value_set]
                else:
                    msg = "All notes in `NoteSet` must be unique. To convert a non-unique collection," \
                          "set `force_unique` to True."
                    raise ValueError(msg)

            if value_typeset.issubset({int}):  # sequence of integers
                self._notes = sorted([Note(v) for v in value])
            elif value_typeset.issubset({Note}):
                self._notes = sorted([v for v in value])
            elif value_typeset.issuperset({Note, int}):  # ints and Notes
                _notes = []
                for v in value:
                    if type(v) == int:
                        _notes.append(Note(v))
                    elif type(v) == Note:
                        _notes.append(v)
                self._notes = sorted(_notes)

            else:
                msg = "`notes` must either be a Sequence of `Note` objects, a Sequence of integers," \
                      "or a combination thereof."
                raise ValueError(msg)

    def as_letters(self) -> List[str]:
        """
        Returns NoteSet as letter notes
        """
        letters = [str(n) for n in self.notes]
        return letters

    # TODO
    def expand_range(self):
        pass

    # TODO
    def truncate_range(self, a: Note, b: Note):
        """
        Keeps all notes in current NoteSet, but truncates outer notes given `a` and `b`.
        """
        if not isinstance(a,Note) and isinstance(b,Note):
            "`a` and `b` must be `Note` objects."
            raise KeyError()
        if not a < b:
            e = "`a` must be lower than `b`."
            raise ValueError(e)

        _notes = [n for n in self.notes if a <= n <= b]

        self.notes = _notes

        return self

    #### UTILITY METHODS ####

    def random_sample(self, n: Optional[int] = None,
                      start: Optional[Note] = None,
                      random_seed: Optional[int] = None,
                      _cycle: bool = True,
                      _cycle_start: bool = False) -> List[Note]:
        """
        Returns randomly selected sample (no replacement) from `NoteSet`.

        :param n: Sample size.
        :param start: `Note` object to start sample with.
        :param random_seed: Optional random seed for reproducibility.
        :param _cycle: If True, `n` is larger than size of `NoteSet`, will re-sample as necessary.
        :param _cycle_start: If True, and conditions for `_cycle` exist, the same starting `Note`
                             will be used at the beginning of each cycle.
        """
        _sample = list()

        ## SET/VALIDATE ARGUMENTS ##

        # get sample size
        if n is None:
            _size = len(self.notes)
        else:
            _size = n

        # get random random_seed
        if random_seed is None:
            _seed = random.randint(0, 10 ** 3)
        else:
            _seed = random_seed

        # validate starting item
        if start is None:
            _start = None
            _set_start_removed = None
            _cycle_start = None
        else:
            if start not in self.notes:
                msg = "The item given for `start` is not in the NoteSet."
                raise ValueError(msg)
            else:
                _start = start

                idx_start_removed = [n for n in range(len(self.notes))
                                     if n != self.notes.index(_start)]
                _set_start_removed = [self.notes[i] for i in idx_start_removed]

                _cycle_start = _cycle_start

        ## GET SAMPLE ##
        with temp_seed(_seed):
            # if requested sample size is larger than set
            if _size > len(self):
                if _cycle is False:
                    msg = "If `n` as a larger than the NoteSet, `_cycle` must be True."
                    raise ValueError(msg)
                else:
                    n_cycles, remainder = divmod(_size, len(self))
                    if _start is not None:
                        if _cycle_start:  # use same starting item each cycle
                            for _ in range(n_cycles):
                                _sample.append(_start)
                                _sample.extend(np.random.choice(_set_start_removed,
                                                                size=len(self) - 1,
                                                                replace=False))
                        else:  # enforce starting item only first cycle
                            _sample.append(_start)
                            _sample.extend(np.random.choice(_set_start_removed,
                                                            size=len(self) - 1,
                                                            replace=False))
                            for _ in range(n_cycles - 1):
                                _sample.extend(np.random.choice(self.notes,
                                                                size=len(self.notes),
                                                                replace=False))
                        if remainder > 0:
                            _sample.append(_start)
                            _sample.extend(np.random.choice(_set_start_removed,
                                                            size=remainder - 1,
                                                            replace=False))
                    elif _start is None:
                        for _ in range(n_cycles):
                            _sample.extend(np.random.choice(self.notes,
                                                            size=len(self.notes),
                                                            replace=False))
                        if remainder > 0:
                            _sample.extend(np.random.choice(self.notes,
                                                            size=remainder,
                                                            replace=False))

            elif _size <= len(self):
                if _start is None:
                    _sample.extend(np.random.choice(self.notes, size=_size, replace=False))
                else:
                    _sample.append(_start)
                    _sample.extend(np.random.choice(_set_start_removed, size=_size - 1, replace=False))

        return list(_sample)

    def random_select(self, random_seed: Optional[int] = None) -> Note:
        """
        Randomly select one item from NoteSet.
        """
        if random_seed is not None:
            with temp_seed(random_seed):
                note = np.random.choice(self.notes, 1)[0]
        else:
            note = np.random.choice(self.notes, 1)[0]

        return note

    def from_scale(self,
                   tonic: Note,
                   scale: list,
                   range_above: Interval = Interval(12),
                   range_below: Interval = Interval(0)):
        """
        Sets self to requested scale.
        """

        _max_note = range_above.above(tonic)
        _min_note = range_below.below(tonic)

        _notes = [tonic]
        highest = _notes[-1]

        idx = 0
        while highest < _max_note:
            if idx == len(scale):
                idx = 0
            note = Interval(scale[idx]).above(highest)
            _notes.append(note)

            highest = _notes[-1]
            idx += 1

        lowest = _notes[0]
        idx = 0
        cp_scale = scale[:]  # copy and reverse scale
        cp_scale.reverse()
        while lowest > _min_note:
            if idx == len(scale):
                idx = 0
            _notes.insert(0, Interval(cp_scale[idx]).below(_notes[0]))
            lowest = _notes[0]
            idx -= 1

        self.notes = _notes

        return self

    def from_range(self, a: Note, b: Note):
        """Get all notes between `a` and `b`. Inclusive."""

        if not isinstance(a,Note) and isinstance(b,Note):
            "`a` and `b` must be `Note` objects."
            raise KeyError()
        if not a < b:
            e = "`a` must be lower than `b`."
            raise ValueError(e)

        _notes = [Note(v) for v in list(range(a.value,b.value+1))]
        self.notes = _notes

        return self







    #### SPECIAL METHODS ####
    def __getitem__(self, item: int) -> Note:
        return self.notes[item]

    def __len__(self):
        return len(self.notes)

    def __iter__(self):
        return NoteSetIterator(self)

    def __eq__(self, other):
        if isinstance(other, NoteSet):
            return self.notes == other.notes
        return NotImplemented

    def __repr__(self):
        r = "NoteSet("
        r += ", ".join([str(n.value) for n in self.notes])
        r += ")"
        if self.verbose:
            r += "\n       ("
            r += ", ".join([n.as_letter(accidental=self.accidental) for n in self.notes])
            r += ")"
        return r


