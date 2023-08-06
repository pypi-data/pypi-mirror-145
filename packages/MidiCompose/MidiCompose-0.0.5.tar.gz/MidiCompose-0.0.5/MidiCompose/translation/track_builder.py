from typing import Union, Sequence, List, Optional

from mido import Message, MidiTrack, bpm2tempo, MetaMessage

from MidiCompose.logic.harmony.note import Note
from MidiCompose.logic.melody.melody import Melody
from MidiCompose.logic.rhythm.part import Part
from MidiCompose.translation import midi_translation as mt

from icecream import ic as ice, ic

# TODO: to_track() -> MidiTrack
class TrackBuilder:
    """
    Class for combining rhythmic figure objects (Beat,Measure,Part) with appropriately sized melodic objects,
    and parsing these objects into arrays of midi-message attributes.

    Crucial property is self.parsed, which is a list of dictionaries containing midi-message attributes.

    Various parsing scenarios:
        - Single figure, single melodies
        - Single figure, multiple melodies
        - Multiple figure (of equal size), single melodies per figure
        - Multiple figure, multiple melodies per figure

    When multiple states (ie. multiple voices), option to "decouple" voices into separate tracks.

    Requires "rhythmic container(s)" as well as appropriately-sized "Melody-like" arrays of notes.

    Message attributes `type` and `time` come from rhythmic containers.
    Message attribute `item` given by Melody object (or any sequence of Note objects)
    Message attribute `channels` given as argument to parser


    """

    def __init__(self,
                 parts: Sequence[Part],
                 melodies: Sequence[Union[Note, Melody]],
                 channels: Optional[Sequence[int]] = None,
                 bpm: int = 60,
                 tpb: int = 480):

        self.parts = parts  # calls setter
        self.melodies = melodies  # calls setter
        self.channels = channels  # calls setter
        self.bpm = bpm

        self.tpb = tpb

    @property
    def parts(self) -> List[Part]:
        return self._parts

    @parts.setter
    def parts(self, value: Sequence[Part]):

        _parts = None
        if set([type(v) for v in value]) == {Part}:
            _parts = list(value)
        else:
            msg = "`part` must consist only of `Part` instances."
            raise ValueError(msg)

        self._parts = _parts

    @property
    def melodies(self) -> List[Melody]:
        return self._melodies

    @melodies.setter
    def melodies(self, value: Sequence[Union[Note, Melody]]):

        _melodies = None

        # if is_multi_part, must have number of melodies as part
        if self.is_multi_part:
            if len(value) != len(self.parts):
                msg = "Must give equal number of items for `part` and `melodies` when parsing multiple part."
                raise ValueError(msg)

        value_typeset = set([type(v) for v in value])

        _note_typeset = {Note}
        _melody_typeset = {Melody}
        _mixed_typeset = {Note, Melody}

        #### SEQUENCE OF NOTES ####
        if value_typeset == _note_typeset:
            # must be unique
            _note_set = set(value)
            if len(_note_set) != len(value):
                msg = "If giving sequence of Notes, all Notes must be unique."
                raise ValueError(msg)
            else:
                _melodies = []
                if self.is_multi_part:
                    for note, part in zip(value, self.parts):
                        _melodies.append(Melody([note for _ in range(part.n_note_on)]))
                else:  # single part, all melodies same size
                    for note in value:
                        _melodies.append(Melody([note for _ in range(self.parts[0].n_note_on)]))

        #### SEQUENCE OF MELODIES ####
        elif value_typeset == _melody_typeset:

            # single part, all melodies must have proper n_notes
            if not self.is_multi_part:
                _n_note_on = self.parts[0].n_note_on
                n_note_set = set([len(v) for v in value])
                if n_note_set != {_n_note_on}:
                    msg = "If giving multiple `Melody` for single `Part`, all melodies must have the same number of" \
                          "notes as part has `n_note_on`."
                    raise ValueError(msg)
                else:  # item counts are equal
                    _melodies = list(value)

            # multiple part, all melodies must have proper n_notes
            else:
                _parts_n_note_on = [p.n_note_on for p in self.parts]
                melodies_n_notes = [len(v) for v in value]
                if not melodies_n_notes == _parts_n_note_on:
                    msg = "If giving multiple `Part` and multiple `Melody`, there must be a one-to-one correspondence" \
                          "between `Part.n_note_on` and size of `Melody`."
                    raise ValueError(msg)
                else:
                    _melodies = list(value)

        #### MIXTURE OF MELODY AND NOTE ####
        elif value_typeset == _mixed_typeset:
            ic("mixed!")
            if not self.is_multi_part:  # single part
                part_n_note_on = self.parts[0].n_note_on
                _melodies = list()
                for v in value:
                    if isinstance(v, Note):
                        note = v
                        _melodies.append(Melody([v for _ in range(part_n_note_on)]))
                    elif isinstance(v, Melody):
                        mel_n_notes = len(v)
                        if mel_n_notes != part_n_note_on:
                            msg = "If giving multiple `Part` and multiple `Melody`, there must be a one-to-one correspondence" \
                                  "between `Part.n_note_on` and size of `Melody`."
                            raise ValueError(msg)
                        else:
                            _melodies.append(v)
            else:  # multi part
                _parts_n_note_on = [p.n_note_on for p in self.parts]
                _melodies = list()
                for i,v in enumerate(value):
                    if isinstance(v,Melody):
                        if len(v) != _parts_n_note_on[i]:
                            e = "Size of `Melody` must match n_note_on in corresponding `Part`"
                            raise ValueError(e)
                        else:
                            _melodies.append(v)
                    elif isinstance(v,Note):
                        _melodies.append(Melody([v for _ in range(_parts_n_note_on[i])]))

        self._melodies = _melodies

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, value: Optional[Sequence[int]] = None):

        _channels = None

        # if None, one channel per Melody
        if value is None:
            _channels = [0 for _ in range(len(self.melodies))]

        else:
            e = "IMPLEMENT CHANNELS SETTER!"
            raise NotImplementedError(e)

        self._channels = _channels

    @property
    def is_multi_part(self) -> bool:
        """
        Evaluates to True if `self` self contains multiple rhythmic `Part` objects.
        """

        _multi_part = None
        if len(self.parts) > 1:
            _multi_part = True
        else:
            _multi_part = False
        return _multi_part

    def get_messages(self) -> List[Union[Message,MetaMessage]]:

        messages = None

        if self.is_multi_part:
            messages = self._parse_multi_part()
        elif not self.is_multi_part:
            messages = self._parse_single_part()

        _tempo = bpm2tempo(self.bpm)
        messages.insert(0,MetaMessage(type="set_tempo",tempo=_tempo))

        return messages

    def get_track(self) -> MidiTrack:


        _messages = self.get_messages()


        return MidiTrack(_messages)

    def _parse_single_part(self) -> List[Message]:

        ice("parsing single-part")
        messages = mt.translate_single_part(self.parts[0],self.melodies,self.channels,self.tpb)

        return messages

    def _parse_multi_part(self) -> List[Message]:

        messages = mt.translate_multi_part(self.parts,self.melodies,self.channels,self.tpb)
        return messages

    #### MAGIC METHODS ####

    def __repr__(self):

        _tab = '   '
        header = "TrackBuilder(\n"
        parts = "\n".join([_tab + str(p) for p in self.parts])
        melodies = "\n".join([_tab + str(m) for m in self.melodies])

        r = header + parts + "\n" + melodies + "\n)"

        return r


