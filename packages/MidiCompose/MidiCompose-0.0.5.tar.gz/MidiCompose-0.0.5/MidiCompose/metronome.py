from typing import Optional, Tuple

import mido

from MidiCompose.logic.harmony.note import Note
from MidiCompose.logic.melody.melody import Melody
from MidiCompose.logic.rhythm.beat import Beat
from MidiCompose.logic.rhythm.part import Part
from MidiCompose.logic.rhythm.measure import Measure

from MidiCompose.translation.track_builder import TrackBuilder

from rendering.sf2_objects import GmPercussionRack, GmInstrumentRack

INST = GmInstrumentRack.jazz
BELL = GmPercussionRack.metronome_bell
CLICK = GmPercussionRack.metronome_click


class Metronome:
    """
    Links to a `Part` object, and accents downbeat of each measure by default.

    Customization options
    """

    def __init__(self, match: Part,
                 measure_click: GmPercussionRack = GmPercussionRack.metronome_bell,
                 beat_click: GmPercussionRack = GmPercussionRack.metronome_click,
                 instrument: GmInstrumentRack = GmInstrumentRack.standard,
                 tpb: int = 480):

        self.match = match

        self.part_measure,self.part_beat = self._get_parts()

        self.measure_click = measure_click
        self.beat_click = beat_click
        self.instrument = instrument

        self.tpb = tpb

    def _get_parts(self) -> Tuple[Part,Part]:

        _match = self.match

        pm_measures = []  # part_measure_measures
        pb_measures = []  # part_beat_measures
        for m in _match:
            pm_beats = []
            pb_beats = []
            for i,b in enumerate(m):
                if i == 0:
                    pm_beats.append(Beat([1]))
                    pb_beats.append(Beat([0]))
                else:
                    pm_beats.append(Beat([0]))
                    pb_beats.append(Beat([1]))

            pm_measures.append(Measure(pm_beats))
            pb_measures.append(Measure(pb_beats))

        part_measure = Part(pm_measures)
        part_beats = Part(pb_measures)

        return part_measure,part_beats

    def get_track(self) -> mido.MidiTrack:

        _part_measure = self.part_measure
        _part_beat = self.part_beat

        mel_measure = Melody([Note(self.measure_click.note) for _ in range(_part_measure.n_note_on)])
        mel_beat = Melody([Note(self.beat_click.note) for _ in range(_part_beat.n_note_on)])

        tb = TrackBuilder(parts=[_part_measure,_part_beat],
                          melodies=[mel_measure,mel_beat],
                          tpb=self.tpb)

        messages = tb.get_messages()

        track = mido.MidiTrack(messages)

        return track


if __name__ == '__main__':
    part_match = Part([Measure([[1, 0, 1, 1], [1, 2, 2, 1]]),
                       Measure([[1, 2, 2], [2, 1, 2]])])

