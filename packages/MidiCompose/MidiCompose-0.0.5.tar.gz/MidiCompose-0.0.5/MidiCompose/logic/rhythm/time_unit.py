
class TimeUnit:
    """
    Contains the time_units of a subdivision within a Beat.

    State can be 1 (attack), 2 (sustain), or 0 (release).
    """

    def __init__(self,
                 state: int = 0,
                 verbose: bool = False):

        # definitive attribute
        self.state: int = state
        self._validate()

        # __repr__ verbosity
        self.verbose: bool = verbose

    def _validate(self):
        if not isinstance(self.state, int):
            msg = "`time_units` must be an integer."
            raise TypeError(msg)
        if self.state not in {0, 1, 2}:
            msg = "`time_units` can only be either 0, 1, or 2."
            raise ValueError(msg)

    def activate(self):
        self.state = 1
        return self

    def sustain(self):
        self.state = 2
        return self

    def deactivate(self):
        self.state = 0
        return self

    def toggle(self):
        """
        Convert "on" to "off" and vice versa.

        Sustain toggles to "on"
        """
        if self.state in (0,2):
            self.state = 1
        elif self.state == 1:
            self.state = 0

        return self

    def set_state(self, value: int):
        if not value in {0, 1, 2}:
            msg = f"Invalid value. TimeUnit `figure` must be in {0, 1, 2}."
            raise ValueError(msg)
        else:
            self.state = value
        return self

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def __eq__(self, other):
        if type(other) == int:
            return self.state == other
        else:
            return self.state == other.state

    def __int__(self):
        return int(self.state)

    def __repr__(self):
        if self.verbose:
            r = f"TimeUnit(time_units={self.state})"
        else:
            r = str(self.state)
        return r