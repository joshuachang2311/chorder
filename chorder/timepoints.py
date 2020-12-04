from _collections import OrderedDict


def get_timepoints(midi_obj):
    timepoints = {}
    for instrument in midi_obj.instruments:
        for note in instrument.notes:
            start = note.start
            end = note.end
            new_note = note
            new_note.instrument = instrument
            new_note.dur = end - start

            if note.start in timepoints.keys():
                timepoints[start].append(new_note)
            else:
                timepoints[start] = [new_note]

    return OrderedDict(sorted(timepoints.items()))


def get_notes_at(timepoints, start=0, end=1e7):
    notes = []
    l_index = 0
    r_index = len(timepoints)
    start_index = -1
    end_index = -1

    while l_index < r_index:
        m = int((l_index + r_index) / 2)
        if list(timepoints.keys())[m] < start:
            l_index = m + 1
        else:
            r_index = m
    start_index = max(l_index - 10, 0)

    l_index = 0
    r_index = len(timepoints)
    while l_index < r_index:
        m = int((l_index + r_index) / 2)
        if list(timepoints.keys())[m] < end:
            l_index = m + 1
        else:
            r_index = m
    end_index = l_index

    partial_timepoints = list(timepoints.items())[start_index:end_index]
    for start_time, timepoint_notes in partial_timepoints:
        for note in timepoint_notes:
            end_time = start_time + note.dur
            if start_time < end and end_time >= start:
                notes.append(note)

    return notes


def get_notes_by_beat(midi_obj, beat=1):
    tick_interval = midi_obj.ticks_per_beat * beat
    timepoints = get_timepoints(midi_obj)
    notes = []

    for tick_time in range(0, midi_obj.max_tick, tick_interval):
        notes.append(get_notes_at(timepoints, tick_time, tick_time + tick_interval))

    return notes
