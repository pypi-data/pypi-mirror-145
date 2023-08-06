import random
from typing import Union, Collection, Optional, List, Sequence
from copy import deepcopy
from itertools import chain

import numpy as np
from icecream import ic

from MidiCompose.logic.rhythm.beat import Beat
from MidiCompose.utilities import temp_seed,ctx_random_seed


class MeasureIterator:

    def __init__(self, measure):
        self._Measure = measure
        self._index = 0
        self._len_Measure = len(self._Measure)

    def __next__(self) -> Beat:
        if self._index < self._len_Measure:
            result = self._Measure.beats[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration


class Measure:

    def __init__(self,
                 beats: Optional[Union[Collection[Union[int, Beat, Collection[int]]]]] = None,
                 verbose: bool = False):
        """
        Three options for initialization:
        1) Supply iterable of Beat object. This is useful if passing Beats with pre-defined time_units.
        2) Supply a collection of collections of integers, where the number of items represents the number
           of time_units, and the values of the integers represents the respective subdivision of each time_units.
        3) Combination of the previous two.

        Note that passing an integer will automatically instantiate an "empty" time_units. That is,
        all TimeUnit objects will be set to 0 within that time_units.

        :param beats: iterable containing Beat objects, bare integers, or a combination of the two.
        :param verbose: if True, __repr__ gives more info.
        """

        self.beats: Collection[Beat] = beats  # calls setter method
        self.verbose: bool = verbose


    #### PROPERTIES ####

    @property
    def beats(self) -> List[Beat]:
        return self._beats

    @beats.setter
    def beats(self, value):

        if value is None:  # initialize empty measure
            self._beats = []
        else:

            value_type_set = set([type(b) for b in value])

            beat_set = {Beat}
            int_set = {int}
            col_of_ints_set = {Collection}
            mixed_set = {Beat, int}

            # collection of collections of integers
            coll_of_colls = all([issubclass(type(b), Collection) for b in value])
            if coll_of_colls:
                self._beats = [Beat(c) for c in value]

            # contains only Beats -- no validation needed
            elif value_type_set.issubset(beat_set):
                self._beats = [v for v in value]

            # contains only integers -- validated by Beat constructor
            elif value_type_set.issubset(int_set):
                self._beats = [Beat(a) for a in value]

            # contains mixture Beat and int -- validated by Beat constructor
            else:
                _beats = []
                for b in value:
                    if type(b) == int:
                        _beats.append(Beat(b))
                    else:
                        _beats.append(b)
                self._beats = _beats

    @property
    def n_beats(self):
        return len(self)

    @property
    def state(self):
        """
        1-d numeric array containing figure of each time_units in Measure.
        """
        beat_states = np.concatenate([b.state for b in self.beats])
        state = np.empty(shape=(beat_states.size + 1,), dtype=np.int8)
        state[0] = -2
        state[1:] = beat_states
        return state

    @property
    def active_state(self) -> np.ndarray:
        """
        Same as `figure` array but without beat/measure flags.
        """
        return np.concatenate([b.active_state for b in self.beats])

    @property
    def subdivision_values(self) -> np.ndarray:
        """
        Returns a 1d array containing the subdivision of each `Beat` in the `Measure`.
        """
        idx_sub_vals = np.where(self.state == -3)[0] + 1
        sub_vals = self.state[idx_sub_vals]
        return sub_vals

    @property
    def n_note_on(self) -> int:
        """
        The number of "note_on" events in the Measure.
        """
        return sum([b.n_note_on for b in self.beats])

    @property
    def is_active(self):
        if self.n_note_on > 0:
            return True
        else:
            return False

    @property
    def flattened(self) -> List[int]:
        _flattened = list(chain(*self))
        return _flattened

    #### UTILITY FUNCTIONS ####

    # TODO: implement override/reshape checks
    def set_state(self,
                  state: [Collection[Collection[int]]],
                  override: bool = True,
                  reshape: bool = False):
        """
        Sets `figure` array as well as `beats` array.

        :param override: If False, will raise exception if trying to override a stateful measure.
        :param reshape: If False, will raise exception if `figure` argument would result in "reshaping" the measure (ie.
        changing the number of beats, or number of subdivisions in a time_units.)
        """
        self.beats = state

    def activate_random(self, density: float,
                        random_seed: Optional[int] = None,
                        beat_idx: Sequence[int] = None):

        beats = deepcopy(self.beats)

        _beats = []
        with ctx_random_seed(random_seed):
            if beat_idx is None:
                beat_idx = list()

            for i,beat in enumerate(beats):
                if i not in beat_idx:
                    choices = random.choices(population=[1,0],
                                             weights=[density,1-density],
                                             k=len(beat))
                    _beat = Beat(choices)
                else:
                    _beat = beat
                _beats.append(_beat)

        _measure = Measure(_beats)
        return _measure

    def sustain_all(self, beat_idx: Optional[Collection[int]] = None):
        """
        Convert all "item-off" events to "sustain" events.
        :param beat_idx: If given, only apply to the given beats.
        """
        if beat_idx is not None:
            if max(beat_idx) > len(self.beats):
                msg = f"`beat_idx` out of range."
                raise IndexError(msg)
            else:
                for i in beat_idx:
                    self.beats[i].sustain_all()
        else:
            for b in self.beats:
                b.sustain_all()

        return self

    def shorten_all(self, beat_idx: Optional[Collection[int]] = None):
        """
        Convert all "sustain" events to "note_off" events.
        :param beat_idx: If given, only apply to the given beats.
        """

        if beat_idx is not None:
            if max(beat_idx) > len(self.beats):
                msg = f"`beat_idx` out of range."
                raise IndexError(msg)
            else:
                for i in beat_idx:
                    self.beats[i].shorten_all()
        else:
            for b in self.beats:
                b.shorten_all()

        return self

    #### GENERATOR FUNCTIONS ####

    def get_complement(self,
                       adherence: float = 1.0,
                       random_seed: Optional[int] = None,
                       beat_idx:Optional[Sequence[int]] = None) -> Beat():

        raise NotImplementedError()

        if adherence > 1 or adherence < 0:
            msg = "`adherence` must be a float between 0 and 1."
            raise ValueError(msg)

        if beat_idx is not None:
            e = "Implement beat indexing!"
            raise NotImplementedError(e)

    #### MAGIC METHODS ####

    def __iter__(self):
        return MeasureIterator(self)

    def __getitem__(self, item: int) -> Beat:
        return self.beats[item]

    def __mul__(self,number: int) -> list:
        return [deepcopy(self) for _ in range(number)]

    def __len__(self):
        return len(self.beats)

    def __repr__(self):
        r = "Measure("
        beat_strs = [str(b.active_state) for b in self.beats]
        for i,b in enumerate(beat_strs):
            if i < len(beat_strs) - 1:
                r += b + ", "
            else:
                r += b + ")"
        return r



