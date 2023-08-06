import sys
from typing import Union, Optional, List, Sequence, Tuple

from icecream import ic

from MidiCompose.logic.harmony import interval_mapping as imap
from MidiCompose.logic.harmony.note import Note


class Interval:
    """
    The distance between two note_vals.

    Can be uniquely identified by:
        - `hs`: number of halfsteps
        - `string`: string representation...eg] "M3+" -> "major third up an octave" -> 16 half-steps

    Either of the unique representations can be supplied as an argument to the constructor.
    """

    def __init__(self, interval: Union[int, str], verbose: bool = True):
        """

        :param interval: Takes one of two options:
                            1) number of half steps (integer)
                            2) string representation...eg] "M3", "P5+", etc.
        :param verbose: If True, __repr__ gives more info.
        """

        # full representations
        self.hs: Optional[int] = None
        self.string: Optional[str] = None

        # individual attributes
        self.quality: Optional[str] = None
        self.value: Optional[int] = None
        self.octave_shift: Optional[int] = None

        # verbosity of __repr__
        self.verbose: bool = verbose

        self._parse_interval_arg(interval)

    def _parse_interval_arg(self, interval: Union[int, str]):

        if isinstance(interval, int):
            if interval not in range(0, 128):
                msg = f"Interval `{interval}` out of range."
                raise ValueError(msg)

            self.hs = interval
            self.string = imap.INTERVAL_MAPPER[self.hs]

        elif isinstance(interval, str):
            try:
                self.string = interval
                self.hs = imap.INTERVAL_MAPPER[interval]
            except:
                msg = f"Interval `{interval}` is an invalid string representation."
                raise ValueError(msg)

        else:
            msg = "Parameter `intervals` must be given either an integer of half-steps, or a" \
                  "string representation of an intervals."
            raise TypeError(msg)

        # set individual attributes
        self.quality = self.string[0]
        self.value = int(self.string[1])
        self.octave_shift = len(self.string[2:])

    #### MAGIC METHODS ####

    def __eq__(self, other):
        if self.hs == other.hs:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.hs < other.hs:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.hs > other.hs:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.hs >= other.hs:
            return True
        else:
            return False

    def __le__(self, other):
        if self.hs <= other.hs:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.hs != other.hs:
            return True
        else:
            return False

    def __add__(self, other):
        if type(other) == type(self):
            return Interval(self.hs + other.hs)
        elif isinstance(other, int):
            return Interval(self.hs + other)

    def __sub__(self, other):
        if type(other) == type(self):
            return Interval(self.hs - other.hs)
        elif isinstance(other, int):
            return Interval(self.hs - other)

    def __repr__(self):
        if self.verbose:
            header = "Interval("
            string_rep = f'string = "{self.string}", '
            quality = f'quality = "{str(self.quality)}", '
            value = f"value = {str(self.value)}, "
            octave_shift = f"octave_shift = {str(self.octave_shift)}, "
            hs = f"hs = {str(self.hs)}"
            footer = ")"

            r = header + string_rep + quality + value + octave_shift + hs + footer

            return r

        else:
            r = f'"{self.string}"'
            return r

    #### UTILITY METHODS ####
    def above(self, note: Union[Note, int, str]) -> Note:
        """
        Given a valid item representation, return a Note object at the appropriate intervals.

        :param note: Note object or valid "Note-like" representation.
        :return: Note object at the appropriate intervals.
        """
        # coerce to Note object
        if not isinstance(note, Note):
            if isinstance(note, int):
                note = int(note)
            try:
                note = Note(note)
            except:
                msg = f"`{note}` is an invalid argument."
                raise ValueError(msg)

        result_value = int(note.value + self.hs)
        result_note = Note(result_value)

        return result_note

    def below(self, note: Union[Note, int, str]) -> Note:
        """
        Given a valid item representation, return a Note object at the appropriate intervals.

        :param note: Note object or valid "Note-like" representation.
        :return: Note object at the appropriate intervals.
        """

        # coerce to Note object
        if not isinstance(note, Note):
            try:
                note = Note(note)
            except:
                msg = f"`{note}` is an invalid argument."
                raise ValueError(msg)

        result_value = int(note.value - self.hs)

        return Note(result_value)

    @staticmethod
    def from_notes(a, b):

        notes = [a, b]
        for i, n in enumerate(notes):
            if not isinstance(n, Note):
                try:
                    notes[i] = Note(a)
                except:
                    e = f"Value `{b}` is not a valid `Note` or Note-like object."
                    raise ValueError(e)

        dif = abs(notes[0].value - notes[1].value)

        return Interval(dif)

    @staticmethod
    def get(quality: str,
            value: int,
            octave_shift: Optional[int] = None):

        _qualities = ["m", "M", "P", "A"]
        if quality not in _qualities:
            e = f"Invalid `quality`. Options are: {_qualities}"
            raise ValueError(e)

        _values = range(8)
        if value not in _values:
            e = f"Invalid `value`. Options are: {list(_values)}"
            raise ValueError(e)

        if octave_shift:
            _oct_shift = range(11)
            if octave_shift not in _oct_shift:
                e = f"Invalid `octave_shift`. Options are {list(_oct_shift)}"
                raise ValueError(e)

        _str = quality + str(value)
        if octave_shift:
            _shift = "+" * octave_shift
            _str += _shift
        try:
            interv = Interval(_str)
            return interv

        except:
            raise


class IntervalRange:
    """
    Inclusive range of Interval objects from `a` to `b` where both `a` and `b` are Intervals.

    Includes utility functions for excluding intervals based on various conditions.
    """

    def __init__(self,
                 a: Optional[Union[Interval, str, int]] = None,
                 b: Optional[Union[Interval, str, int]] = None):

        self.intervals = (a, b)  # calls setter

    @property
    def intervals(self) -> List[Interval]:
        return self._intervals

    @intervals.setter
    def intervals(self, value):

        if any([v is None for v in value]):
            _intervals = []
        else:
            try:
                _intervals = sequence_to_intervals(value)
            except:
                raise

            smallest = min(_intervals).hs
            largest = max(_intervals).hs

            _intervals = [Interval(hs) for hs in range(smallest, largest + 1)]

        self._intervals = _intervals

    @property
    def smallest(self):
        return min(self.intervals)

    @property
    def largest(self):
        return max(self.intervals)

    def get(self) -> List[Interval]:
        """
        Returns list of intervals for current figure of IntervalRange
        """
        return self.intervals

    #### FILTERING ####

    def exclude_intervals(self,
                          intervals: Sequence[Interval],
                          exclude_octaves: bool = False,
                          octave_indexes: Optional[Sequence[int]] = None):
        """

        :param intervals:
        :param exclude_octaves: if True, exclude octave-equivalents of given interval.
        :param octave_indexes: only applies if `exclude_octaves` == True. Sequence of octave indexes to exclude.
        :return: self
        """
        _intervals = self._intervals

        # remove exact intervals given
        for interv in intervals:
            if interv in _intervals:
                _intervals.remove(interv)

        # handle octave equivalents
        if exclude_octaves:
            if octave_indexes:
                print("implement octave exclusion by index")
            else:  # exclude all octave equivalents
                for interv in intervals:
                    while interv <= self.largest and interv.hs + 12 <= 126:
                        if interv in _intervals:
                            _intervals.remove(interv)
                        interv += 12

        self._intervals = _intervals
        return self

    def exclude_qualities(self, qualities: Sequence[str]):

        valid_quality_set = {"m", "M", "P", "A"}
        given_quality_set = set(qualities)
        if not given_quality_set.issubset(valid_quality_set):
            e = f"Invalid qualities. Valid arguments include: {valid_quality_set}"
            raise ValueError(e)

        _intervals = list()
        for interv in self.intervals:
            if interv.quality not in qualities:
                _intervals.append(interv)

        self._intervals = _intervals
        return self

    def include_values(self, values: Sequence[int]):

        if not all([v in [1, 2, 3, 4, 5, 6, 7] for v in values]):
            e = "Values can only be {0,2,3,4,5,6,7}"
            raise ValueError(e)

        _intervals = []
        for interv in self.intervals:
            if interv.value in values:
                _intervals.append(interv)

        self._intervals = _intervals
        return self

    def include_qualities(self, qualities: Sequence[str]):

        if not all([q in ["M", "m", "P", "A"] for q in qualities]):
            e = "Argument `qualities` must be in {M,m,P,A}"
            raise ValueError(e)

        _intervals = []
        for interval in self.intervals:
            if interval.quality in qualities:
                _intervals.append(interval)

        self._intervals = _intervals
        return self

    def from_values(self,
                    values: Sequence[int],
                    octave_indexes: Optional[Sequence[int]] = None):

        if octave_indexes is None:
            octave_indexes = [0]
        if not all([idx in list(range(0,11)) for idx in octave_indexes]):
            e = f"`octave_indexes` must be in between 0 and 10."
            raise ValueError(e)

        # get all octaves
        all_octaves = []
        for _oct in octave_indexes:
            _intervs = IntervalRange(a=0 + (12*_oct),b=11 + (12*_oct))
            all_octaves.extend(_intervs.intervals)

        # filter octaves by values
        filtered = []
        for v in values:
            for interv in all_octaves:
                if interv.value == v:
                    filtered.append(interv)

        self._intervals = filtered
        return self

    def __getitem__(self, item):
        try:
            _interv = self.intervals[item]
        except:
            raise
        return _interv

    def __repr__(self):
        r = f"IntervalRange("
        for i,interv in enumerate(self.intervals):
            if i == len(self.intervals) - 1:
                r += f"\n    {interv}"
            else:
                r += f"\n    {interv}"
        r += ")"
        return r


#### VALIDATORS ####

def is_interval_like(interval_like) -> bool:
    if isinstance(interval_like,Interval):
        return True
    elif (
            isinstance(interval_like,int) and
            0 <= interval_like < 127
    ):
        return True

def to_interval(interval_like) -> Interval:

    if isinstance(interval_like, Interval):
        return interval_like

    elif isinstance(interval_like, str):
        try:
            _hs = imap.INTERVAL_MAPPER[interval_like]
            _interv = Interval(_hs)
        except:
            e = f"Unable to interpret `{interval_like}` as an Interval."
            raise ValueError(e)

    elif isinstance(interval_like, int):
        try:
            _interv = Interval(interval_like)
        except:
            e = f"Unable to interpret `{interval_like}` as an Interval."
            raise ValueError(e)

    else:
        e = f"Unable to interpret `{interval_like}` as an Interval."
        raise ValueError(e)

    return _interv

def sequence_to_intervals(s: Sequence) -> List[Interval]:
    _intervs = []
    for interv in s:
        try:
            _interv = to_interval(interv)
            _intervs.append(_interv)
        except:
            raise

    return _intervs
