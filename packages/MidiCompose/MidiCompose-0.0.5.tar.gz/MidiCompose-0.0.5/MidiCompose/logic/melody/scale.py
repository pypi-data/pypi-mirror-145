from dataclasses import dataclass
from itertools import cycle
from typing import Union, List, Tuple, Optional, Any

from MidiCompose.logic.harmony.note import Note

@dataclass
class DiatonicModes:

    IONIAN = [2, 2, 1, 2, 2, 2, 1]
    DORIAN = [2, 1, 2, 2, 2, 1, 2]
    PHRYGIAN = [1, 2, 2, 2, 1, 2, 2]
    LYDIAN = [2, 2, 2, 1, 2, 2, 1]
    MIXOLYDIAN = [2, 2, 1, 2, 2, 1, 2]
    AEOLIAN = [2, 1, 2, 2, 1, 2, 2]
    LOCRIAN = [1, 2, 2, 1, 2, 2, 2]

    # aliases
    MAJOR = IONIAN
    MINOR = AEOLIAN

@dataclass
class NonDiatonicModes:
    MELODIC_MINOR = [2,1,2,2,2,2,1]
    HARMONIC_MINOR = [2,1,2,2,1,3,1]
    WHOLE_TONE = [2,2,2,2,2,2]
    DIMINISHED_HW = [1,2,1,2,1,2,1,2]
    DIMINISHED_WH = [2,1,2,1,2,1,2,1]

@dataclass
class AllModes(DiatonicModes,NonDiatonicModes):
    pass

class Scale:

    def __init__(self,
                 tonic: Union[Note,int,str],
                 mode: str = "MAJOR",
                 note_range: Optional[Tuple[Any,Any]] = None):
        """
        By default, returns single octave starting at `tonic`.
        """
        self.tonic = tonic  # setter
        self.mode = mode  # setter
        self.note_range = note_range  # setter

    @property
    def tonic(self):
        return self._tonic

    @tonic.setter
    def tonic(self,tonic):
        if not isinstance(tonic,Note):
            try:
                _tonic = Note(tonic)
            except:
                raise
        else:
            _tonic = tonic

        self._tonic = _tonic

    @property
    def mode(self) -> List[int]:
        return self._mode

    @mode.setter
    def mode(self,mode):

        if not hasattr(AllModes,mode):
            e = "Invald name for `mode`. See AllModes object for possibilites."
            raise ValueError(e)
        else:
            _mode = getattr(AllModes,mode)
        self._mode = _mode

    @property
    def note_range(self) -> Tuple[Note,Note]:
        return self._note_range

    @note_range.setter
    def note_range(self,note_range):

        if note_range is None:
            _lower = self.tonic
            _upper = _lower + Note(12 - self.mode[-1])
            note_range = (_lower,_upper)

        elif not len(note_range) == 2:
            e = "`note_range` must be a tuple of 2 ascending notes."
            raise ValueError(e)

        elif not all([isinstance(n, Note) for n in note_range]):
            try:
                note_range = tuple([Note(n) for n in note_range])
            except:
                raise

        elif not note_range[0] < note_range[1]:
            e = "`note_range` must be a tuple of 2 ascending notes."
            raise ValueError(e)

        _lower = note_range[0]
        while not self.note_in_key(note=_lower):
            _lower += 1
        _upper = note_range[1]
        while not self.note_in_key(note=_upper):
            _upper -= 1

        self._note_range = (_lower,_upper)

    @property
    def scale(self) -> List[Note]:

        _lower = self.note_range[0]
        _upper = self.note_range[1]

        _scale = [_lower]
        for interv in cycle(self.mode):
            next_note = _scale[-1] + interv
            if _scale[-1] >= _upper:
                break
            else:
                _scale.append(_scale[-1] + interv)

        return _scale

    def note_in_key(self, note: Union[Note,int,str]):

        if not isinstance(note,Note):
            try:
                note = Note(note)
            except:
                raise

        tonic_compressed = self.tonic.value % 12
        note_compressed = (note.value % 12)

        if note_compressed < tonic_compressed:
            note_compressed += 12

        _current = tonic_compressed
        for hs in self.mode:
            if _current == note_compressed:
                return True
            else:
                _current += hs

        return False

    def degree_of_note(self, note: Union[Note,int,str]) -> int:

        if not isinstance(note,Note):
            try:
                note = Note(note)
            except:
                raise

        if not self.note_in_key(note):
            e = f"The given item `{note}` does not exist within the scale `{self.tonic} {self.mode}`"
            raise ValueError(e)

        tonic_compressed = self.tonic.value % 12
        note_compressed = (note.value % 12)

        if note_compressed < tonic_compressed:
            note_compressed += 12

        _current = tonic_compressed
        for i,hs in enumerate(self.mode):
            if _current == note_compressed:
                return i
            else:
                _current += hs










