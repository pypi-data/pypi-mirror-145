import contextlib
import random
from typing import Optional

import numpy as np


@contextlib.contextmanager
def temp_seed(seed):
    state = np.random.get_state()
    if seed is None:
        np.random.set_state(state)
        yield

    else:
        np.random.seed(seed)
        try:
            yield
        finally:
            np.random.set_state(state)

@contextlib.contextmanager
def ctx_random_seed(seed: Optional[int]):
    if seed is None:
        yield
    else:
        random_state = random.getstate()
        random.seed(seed)
        try:
            yield
        finally:
            random.setstate(random_state)




class TwoWayDict(dict):
    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        """Returns the number of connections"""
        return dict.__len__(self) // 2