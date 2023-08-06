from collections import OrderedDict, namedtuple
from dataclasses import dataclass, field
from typing import Type, Optional, List, Dict, Union

from icecream import ic
from mido import MidiFile, MidiTrack, Message

import json


MessageTimeStamp = namedtuple("MessageTimeStamp",
                              ["msg_num",
                               "ticks_elapsed",
                               "msg_type",
                               "time_attribute"
                               ])

@dataclass
class MessageCounts:
    track: MidiTrack = field(repr=False)
    msg_timestamps: List[MessageTimeStamp] = field(default=None,
                                                   repr=False)

    total: Optional[int] = 0

    meta: Optional[int] = 0
    set_tempo: Optional[int] = 0

    note_on: Optional[int] = 0
    note_off: Optional[int] = 0
    other: Optional[int] = 0

    def __post_init__(self):

        ticks_elapsed = 0
        msg_num = 0
        self.msg_timestamps = list()
        for msg in self.track:

            self.total += 1

            if msg.is_meta:
                self.meta += 1
                if msg.type == "set_tempo":
                    self.set_tempo += 1

            elif msg.type == "note_on":
                if self.note_on is None:
                    self.note_on = 0
                self.note_on += 1

            elif msg.type == "note_off":
                if self.note_off is None:
                    self.note_off = 0
                self.note_off += 1

            else:
                self.other += 1

            msg_time_attr = msg.time
            msg_type = msg.type

            msg_ts = MessageTimeStamp(msg_num=msg_num,
                                      ticks_elapsed=ticks_elapsed,
                                      msg_type=msg_type,
                                      time_attribute=msg_time_attr)
            self.msg_timestamps.append(msg_ts)

            ticks_elapsed += msg_time_attr
            msg_num += 1


@dataclass
class MidTrackInfo:
    track: MidiTrack = field(repr=False)

    n_messages: Optional[int] = None

    # contains message type booleans
    contains_notes: Optional[bool] = field(default=None, repr=False)
    contains_meta: Optional[bool] = field(default=None, repr=False)
    contains_set_tempo: Optional[bool] = field(default=None, repr=False)

    msg_counts: Optional[MessageCounts] = None
    msg_timestamps: Optional[List[MessageTimeStamp]] = field(
        default=None,
        repr=False
    )
    track_number: Optional[int] = None

    def __post_init__(self):
        self.msg_counts = MessageCounts(self.track)
        self.msg_timestamps = self.msg_counts.msg_timestamps

        self._contains_msg_types()

        self.n_messages = len(self.track)

        self.only_notes: Union[MidiTrack, None] = self._only_notes()
        self.only_meta: Union[MidiTrack, None] = self._only_meta()
        self.only_tempo: Union[MidiTrack, None]

    def _contains_msg_types(self):
        """
        Check self.message_counts to determine if certain message types are present
        """
        self.contains_notes = False
        self.contains_meta = False
        self.contains_set_tempo = False

        msg_counts = self.msg_counts
        if (msg_counts.note_on + msg_counts.note_off) > 0:
            self.contains_notes = True
        if msg_counts.meta > 0:
            self.contains_meta = True
        if msg_counts.set_tempo > 0:
            self.contains_set_tempo = True

    def _only_notes(self) -> Union[MidiTrack, None]:
        """
        Returns only messages which are either "note_on" or "note_off"
        """

        if self.contains_notes:
            only_notes = MidiTrack()
            for msg in self.track:
                if msg.type in {"note_on", "note_off"}:
                    only_notes.append(msg)
            return only_notes
        else:
            return None

    def _only_meta(self) -> Union[MidiTrack, None]:

        if self.contains_meta:
            only_meta = MidiTrack()
            for msg in self.track:
                if msg.is_meta:
                    only_meta.append(msg)
            return only_meta
        else:
            return None

    def __contains_tempo(self):

        self.contains_tempo = False
        if self.contains_meta:
            self.only_tempo = MidiTrack()
            for msg in self.only_meta:
                if msg.type == "set_tempo":
                    self.contains_tempo = True
                    self.only_tempo.append(msg)


@dataclass
class MidInfo:
    # MidiFile-level attributes
    mid: MidiFile = field(repr=False)

    type: Optional[str] = None
    n_tracks: Optional[int] = None
    ticks_per_beat: Optional[int] = None

    # MidiTrack-level attributes
    track_info: List[MidTrackInfo] = field(default=None, repr=False)
    tracks: List[MidiTrack] = field(default=None, repr=False)

    tempo_is_uniform: Optional[bool] = None
    tempo_ticks: Optional[int] = None
    tempo_bpm: Optional[int] = None

    def __post_init__(self):
        self.type = self.mid.type
        self.n_tracks = len(self.mid.tracks)
        self.ticks_per_beat = self.mid.ticks_per_beat

        self._set_track_info()

    def _set_track_info(self):

        self.track_info = list()
        self.tracks = list()
        for i, track in enumerate(self.mid.tracks):
            mt_info = MidTrackInfo(track=track,
                                   track_number=i)

            self.track_info.append(mt_info)
            self.tracks.append(mt_info.track)

    def _set_tempo_info(self):
        pass

    def get_note_tracks(self, strip=False) -> List[MidiTrack]:
        """
        Return only tracks which contain note_vals

        :param strip : if True, remove all non-item messages from track
        """

        note_tracks = list()
        for track_info in self.track_info:
            if track_info.contains_notes:
                note_tracks.append(track_info.track)

        if strip:
            stripped_tracks = list()
            for track in note_tracks:
                stripped_track = MidiTrack()
                for msg in track:
                    if msg.type in {"note_on", "note_off"}:
                        stripped_track.append(msg)
                stripped_tracks.append(stripped_track)
            return stripped_tracks

        else:
            return note_tracks



