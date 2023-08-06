from dataclasses import dataclass
from typing import List, Collection

import numpy as np


#### CONTAINER OBJECTS ####

## FOR SINGLE-STATE ##
@dataclass
class StateAttributes:
    active_state: np.ndarray
    total_ticks: int
    ticks_per_beat: int

    sub_values: np.ndarray
    ticks_per_sub: np.ndarray
    timestamp: np.ndarray

    active_state_comp: np.ndarray
    timestamp_comp: np.ndarray
    timedelta: np.ndarray
    msg_types: np.ndarray


## FOR MULTI-STATE ##

@dataclass
class AdjustedAttributes:
    adj_timestamp: np.ndarray
    adj_msg_types: np.ndarray


@dataclass
class ConsolidatedAttributes:
    cons_timestamp: np.ndarray
    cons_timedelta: np.ndarray
    total_ticks: int
    ticks_per_beat: int


@dataclass
class ParallelAttributes:
    """
    Container used for generating midi from parallel figure.
    """
    cons_attributes: ConsolidatedAttributes
    adj_attributes: List[AdjustedAttributes]


#### ATTRIBUTE GETTER FUNCTIONS ####

#### DEPENDENCE: 0 ####

def get_active_state(state: np.ndarray) -> np.ndarray:

    idx_sub_flags = np.where(state == -3)[0]
    idx_sub_values = idx_sub_flags + 1
    idx_flags_and_values = np.union1d(idx_sub_flags, idx_sub_values)

    part_measure_flags = np.where((state == -1) | (state == -2))[0]
    idx_not_active = np.union1d(part_measure_flags, idx_flags_and_values)

    mask = np.ones_like(state, bool)
    mask[idx_not_active] = False
    active_state = state[mask]

    return active_state


def get_ticks_per_sub(sub_values: np.ndarray,
                      tpb: int):
    """
    Returns a 1d array where each element represents the number of ticks in that
    particular subdivision.

    PARAMETERS DEPEND ON:
        - get_subdivision_flags()
    """

    # get ticks per sub
    tick_values = tpb // sub_values
    ticks_per_sub = np.repeat(tick_values, sub_values)

    return ticks_per_sub

def get_subdivision_values(state: np.ndarray) -> np.ndarray:
    """
    Returns array where each element represents the number of subdivisions within a time_units.
    """

    idx_sub_flag = np.where(state == -3)[0] + 1
    sub_vals = np.take(state, idx_sub_flag)

    return sub_vals

#### DEPENDENCE: 2 ####

def get_size_of_active_state(active_st: np.ndarray):
    return active_st.size


def get_total_ticks(ticks_per_sub: np.ndarray) -> int:
    """
    Returns total number of ticks in State.
    """
    return ticks_per_sub.sum(dtype=int)


def get_timestamp(active_st: np.ndarray,
                  ticks_per_sub: np.ndarray):
    """
    Get the array which represents the absolute timedelta for each TimeUnit in a midi-figure.
    """
    size_st = active_st.size

    # initialize empty array of size n+1 compared to active figure
    abs_time = np.zeros(shape=(size_st + 1,), dtype=int)
    abs_time[1:] = np.cumsum(ticks_per_sub)

    return abs_time


def get_active_state_comp(active_st: np.ndarray) -> np.ndarray:
    """
    Strips all "sustain" (2) instances from buffered figure so that there's a one-to-one
    relationship between figure and timedelta attributes.
    """
    return active_st[active_st != 2]


def get_timestamp_comp(active_st: np.ndarray,
                       timestamp: np.ndarray):
    idx_active_st_comp = np.where((active_st == 1) | (active_st == 0))
    timestamp_comp = timestamp[:-1][idx_active_st_comp]
    return timestamp_comp


def get_msg_types(active_st_comp: np.ndarray):
    asc = active_st_comp

    idx_off = np.where(asc == 0)[0]
    idx_on = np.where(asc == 1)[0]

    # get idx ofn
    idx_elements_equal = np.where(asc[1:] == asc[:-1])[0] + 1
    idx_ofn = np.intersect1d(idx_on, idx_elements_equal)

    msg_types = np.empty(shape=asc.shape, dtype=object)
    msg_types[idx_on] = "note_on"
    msg_types[idx_off] = "note_off"
    msg_types[idx_ofn] = "ofn"

    return msg_types


#### DEPENDENCE: 3 ####

def get_timedelta(timestamp_comp: np.ndarray):

    timedelta = np.zeros(shape=timestamp_comp.shape, dtype=int)
    timedelta[1:] = timestamp_comp[1:] - timestamp_comp[:-1]

    return timedelta


#### MULTI-STATE ####

def get_cons_abs_ts_comp(abs_times: Collection[np.ndarray]):
    """
    Given 2 or more abs_time arrays, return consolidated array.

    Used for mapping parallel states into a single track.
    """

    consolidated = np.zeros(shape=(1,), dtype=int)
    for _abs in abs_times:
        consolidated = np.union1d(_abs, consolidated, )

    return consolidated


#### ATTRIBUTE-CONTAINER SETTERS ####

## MULTIPLE STATE ##

def _get_multiple_state_attributes(states: Collection[np.ndarray],
                                   tpb: int) -> List[StateAttributes]:
    return [get_state_attributes(s, tpb) for s in states]


def _get_consolidated_attrs(state_attrs: List[StateAttributes]) -> ConsolidatedAttributes:
    # get consolidated absolute timestamps
    cons_timestamp = get_cons_abs_ts_comp([sa.timestamp_comp for sa in state_attrs])
    # get consolidated timedelta
    cons_timedelta = get_timedelta(cons_timestamp)

    total_ticks = []
    tpb = []
    for sa in state_attrs:
        total_ticks.append(sa.total_ticks)
        tpb.append(sa.ticks_per_beat)

    # total_ticks must be uniform
    if len(set(total_ticks)) != 1:
        msg = f"All child `states` must contain the same `total_ticks`."
        raise Exception(msg)
    else:
        total_ticks = total_ticks[0]

    # ticks_per_beat must be uniform
    if len(set(tpb)) != 1:
        msg = f"All child `states` must have the same `ticks_per_beat`."
        raise Exception(msg)
    else:
        tpb = tpb[0]

    return ConsolidatedAttributes(cons_timestamp=cons_timestamp,
                                  cons_timedelta=cons_timedelta,
                                  total_ticks=total_ticks,
                                  ticks_per_beat=tpb)


def _get_adjusted_attrs(state_attrs: List[StateAttributes],
                        cons_attrs: ConsolidatedAttributes) -> List[AdjustedAttributes]:
    adjusted_attrs = list()

    # adjust active_state, msg_type, etc to match consolidated timedelta by comparing absolute timestamps
    for sa in state_attrs:
        # boolean mask to match indeces of individual states with consolidated timestamps
        mask_ts_in_cons = np.in1d(cons_attrs.cons_timestamp,
                                  sa.timestamp_comp)

        # adjusted absolute timestamp
        adj_abs_ts_comp = np.where(mask_ts_in_cons,
                                   cons_attrs.cons_timestamp,
                                   -4)
        # adjusted msg type
        adj_msg_types = np.full(shape=cons_attrs.cons_timestamp.shape,
                                fill_value="-4",
                                dtype=object)
        idx_adj = np.where(adj_abs_ts_comp != -4)
        adj_msg_types[idx_adj] = sa.msg_types

        adj_attrs = AdjustedAttributes(adj_timestamp=adj_abs_ts_comp,
                                       adj_msg_types=adj_msg_types)

        adjusted_attrs.append(adj_attrs)

    return adjusted_attrs


def _get_parallel_attrs(cons_attrs: ConsolidatedAttributes,
                        adj_attrs: List[AdjustedAttributes]) -> ParallelAttributes:
    return ParallelAttributes(cons_attrs,
                              adj_attrs)


#### MAIN ####

def get_state_attributes(state: np.ndarray,
                         tpb: int) -> StateAttributes:
    """

    """
    sub_values = get_subdivision_values(state=state)
    active_state = get_active_state(state=state)

    ticks_per_sub = get_ticks_per_sub(sub_values=sub_values,
                                      tpb=tpb)
    total_ticks = get_total_ticks(ticks_per_sub=ticks_per_sub)

    timestamp = get_timestamp(active_st=active_state,
                              ticks_per_sub=ticks_per_sub)

    active_state_comp = get_active_state_comp(active_st=active_state)
    timestamp_comp = get_timestamp_comp(active_st=active_state,
                                        timestamp=timestamp)
    timedelta = get_timedelta(timestamp_comp=timestamp_comp)
    msg_types = get_msg_types(active_st_comp=active_state_comp)

    state_attributes = StateAttributes(
        active_state=active_state,
        sub_values=sub_values,
        ticks_per_sub=ticks_per_sub,
        total_ticks=total_ticks,
        timestamp=timestamp,
        active_state_comp=active_state_comp,
        timestamp_comp=timestamp_comp,
        timedelta=timedelta,
        msg_types=msg_types,
        ticks_per_beat=tpb
    )

    return state_attributes


def get_parallel_attrs(states: Collection[np.ndarray],
                       tpb: int):

    state_attrs = _get_multiple_state_attributes(states, tpb)
    cons_attrs = _get_consolidated_attrs(state_attrs)
    adj_attrs = _get_adjusted_attrs(state_attrs, cons_attrs)

    return _get_parallel_attrs(cons_attrs, adj_attrs)
