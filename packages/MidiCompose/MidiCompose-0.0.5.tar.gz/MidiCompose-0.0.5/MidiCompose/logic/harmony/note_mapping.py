from dataclasses import dataclass
from typing import Optional

import numpy as np


#### NOTE REPRESENTATION MAPPER ####

RANGELESS_NOTES = {
    "C":0,
    "C#":1,
    "Db":1,
    "D":2,
    "D#":3,
    "Eb":3,
    "E":4,
    "F":5,
    "F#":6,
    "Gb":6,
    "G":7,
    "G#":8,
    "Ab":8,
    "A":9,
    "A#":10,
    "Bb":10,
    "B":11
}

@dataclass
class FlatNoteMatrix:
    values: np.ndarray

    letters: np.ndarray
    sharps: np.ndarray
    flats: np.ndarray

@dataclass
class ValueLetter:
    values: np.ndarray
    letters: np.ndarray


@dataclass
class ValueSharp:
    values: np.ndarray
    sharps: np.ndarray


@dataclass
class ValueFlat:
    values: np.ndarray
    flats: np.ndarray


def get_value_range():
    values_range = np.arange(128)
    return values_range


def get_octave_range():
    octaves = np.arange(-2, 9).astype(str)
    octaves_range = octaves.repeat(12)[:128]

    return octaves_range


def get_letter_range(octave_range):
    letters = np.array(["C", "", "D", "", "E", "F", "", "G", "", "A", "", "B"], dtype=str)
    letter_arr = np.tile(letters, 11)[:128]

    letter_range = np.char.add(letter_arr, octave_range)

    return letter_range


def get_sharps_range(octave_range):
    sharps = np.array(["", "C#", "", "D#", "", "", "F#", "", "G#", "", "A#", ""], dtype=str)
    sharps_arr = np.tile(sharps, 11)[:128]
    sharps_range = np.char.add(sharps_arr, octave_range)

    return sharps_range


def get_flats_range(octave_range):
    flats = np.array(["", "Db", "", "Eb", "", "", "Gb", "", "Ab", "", "Bb", ""], dtype=str)
    flats_arr = np.tile(flats, 11)[:128]
    flats_range = np.char.add(flats_arr, octave_range)

    return flats_range


def get_idx_letters(letter_range):
    idx_starts_neg = np.char.startswith(letter_range, prefix="-")
    idx_starts_num = np.char.isnumeric(letter_range)

    idx_letters = np.where(~idx_starts_neg & ~idx_starts_num)

    return idx_letters


def get_idx_sharps(sharps_range):
    idx_starts_neg = np.char.startswith(sharps_range, prefix="-")
    idx_starts_num = np.char.isnumeric(sharps_range)

    idx_sharps = np.where(~idx_starts_neg & ~idx_starts_num)

    return idx_sharps


def get_idx_flats(flats_range):
    idx_starts_neg = np.char.startswith(flats_range, prefix="-")
    idx_starts_num = np.char.isnumeric(flats_range)

    idx_flats = np.where(~idx_starts_neg & ~idx_starts_num)

    return idx_flats


#### DATACLASS FILLERS ####

def populate_FlatNoteMatrix() -> FlatNoteMatrix:
    values = get_value_range()
    octaves = get_octave_range()

    letters = get_letter_range(octaves)
    sharps = get_sharps_range(octaves)
    flats = get_flats_range(octaves)

    return FlatNoteMatrix(values, letters, sharps, flats)


def populate_ValueLetter(letter_range) -> ValueLetter:
    idx_letters = get_idx_letters(letter_range)
    letters = letter_range[idx_letters]

    return ValueLetter(values=idx_letters[0],
                       letters=letters)


def populate_ValueSharp(sharp_range) -> ValueSharp:
    idx_sharps = get_idx_sharps(sharp_range)
    sharps = sharp_range[idx_sharps]

    return ValueSharp(values=idx_sharps[0],
                      sharps=sharps)


def populate_ValueFlat(flat_range) -> ValueFlat:
    idx_flats = get_idx_flats(flat_range)
    flats = flat_range[idx_flats]

    return ValueFlat(values=idx_flats[0],
                     flats=flats)


FLAT_NOTE_MATRIX = populate_FlatNoteMatrix()
VALUE_LETTER = populate_ValueLetter(FLAT_NOTE_MATRIX.letters)
VALUE_SHARP = populate_ValueSharp(FLAT_NOTE_MATRIX.sharps)
VALUE_FLAT = populate_ValueFlat(FLAT_NOTE_MATRIX.flats)


#### MAPPER FUNCTIONS ####

def value_to_letter(value: int,
                    accidental: Optional[str] = None) -> str:

    if value not in range(128):
        msg = f"`value` `{value}` out of range."
        raise ValueError(msg)

    # always try bare letter first
    if value in VALUE_LETTER.values:
        return str(FLAT_NOTE_MATRIX.letters[value])

    elif accidental is None:
        # default flat
        if value in VALUE_FLAT.values:
            return str(FLAT_NOTE_MATRIX.flats[value])

    elif accidental == "sharp":
        # bare letter first
        if value in VALUE_SHARP.values:
            return str(FLAT_NOTE_MATRIX.sharps[value])

    elif accidental == "flat":
        if value in VALUE_FLAT.values:
            return str(FLAT_NOTE_MATRIX.flats[value])

def letter_to_value(letter: str) -> int:
    if letter in RANGELESS_NOTES.keys():
        return RANGELESS_NOTES[letter]
    elif letter[1] == "b":
        if letter in VALUE_FLAT.flats:
            return np.where(FLAT_NOTE_MATRIX.flats == letter)[0][0]
    elif letter[1] == "#":
        if letter in VALUE_SHARP.sharps:
            return np.where(FLAT_NOTE_MATRIX.sharps == letter)[0][0]
    elif letter in VALUE_LETTER.letters:
        return np.where(FLAT_NOTE_MATRIX.letters == letter)[0][0]
    else:
        msg = f"Invalid `letter`: `{letter}`"
        raise ValueError(msg)

