from typing import List, Optional
from importlib import import_module

from MidiCompose.logic.harmony.note import Note,HasNotes
from MidiCompose.logic.harmony.chord import Chord
from MidiCompose.logic.harmony.chord_sequence import ChordSequence
from MidiCompose.logic.harmony.interval import Interval
from MidiCompose.logic.harmony.interval import IntervalRange
from MidiCompose.logic.harmony.key import Key
from MidiCompose.logic.harmony.figure import TonalFiguredNote, ChromaticFiguredNote

from MidiCompose.logic.melody.melody import Melody
from MidiCompose.logic.melody.note_set import NoteSet
from MidiCompose.logic.melody.scale import Scale, DiatonicModes, NonDiatonicModes, AllModes

from MidiCompose.logic.rhythm.time_unit import TimeUnit
from MidiCompose.logic.rhythm.beat import Beat
from MidiCompose.logic.rhythm.measure import Measure
from MidiCompose.logic.rhythm.part import Part

from MidiCompose.translation.track_builder import TrackBuilder

from MidiCompose.playback import play_mid

from MidiCompose.utilities import ctx_random_seed

