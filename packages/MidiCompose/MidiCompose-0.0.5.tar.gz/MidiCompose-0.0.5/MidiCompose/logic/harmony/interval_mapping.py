from icecream import ic

from MidiCompose.utilities import TwoWayDict

HS_INTERVAL_DICT = {
    0: 'P1',
    1: 'm2',
    2: 'M2',
    3: 'm3',
    4: 'M3',
    5: 'P4',
    6: 'A4',
    7: 'P5',
    8: 'm6',
    9: 'M6',
    10: 'm7',
    11: 'M7',
}


def populate_interval_mapper() -> TwoWayDict:
    interval_mapper = TwoWayDict()
    for _hs in range(0, 127):
        oct_shift, hs = divmod(_hs, 12)
        oct_shift = int(oct_shift)

        qual_val = HS_INTERVAL_DICT[hs]

        interval = qual_val + str(oct_shift * "+")
        interval_mapper[_hs] = interval

    return interval_mapper


INTERVAL_MAPPER = populate_interval_mapper()