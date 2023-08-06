from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field, Field
from itertools import cycle
from typing import Set, List, Union, Sequence, Tuple, Any, Optional
from enum import Enum
from icecream import ic

from MidiCompose.logic.harmony.interval import Interval
from MidiCompose.logic.harmony.note import Note, HasNotes, to_note, sequence_to_notes


class KeySchema(Enum):
    IONIAN = MAJOR = (2, 2, 1, 2, 2, 2)
    DORIAN = (2, 1, 2, 2, 2, 1)
    PHRYGIAN = (1, 2, 2, 2, 1, 2)
    LYDIAN = (2, 2, 2, 1, 2, 2)
    MIXOLYDIAN = (2, 2, 1, 2, 2, 1)
    AEOLIAN = MINOR = (2, 1, 2, 2, 1, 2)
    LOCRIAN = (1, 2, 2, 1, 2, 2)

    MELODIC_MINOR = (2, 1, 2, 2, 2, 2)
    LYDIAN_DOMINANT = (2, 2, 2, 1, 2, 1)
    ALTERED = (1, 2, 1, 2, 2, 2)

    HARMONIC_MINOR = (2, 1, 2, 2, 1, 3)
    HARMONIC_MAJOR = (2, 2, 1, 2, 1, 3)
    WHOLE_TONE = (2, 2, 2, 2, 2)
    DIMINISHED_HW = (1, 2, 1, 2, 1, 2, 1)
    DIMINISHED_WH = (2, 1, 2, 1, 2, 1, 2)

    CHROMATIC = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

    @classmethod
    def parse(cls, value: Any) -> KeySchema:

        if isinstance(value, KeySchema):
            return value
        elif isinstance(value, str):
            try:
                return KeySchema[value.upper()]
            except:
                e = f"Invalid `KeySchema` string representation. Possible inputs are: {[v.name for v in cls]}"
                raise ValueError(e)

    @staticmethod
    def all_diatonic(exclude: KeySchema | Sequence[KeySchema | Any] = None) -> List[KeySchema]:
        if exclude is not None:
            if isinstance(exclude,KeySchema):
                _exclude = [exclude]
            else:
                try:
                    _exclude = [KeySchema.parse(ks) for ks in exclude]
                except:
                    raise
        else:
            _exclude = []

        diatonic = [KeySchema.MAJOR,KeySchema.DORIAN,KeySchema.PHRYGIAN,
                    KeySchema.LYDIAN,KeySchema.MIXOLYDIAN,KeySchema.AEOLIAN,
                    KeySchema.LOCRIAN]

        return [ks for ks in diatonic if ks not in _exclude]


class Key:

    def __init__(self,
                 tonic: Note | Any,
                 key_schema: KeySchema | str = None):

        if key_schema is None:
            _parsed = self.parse(value=tonic)
            tonic, key_schema = _parsed["tonic"], _parsed["key_schema"]

        self.tonic = tonic  # calls setter
        self.key_schema = key_schema  # setter

    @classmethod
    def parse(cls, value: Any) -> dict:
        """
        Parse various input types as Key.

        returns kwargs to pass to instance attributes in __init__ method.

        Possible inputs include:
        - Key object -> returns unchanged
        - Note object -> returns Major scale with give Note as tonic if no key schema given.
        - string representation with the form: <NOTE_STR> [<KEY_SCHEMA_STR>='MAJOR'] (e.g. "C HARMONIC_MINOR")
        """
        DEFAULT_SCHEMA = KeySchema["MAJOR"]

        if isinstance(value, Key):
            _parsed = {"tonic": value.tonic, "key_schema": value.key_schema}
        elif isinstance(value, Note):
            _parsed = {"tonic": value, "key_schema": DEFAULT_SCHEMA}
        elif isinstance(value, str):
            _split_value = value.split(sep=" ")
            if len(_split_value) == 2:  # interpret as <tonic> <KeySchema>
                try:
                    _tonic = Note(_split_value[0].title())
                    _key_schema = KeySchema.parse(_split_value[1])

                    _parsed = {"tonic": _tonic, "key_schema": _key_schema}
                except:
                    raise

            elif len(_split_value) == 1:  # interpret as <tonic> with default KeySchema

                try:
                    _tonic = Note(_split_value[0].title())
                    _parsed = {"tonic": _tonic, "key_schema": DEFAULT_SCHEMA}
                except:
                    raise

            else:
                e = "Invalid string representation of `Key` object. Should have the form: '<tonic> [<key_schema>=MAJOR]'."
                raise ValueError(e)

        elif isinstance(value, int):
            try:
                _tonic = Note(value)
                _parsed = {"tonic": _tonic, "key_schema": DEFAULT_SCHEMA}
            except:
                raise

        else:
            e = f"Failed to parse input `{value}` as a Key object."
            raise ValueError(e)

        return _parsed

    @property
    def tonic(self) -> Note:
        return self._tonic

    @tonic.setter
    def tonic(self, value):

        if not isinstance(value, Note):
            try:
                _tonic = Note(value)
            except:
                raise
        else:
            _tonic = value

        self._tonic = _tonic

    @property
    def key_schema(self) -> KeySchema:
        return self._key_schema

    @key_schema.setter
    def key_schema(self, value):
        if isinstance(value, KeySchema):
            _key_schema = value
        elif isinstance(value, str):
            try:
                _key_schema = KeySchema[value]
            except:
                e = f"The argument given for `key_schema` : `{value}` is not a valid KeySchema value. Supported arguments include: {[v.name for v in KeySchema]}."
                raise ValueError(e)
        else:
            e = f"Parameter `key_schema` must be given a valid KeySchema object or string representation."
            raise TypeError(e)

        self._key_schema = _key_schema

    @property
    def key_name(self) -> str:
        return self.key_schema.name

    @property
    def schema(self) -> Tuple[int]:
        return self.key_schema.value

    @property
    def notes(self) -> List[Note]:

        # get major scale based on tonic
        _family = Note(self.tonic.value % 12)

        _scale = [_family]
        for interv in self.schema:
            next_note = Note((_scale[-1].value + interv) % 12)
            _scale.append(next_note)

        return _scale

    def get_neighbors(self,
                      depth=1) -> List[Tuple[Key, Key]]:
        """
        Returns list of tuples where first element of each tuple is the 'lower neighbor' (P5 below self) \
        and the second element is the `upper neighbor` (P5 above self).

        :param depth: number of neighbor sets to generate.
        """

        if depth not in range(1,7):
            e = "`depth` must be between 1 and 6"
            raise ValueError(e)

        _tonic = self.tonic

        _neighbors = []
        for _ in range(depth):
            if len(_neighbors) == 0:
                lower_tonic = Interval("P4").above(_tonic)
                upper_tonic = Interval("P5").above(_tonic)

                lower_neighbor = Key(tonic=lower_tonic, key_schema=self.key_schema)
                upper_neighbor = Key(tonic=upper_tonic, key_schema=self.key_schema)

                _neighbors.append((lower_neighbor, upper_neighbor))

            else:
                lower_tonic = Interval("P4").above(_neighbors[-1][0].tonic)
                upper_tonic = Interval("P5").above(_neighbors[-1][1].tonic)

                lower_neighbor = Key(tonic=lower_tonic, key_schema=self.key_schema)
                upper_neighbor = Key(tonic=upper_tonic, key_schema=self.key_schema)
                _neighbors.append((lower_neighbor, upper_neighbor))

        return _neighbors

    def get_index_of(self,
                     note: Union[Note, int, str]) -> int:

        try:
            _note = to_note(note)
        except:
            raise

        if _note not in self:
            e = f"Given from_note `{note}` is not in Key `{self.tonic}`"
            raise ValueError(e)

        _note = Note(_note.value % 12)

        return self.notes.index(_note)

    def next_note(self,
                  from_note: Union[Note, int, str],
                  step: int = 1) -> Note:

        if step <= 0:
            e = "Argument `step` must be >= 1."
            raise ValueError(e)
        else:
            try:
                _note = to_note(from_note)
            except:
                raise

            try:
                _idx = self.get_index_of(from_note)
            except:
                raise

        for _step in range(step):
            _idx = (_idx + 1) % len(self.notes)
            _next_note = self[_idx]

        return _next_note

    def previous_note(self,
                      note: Union[Note, int, str],
                      step: int = 1) -> Note:
        if step <= 0:
            e = "Argument `step` must be >= 1."
            raise ValueError(e)
        else:
            try:
                _note = to_note(note)
            except:
                raise
            try:
                _idx = self.get_index_of(note)
            except:
                raise

            for _step in range(step):
                _idx = (_idx - 1) % len(self.notes)
                _previous_note = self[_idx]

        return _previous_note

    def note_range(self,
                   a: Note | Any,
                   b: Note| Any) -> List[Note]:
        """
        order is preserved
        """
        try:
            a, b = [to_note(n) for n in [a, b]]
        except:
            raise

        if a == b:
            return [a]
        else:
            chrom_range = Note.range(a, b)
            rng = [n for n in chrom_range if n in self]
            return rng

    def steps_above(self,
                    note: Union[Note, int, str],
                    steps: int) -> Note:
        """
        Get the Note which is "N" steps away from the given from_note in the context of the current Key.
        """

        try:
            _note = to_note(note)
        except:
            raise
        try:
            _idx = self.get_index_of(note)
        except:
            raise

        if steps < 0:
            e = "Argument `steps` must be positive."
            raise ValueError(e)

        _previous = _note
        for _ in range(steps):
            _n = self.next_note(_previous)
            _previous = _previous.nearest_neighbors(_n, "UPPER")

        _final = _previous
        return _final

    def steps_below(self,
                    note: Union[Note, int, str],
                    steps: int) -> Note:
        try:
            _note = to_note(note)
        except:
            raise
        try:
            _idx = self.get_index_of(note)
        except:
            raise

        if steps < 0:
            e = "Argument `steps` must be positive."
            raise ValueError(e)

        _previous = _note
        for _ in range(steps):
            _n = self.previous_note(_previous)
            _previous = _previous.nearest_neighbors(_n, "LOWER")

        _final = _previous
        return _final

    def steps_between(self,
                      a: Note,
                      b: Note) -> int:
        """
        Returns the number of scale-steps between two notes in a key. Direction is assumed as from `a` to `b`.
        """
        try:
            a, b = to_note(a), to_note(b)
            _notes = [a, b]

        except:
            raise

        if any([n not in self for n in _notes]):
            bad = [n for n in _notes if n not in self]
            e = f"The given from_note(s) `{bad}` do not exist in the Key `{self.tonic}`."
            raise ValueError(e)

        else:
            steps = 0
            _dir = 1
            if a == b:
                pass
            elif a < b:
                while a < b:
                    a = self.steps_above(a, 1)
                    steps += 1
            elif a > b:
                _dir = -1
                while a > b:
                    a = self.steps_below(a, 1)
                    steps += 1

            steps = steps * _dir

            return steps

    @staticmethod
    def all_keys_with(notes: Union[Note, int, str, Sequence],
                      key_schemas: KeySchema | Sequence[KeySchema] = KeySchema.MAJOR,
                      _any: bool = False,
                      _raise: bool = False) -> List[Key]:
        """
        Returns a list of Key instances which contain `notes`.
        :param notes: One or many Note/from_note-like objects
        :param _any: if True, will return all keys containing any of the given notes. Default behavior is to include only
        keys which contain all `notes`
        """
        if isinstance(key_schemas, KeySchema):
            _key_schemas = [key_schemas]
        else:
            try:
                _key_schemas = [KeySchema.parse(ks) for ks in key_schemas]
            except:
                raise

        _all_tonics = list(range(0, 12))

        all_keys = []
        for t in _all_tonics:
            for ks in _key_schemas:
                all_keys.append(Key(tonic=t,key_schema=ks))

        if isinstance(notes, Sequence):
            try:
                _notes = sequence_to_notes(notes)
            except:
                raise
        else:
            try:
                _notes = [to_note(notes)]
            except:
                raise

        if _any:
            _keys_with = []
            for key in all_keys:
                if any([n in key for n in _notes]):
                    _keys_with.append(key)

        else:
            _keys_with = [k for k in all_keys if _notes in k]

        if len(_keys_with) == 0 and _raise:
            e = f"Given notes {_notes} do not exist in any Key."
            raise ValueError(e)

        return _keys_with

    @staticmethod
    def all_keys(key_schemas: KeySchema | Sequence[KeySchema] = KeySchema.MAJOR) -> List[Key]:
        """
        Returns a list of all Keys
        """
        if isinstance(key_schemas,KeySchema):
            key_schemas = [key_schemas]
        else:
            try:
                key_schemas = [KeySchema.parse(ks) for ks in key_schemas]
            except:
                raise

        all_keys = []
        for t in range(12):
            for ks in key_schemas:
                all_keys.append(Key(tonic=t,key_schema=ks))

        return all_keys

    def __getitem__(self, item):

        if item not in range(0, len(self.notes)):
            e = f"Index must be between 1 and {len(self.notes) - 1}."
            raise IndexError(e)

        return self.notes[item]

    def __contains__(self, item: Union[Note, str, int, Sequence]) -> bool:

        if isinstance(item, Note):

            _item = Note(item.value % 12)

            if _item in self.notes:
                return True
            else:
                return False

        elif isinstance(item, str) or isinstance(item, int):
            try:
                _item = Note(item)
            except:
                raise

            _item = Note(_item.value % 12)
            if _item in self.notes:
                return True
            else:
                return False

        elif isinstance(item, Sequence):
            try:
                _notes = sequence_to_notes(item)
            except:
                raise

            if all([n.signature in self.notes for n in _notes]):
                return True
            else:
                return False

    def __len__(self):
        return len(self.notes)

    def __eq__(self, other):
        if isinstance(other, Key):
            if other.tonic == self.tonic:
                return True
            else:
                return False
        else:
            return NotImplementedError

    def __repr__(self):
        r = f"Key({self.tonic.as_letter(include_range=False)} " \
            f"{self.key_name} " \
            f"{[n.as_letter(include_range=False) for n in self.notes]})"
        return r

