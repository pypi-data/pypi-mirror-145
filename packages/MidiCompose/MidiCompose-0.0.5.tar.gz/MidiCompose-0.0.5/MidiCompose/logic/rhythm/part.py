from __future__ import annotations

from copy import deepcopy
from typing import Collection, Optional, List, Sequence
import random

import numpy as np
from icecream import ic

from MidiCompose.logic.rhythm.measure import Measure
from MidiCompose.logic.rhythm.measure import Beat

from MidiCompose.utilities import ctx_random_seed


class PartIterator:

    def __init__(self, part):
        self._Part = part
        self._index = 0
        self._len_Part = self._Part.n_measures

    def __next__(self) -> Measure:
        if self._index < self._len_Part:
            result = self._Part.measures[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration


class Part:
    """
    Container for Measures
    """

    def __init__(self, measures: Optional[Collection[Measure]] = None):
        self.measures = measures

    @property
    def measures(self) -> List[Measure]:
        return self._measures

    @measures.setter
    def measures(self, value):

        if value is None:  # initialize empty part
            self._measures = []
        else:
            self._measures = [measure for measure in value]

    @property
    def state(self):
        measure_states = np.concatenate([m.state for m in self.measures])
        state = np.empty(shape=(measure_states.size + 2,), dtype=np.int8)
        state[0], state[-1] = -1, -1
        state[1:-1] = measure_states
        return state

    @property
    def n_note_on(self) -> int:
        return sum([m.n_note_on for m in self.measures])

    @property
    def n_measures(self) -> int:
        return len(self.measures)

    @property
    def n_beats(self) -> int:
        return sum([m.n_beats for m in self.measures])

    @property
    def active_state(self):
        pass

    #### UTILITY METHODS ####
    def append_measure(self, measure: Measure):

        if not isinstance(measure,Measure):
            e = "`measure` must be a Measure instance."
            raise TypeError(e)

        self.measures.append(measure)
        return self

    def activate_random(self,
                        density: float,
                        random_seed: int = None,
                        measure_idx: Sequence[int] = None) -> Part:

        if measure_idx is None:
            measure_idx = list()

        _measures = []
        with ctx_random_seed(seed=random_seed):
            for i, measure in enumerate(self.measures):
                if i in measure_idx:
                    _measure = measure
                else:
                    _n_beats = measure.n_beats
                    _sub_values = list(measure.subdivision_values)
                    ic(_sub_values)

                    choices = random.choices([1,0],
                                             weights=[density,1-density],
                                             k=sum(_sub_values))
                    ic(choices)

                    _beats = []
                    idx = 0
                    for sub_val in _sub_values:
                        _beats.append(Beat(choices[idx:sub_val+1]))
                        idx += sub_val
                    _measure = Measure(_beats)
                _measures.append(_measure)

        return Part(_measures)








    #### GENERATOR METHODS ####

    def get_complement(self, measure_idx: Optional[Sequence[int]] = None):

        if measure_idx is not None:
            e = "Implement measure indexing!"
            raise NotImplementedError(e)
        _measures = self._measures
        complement = Part([m.get_complement() for m in _measures])
        return complement

    #### MAGIC METHODS ####
    def __iter__(self):
        return PartIterator(self)

    def __getitem__(self, item: int) -> Measure:
        return self.measures[item]

    def __len__(self):
        return len(self.measures)

    def __mul__(self, other: int):
        return [deepcopy(self) for _ in range(other)]

    def __repr__(self):

        r = "Part(["
        measure_strings = [str(m) for m in self.measures]
        for m in measure_strings:
            r += "\n" + " " + m
        r += f"\nn_beats: {self.n_beats}"
        r += "\n])"
        return r

