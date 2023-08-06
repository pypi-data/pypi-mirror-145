from copy import deepcopy
from typing import Union, Iterable, Collection, Optional, List
import random

import numpy as np

from MidiCompose.logic.rhythm.time_unit import TimeUnit
from MidiCompose.utilities import temp_seed, ctx_random_seed


class BeatIterator:

    def __init__(self, beat):
        self._Beat = beat
        self._index = 0

        self._len_Beat = len(self._Beat)

    def __next__(self):
        if self._index < self._len_Beat:
            result = self._Beat.time_units[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration


class Beat:
    """
    Container for TimeUnit objects.

    Definitive attribute is `self.time_units`, which is a numpy array containing TimeUnit objects.

    Argument `time_units` must either be a single integer representing the number of
    subdivisions, or an iterable containing TimeUnit objects and/or "TimeUnit-like"
    integers (ie. {0,1,2}). The latter is useful when passing stateful TimeUnit objects.
    """

    def __init__(self,
                 time_units: Union[int, Iterable[Union[int, TimeUnit]]] = 1,
                 verbose: bool = False):
        """
        :param verbose: determines format of output
        """

        # self._parse_beat_arg(time_units)

        self.time_units = time_units  # calls setter method

        self.verbose = verbose

    @property
    def time_units(self) -> List[TimeUnit]:
        return self._time_units

    @time_units.setter
    def time_units(self, value):

        # if integer, `value` represents number of subdivisions
        if isinstance(value, int):
            self._time_units = [TimeUnit() for _ in range(value)]
        else:
            tu_like_type_set = {int, TimeUnit}
            value_type_set = set([type(v) for v in value])

            # else, collection of integers/TimeUnit objects
            if value_type_set.issubset(tu_like_type_set):
                _time_units = []
                for v in value:
                    if isinstance(v, TimeUnit):
                        _time_units.append(v)
                    else:
                        _time_units.append(TimeUnit(v))
                self._time_units = _time_units

            else:
                msg = f"Invalid input"
                raise AttributeError(msg)

    @property
    def subdivision(self) -> int:
        return len(self)

    @property
    def state(self) -> np.ndarray:
        """
        1d numeric array representing the value of each TimeUnit in the Beat.
        """
        state = np.empty(shape=(self.subdivision + 2,), dtype=np.int8)
        state[:2] = [-3, self.subdivision]
        state[2:] = [tu.state for tu in self.time_units]
        return state

    @property
    def active_state(self) -> np.ndarray:
        return self.state[2:]

    @property
    def n_note_on(self) -> int:
        """
        The number of "note_on" events in the Beat.
        """
        return np.where(self.active_state == 1)[0].size

    @property
    def is_active(self) -> bool:
        """
        Returns True if any TimeUnit instances contain active time_units (1 or 2).
        Otherwise, returns False.
        """
        if self.n_note_on > 0:
            return True
        else:
            return False

    #### UTILITY FUNCTIONS ####

    def set_state(self,
                  state: Collection[int],
                  override: bool = False):
        """
        Set the `value` of the time_units instance to collection of either 0,1 or 2.

        Automatically updates `time_units` attribute.

        :param state: Collection of integers in {0,1,2}
        :param override: If False, error will be raised if setting time_units to an already active
        """
        valid_state_set = {0, 1, 2}
        given_state_set = set(state)
        if not given_state_set.issubset(valid_state_set):
            msg = "Parameter `value` takes a collection containing only integers 0,1 and 2."
            raise AttributeError(msg)

        # PICKUP HERE -- SEE FAILING TEST
        self.time_units = state  # calls setter method

        return self

    def activate_random(self,
                        density: float,
                        random_seed: Optional[int] = None):
        """
        :param density: float between 0 and 1 representing the density of activation.
        :param random_seed: Provide a random random_seed for reproducibility.
        """
        _beat = deepcopy(self)

        if random_seed is not None:
            with temp_seed(random_seed):
                choices = np.random.choice(a=[0, 1],
                                           size=_beat.subdivision,
                                           p=[1 - density, density])

                [tu.set_state(c) for tu, c in zip(_beat.time_units, choices)]
        else:
            choices = np.random.choice(a=[0, 1],
                                       size=_beat.subdivision,
                                       p=[1 - density, density])
            [tu.set_state(c) for tu, c in zip(_beat.time_units, choices)]

        return _beat

    def sustain_all(self):
        """
        Convert all "note_off" events to sustain events (ie change all 0s to 2).
        """
        _beat = deepcopy(self)

        idx_off = np.where(_beat.state[2:] == 0)[0]
        for idx in idx_off:
            _beat.time_units[idx].sustain()

        return _beat

    def shorten_all(self):
        """
        Convert all "sustain" events to "note_off".
        """
        idx_sustain = np.where(self.state[2:] == 2)[0]
        for idx in idx_sustain:
            self.time_units[idx].deactivate()

    #### GENERATOR METHODS ####

    def get_complement(self,
                       adherence: float = 1.0,
                       random_seed: Optional[int] = None):
        """
        Returns new `Beat` instance which is complement of "attack".

        ie. all "sustain" is stripped.

        Params:
        - adherence (str) : ...
        """

        if adherence < 0 or adherence > 1:
            msg = "`Adherence` must be a float between 0 and 1"
            raise ValueError(msg)

        _time_units = deepcopy(self._time_units)

        with ctx_random_seed(random_seed):
            _adherence = random.choices([0,1],
                                        weights=[1-adherence,adherence],
                                        k=len(_time_units))

        _complement = []
        for tu,adhere in zip(_time_units,_adherence):
            if adhere == 1:
                _tu = tu.toggle()
            else:
                _tu = tu
            _complement.append(_tu)

        complement = Beat(_complement)

        return complement

    #### MAGIC METHODS ####

    def __iter__(self):
        return BeatIterator(self)

    def __getitem__(self, item: int) -> TimeUnit:
        return self.time_units[item]

    def __mul__(self, number: int):
        copies = []
        for _ in range(number):
            copies.append(deepcopy(self))
        return copies

    def __len__(self):
        return len(self.time_units)

    def set_verbosity(self, verbose: bool):
        self.verbose = verbose

    def __repr__(self):
        r = "Beat("
        time_units = [str(tu) for tu in self.time_units]
        r += ",".join(time_units) + ")"
        return r