from typing import Collection, Union, List, Optional, Sequence

import numpy as np
from mido import MidiFile, MidiTrack, Message

from MidiCompose.logic.harmony.note import Note
from MidiCompose.logic.melody.melody import Melody
from MidiCompose.logic.rhythm.part import Part
from MidiCompose.translation import state_translation as st

#### OBJECTS ####


#### MESSAGE PROTOCOLS ####

def ofn(timedelta, off_note=64, on_note=64, channel=0, velocity=64) -> List[Message]:
    """
    ofn "off on" is used when simultaneously sending "note_off" and "note_on" messages.
    eg]
        [...,
         Message(type="note_off",item=<off_note>,timedelta=<timedelta>),
         Message(type="note_on",item=<on_note>,timedelta=0))
         ...]
    """
    msgs = [Message(type="note_off", note=off_note, channel=channel, time=timedelta),
            Message(type="note_on", note=on_note, channel=channel, velocity=velocity, time=0)]
    return msgs


def on_poly(timedelta: int,
            note_vals: Sequence[int],
            channels: Union[int, Sequence[int]] = 0,
            velocities: Union[int, Sequence[int]] = 80) -> List[Message]:
    if type(channels) == int:
        channels = [channels for _ in range(len(note_vals))]
    if type(velocities) == int:
        velocities = [velocities for _ in range(len(note_vals))]

    if (len(channels) or len(velocities)) != len(note_vals):
        msg = "The number of `channels` and `velocities` must match the number of `note_vals`."
        raise ValueError(msg)

    msgs = [Message(type="note_on", time=timedelta, note=note_vals[0],
                    velocity=velocities[0], channel=channels[0])]
    msgs.extend([Message(type="note_on", time=0, note=n, velocity=v, channel=c)
                 for n, c, v in zip(note_vals[1:], channels[1:], velocities[1:])])
    return msgs


def off_poly(timedelta: int,
             note_vals: Sequence[int],
             channels: Union[int, Sequence[int]] = 0) -> List[Message]:
    if type(channels) == int:
        channels = [channels for _ in range(len(note_vals))]

    if len(channels) != len(note_vals):
        msg = "The number of `channels` must match the number of `note_vals`."
        raise ValueError(msg)

    msgs = [Message(type="note_off", time=timedelta, note=note_vals[0], channel=channels[0])]
    msgs.extend([Message(type="note_off", time=0, note=n, channel=c)
                 for n, c in zip(note_vals[1:], channels[1:])])

    return msgs


def ofn_poly(timedelta: int,
             off_note_vals: Sequence[int],
             on_note_vals: Sequence[int],
             channels: Union[int, Sequence[int]] = 0,
             velocities: Union[int, Sequence[int]] = 80) -> List[Message]:
    if len(off_note_vals) != len(on_note_vals):
        msg = "`off_note_vals` and `on_note_vals` must be of equal size."
        raise ValueError(msg)

    if type(channels) == int:
        channels = [channels for _ in range(len(on_note_vals))]
    if type(velocities) == int:
        velocities = [velocities for _ in range(len(on_note_vals))]
    if (len(channels) or len(velocities)) != len(on_note_vals):
        msg = "The number of `channels` and `velocities` must match the number of `note_vals`."
        raise ValueError(msg)

    msgs = [Message(type="note_off", time=timedelta, note=off_note_vals[0], channel=channels[0])]

    msgs.extend([Message(type="note_off", time=0, note=_note, channel=channels[i + 1])
                 for i, _note in enumerate(off_note_vals[1:])])
    msgs.extend([Message(type="note_on", time=0, note=_note, channel=channels[i], velocity=velocities[i])
                 for i, _note in enumerate(on_note_vals)])
    return msgs

#### TRACK ####
def track_from_messages(messages: Collection[Message]) -> MidiTrack:
    return MidiTrack(messages)


#### FILE ####

def mid_from_tracks(tracks: Collection[MidiTrack],
                    tpb) -> MidiFile:
    mid = MidiFile()
    mid.ticks_per_beat = tpb
    [mid.tracks.append(t) for t in tracks]
    return mid


def save_mid(mid: MidiFile,
             path: str) -> None:
    mid.save(path)


#### STATEPARSER HELPERS ####

def translate_single_part(part: Part,
                          melodies: Union[Melody, Note],
                          channels: Sequence[int],
                          tpb: int = 480) -> List[Message]:
    # get figure attributes
    state_attrs = st.get_state_attributes(part.state, tpb=tpb)

    # unpack figure attributes
    timedelta = state_attrs.timedelta
    msg_types = state_attrs.msg_types
    total_ticks = state_attrs.total_ticks

    # get messages
    messages = []
    idx_melodies = [0 for _ in melodies]
    for idx_timedelta, _timedelta in enumerate(timedelta):  # for each timedelta

        timedelta_used = False

        for j, melody in enumerate(melodies):

            # handle concurrent msg_attrs
            if timedelta_used:
                _time = 0
            else:
                _time = _timedelta

            # parse message types
            msg_type = msg_types[idx_timedelta]

            # current channel
            channel = channels[j]

            # current melodies
            current_idx_melody = idx_melodies[j]

            if current_idx_melody < len(melody):
                current_note = melody.notes[current_idx_melody].value
                velocity = melody.velocity[current_idx_melody]

            if current_idx_melody > 0:
                previous_note = melody.notes[current_idx_melody - 1].value

            if msg_type == "-4":
                continue

            elif msg_type == "ofn":
                messages.extend(ofn(timedelta=_time,
                                    off_note=previous_note, on_note=current_note,
                                    channel=channel, velocity=velocity))
                timedelta_used = True
                idx_melodies[j] += 1

            elif msg_type == "note_on":

                messages.append(Message(type=msg_type, time=_time, note=current_note,
                                        channel=channel, velocity=velocity))
                timedelta_used = True
                idx_melodies[j] += 1

            elif msg_type == "note_off":

                messages.append(Message(type=msg_type, time=_time, note=previous_note,
                                        channel=channel, velocity=velocity))
                timedelta_used = True

    # send final "note_off" message
    remaining_ticks = total_ticks - np.sum(timedelta)
    messages.append(Message(type="note_off", time=remaining_ticks))

    return messages


def translate_multi_part(parts: Sequence[Part],
                         melodies: Sequence[Melody],
                         channels: Sequence[int],
                         tpb: int = 480) -> List[Message]:
    # parallel attributes
    parallel_attrs = st.get_parallel_attrs(states=[p.state for p in parts], tpb=tpb)

    # consolidated attributes (merged timedelta)
    cons_attrs = parallel_attrs.cons_attributes

    timedelta = cons_attrs.cons_timedelta
    total_ticks = cons_attrs.total_ticks

    # adjusted attributes (individual message types)
    adj_attrs = parallel_attrs.adj_attributes

    adj_msg_types = [a.adj_msg_types for a in adj_attrs]

    # melodies attributes

    # tracks index of each melodies during iteration
    idx_of_melodies = [0 for _ in range(len(melodies))]
    idx_of_parts = [0 for _ in range(len(adj_msg_types))]

    messages = list()
    for idx_td, _timedelta in enumerate(timedelta):
        timedelta_used = False

        for idx_part, types in enumerate(adj_msg_types):

            if timedelta_used:
                _timedelta = 0

            # ic(idx_part)
            #
            # ic(idx_of_melodies,
            #    idx_of_parts)
            # ic(types)

            _type = types[idx_of_parts[idx_part]]

            # ic(_type)

            if _type == "-4":
                idx_of_parts[idx_part] += 1
                continue

            else:

                current_melody = melodies[idx_part]
                _channel = channels[idx_part]

                # ic(current_melody,_channel)

                if _type == "ofn":

                    _note = current_melody.notes[idx_of_melodies[idx_part]].value
                    _note_previous = current_melody.notes[idx_of_melodies[idx_part] - 1].value
                    _velocity = current_melody.velocity[idx_of_melodies[idx_part]]

                    # ic(_note,_note_previous,_velocity)

                    messages.extend(ofn(timedelta=_timedelta,off_note=_note_previous,
                                        on_note=_note,channel=_channel,velocity=_velocity))

                    timedelta_used = True
                    idx_of_melodies[idx_part] += 1

                elif _type == "note_on":

                    _note = current_melody.notes[idx_of_melodies[idx_part]].value
                    _velocity = current_melody.velocity[idx_of_melodies[idx_part]]

                    messages.append(Message(type=_type,time=_timedelta,note=_note,
                                            channel=_channel,velocity=_velocity))

                    timedelta_used = True
                    idx_of_melodies[idx_part] += 1

                elif _type == "note_off":

                    _note_previous = current_melody.notes[idx_of_melodies[idx_part] - 1].value

                    # ic(_note_previous)

                    messages.append(Message(type=_type,time=_timedelta,note=_note_previous,
                                            channel=_channel))

                    timedelta_used = True

                idx_of_parts[idx_part] += 1

    # send final "note_off" message
    remaining_ticks = total_ticks - np.sum(timedelta)
    messages.append(Message(type="note_off", time=remaining_ticks))

    return messages