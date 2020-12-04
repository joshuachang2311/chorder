from .dechorder import Dechorder, get_key_from_pitch
from .timepoints import get_notes_by_beat
from miditoolkit.midi import containers


class Acchorder:
    pc_maps = [
        [0, 2, 4, 7, 9, 11],
        [],
        [0, 2, 4, 5, 9],
        [],
        [0, 2, 4, 7, 11],
        [0, 2, 4, 5, 7, 9],
        [],
        [2, 5, 7, 9, 11],
        [],
        [0, 2, 4, 7, 9, 11],
        [],
        [2, 5, 7, 9, 11]
    ]

    @staticmethod
    def get_score_map(note, key, candidate_lists, time_weights, distance_penalty=1):
        pitch = note.pitch - key
        time = note.end - note.start

        score_map = {}
        for candidates, weight in zip(candidate_lists, time_weights):
            for candidate in candidates:
                if candidate not in score_map.keys():
                    score_map[candidate] = weight
                else:
                    score_map[candidate] += weight

        for key in score_map.keys():
            score_map[key] -= abs(pitch - key) * time * distance_penalty

        return score_map

    @staticmethod
    def get_bass_pitch(notes, start=0, end=1e7):
        distribution = Dechorder.get_pitch_distribution(notes, start, end)
        distribution = list(sorted(distribution.items()))
        for pitch, span in distribution:
            if span >= (end - start) / 8:
                return pitch

        return None

    @staticmethod
    def get_bass_list(midi_obj):
        interval = midi_obj.ticks_per_beat
        bass_list = []
        notes_by_beat = get_notes_by_beat(midi_obj)

        for i, notes in enumerate(notes_by_beat):
            bass_list.append(Acchorder.get_bass_pitch(notes, i * interval, (i + 1) * interval))

        return bass_list

    @staticmethod
    def acchord(midi_obj, progression, bpm=120):
        interval = midi_obj.ticks_per_beat
        new_notes = []
        key = get_key_from_pitch(midi_obj)
        bass_list = Acchorder.get_bass_list(midi_obj)

        for note in midi_obj.instruments[0].notes:
            pitch = note.pitch - key
            start_beat = note.start // interval
            end_beat = (note.end - 1) // interval
            candidate_lists = []
            bass_candidates = bass_list[start_beat:end_beat + 1]

            if note.pitch in bass_candidates:
                bass_index = bass_candidates.index(note.pitch)
                if progression[start_beat + bass_index].bass_pc is None:
                    continue
                elif progression[start_beat + bass_index].bass_pc in [1, 3, 6, 10]:
                    continue

                new_pitch = progression[start_beat + bass_index].bass_pc + (pitch // 12) * 12 + key
                new_note = note
                new_note.pitch = new_pitch
                new_notes.append(new_note)

                continue

            time_weights = [interval for i in range(end_beat - start_beat + 1)]
            if start_beat == end_beat:
                time_weights[0] = note.end - note.start
            else:
                time_weights[0] = (start_beat + 1) * interval - note.start
                time_weights[-1] = note.end - end_beat * interval

            for beat in range(start_beat, end_beat + 1):
                chord = progression[beat]
                if not chord.is_complete():
                    candidate_lists.append([])
                    continue
                root, quality, bass = chord.root_pc, chord.quality, chord.bass_pc
                candidates = ([i % 12 + (pitch // 12) * 12 for i in Acchorder.pc_maps[root]] +
                              [i % 12 + (pitch // 12 - 1) * 12 for i in Acchorder.pc_maps[root]])
                candidate_lists.append(candidates)

            score_map = Acchorder.get_score_map(note, key, candidate_lists, time_weights)
            best_pitch = pitch
            best_score = -10e8

            for midi_num, score in score_map.items():
                if score > best_score:
                    best_pitch = midi_num
                    best_score = score
            if best_score == -10e8:
                continue

            pitch = best_pitch + key
            new_note = note
            new_note.pitch = pitch
            new_notes.append(new_note)

        new_obj = midi_obj
        new_obj.instruments[0].notes = new_notes
        new_obj.tempo_changes = [containers.TempoChange(tempo=bpm, time=0)]

        return new_obj
