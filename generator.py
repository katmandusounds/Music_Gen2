import os
import random
import pandas as pd
import json
import pretty_midi

METADATA_DIR = 'metadata'
MIDI_CHORD_DIR = 'midi/chords'
MIDI_DRUM_DIRS = {
    'hihat': 'midi/drums/drill/drill hihat midi',
    'kick': 'midi/drums/drill/drill kick midi',
    'perc': 'midi/drums/drill/drill perc midi',
    'snare': 'midi/drums/drill/drill snare midi'
}
OUTPUT_DIR = 'output'
PALETTES_DIR = 'palettes'

def normalize_key(key_str):
    k = str(key_str).strip().lower().replace(' ', '')
    if k in ['c', 'cmaj', 'cmajor']:
        return 'cmajor'
    if k in ['a', 'amin', 'aminor', 'am']:
        return 'aminor'
    return k

def load_metadata():
    metadata = {}
    metadata['progressions'] = pd.read_csv(os.path.join(METADATA_DIR, 'chord_progressions.csv'))
    with open(os.path.join(PALETTES_DIR, 'mood_scales.json')) as f:
        metadata['mood_scales'] = json.load(f)
    return metadata

def merge_chord_midis(progression, bars, bpm):
    chord_inst = pretty_midi.Instrument(program=0)      # Piano
    bass_inst = pretty_midi.Instrument(program=33)       # Electric Bass
    bar_len = 60 / bpm * 4
    prog_steps = progression.split(',')
    roman_to_root = {'1': 60, '2': 62, '3': 64, '4': 65, '5': 67, '6': 69, '7': 71,
                     'I': 60, 'ii': 62, 'iii': 64, 'IV': 65, 'V': 67, 'vi': 69, 'vii': 71}
    for i in range(bars):
        roman = prog_steps[i % len(prog_steps)].strip()
        midi_file = os.path.join(MIDI_CHORD_DIR, f"{roman}.mid")
        if not os.path.exists(midi_file):
            # Try lower-case
            midi_file = os.path.join(MIDI_CHORD_DIR, f"{roman.lower()}.mid")
        if not os.path.exists(midi_file):
            print(f"Warning: Missing MIDI for chord {roman} at bar {i+1}!")
            continue
        chord_midi = pretty_midi.PrettyMIDI(midi_file)
        # Place chord notes
        for note in chord_midi.instruments[0].notes:
            new_note = pretty_midi.Note(
                velocity=note.velocity,
                pitch=note.pitch,
                start=i * bar_len,
                end=(i+1) * bar_len
            )
            chord_inst.notes.append(new_note)
        # Bass: root of the chord, one octave down (if using Roman numerals or numbers)
        root_pitch = None
        if roman in roman_to_root:
            root_pitch = roman_to_root[roman] - 12
        elif roman.isdigit() and roman in roman_to_root:
            root_pitch = roman_to_root[roman] - 12
        if root_pitch:
            bass_inst.notes.append(pretty_midi.Note(
                velocity=80,
                pitch=root_pitch,
                start=i * bar_len,
                end=(i+1) * bar_len
            ))
    return [chord_inst, bass_inst]

def add_generated_melody(bars, bpm, chord_prog, mood_notes, is_main=True):
    melody_inst = pretty_midi.Instrument(program=40 if is_main else 41)  # 40: Violin, 41: Viola
    bar_len = 60 / bpm * 4
    notes_per_bar = random.randint(4, 6) if is_main else random.randint(2, 4)
    prog_steps = chord_prog.split(',')
    note_name_to_index = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    for i in range(bars):
        allowed_notes = mood_notes
        note_durations = bar_len / notes_per_bar
        for j in range(notes_per_bar):
            note_name = random.choice(allowed_notes)
            # Map to MIDI pitch (one octave up, C5 = 72)
            base_pitch = 60 + 12  # C5 = 72
            pitch = base_pitch + note_name_to_index.get(note_name[0].upper(), 0)
            velocity = random.randint(60, 100)
            melody_inst.notes.append(pretty_midi.Note(
                velocity=velocity,
                pitch=pitch,
                start=i * bar_len + j * note_durations,
                end=i * bar_len + (j+1) * note_durations
            ))
    return melody_inst

def add_drum_midi(master_midi, drum_folder, bpm, bars):
    bar_len = 60 / bpm * 4
    drum_files = [f for f in os.listdir(drum_folder) if f.endswith('.mid')]
    if not drum_files:
        print(f"No drum MIDIs found in {drum_folder}")
        return
    midi_path = os.path.join(drum_folder, random.choice(drum_files))
    drum_midi = pretty_midi.PrettyMIDI(midi_path)
    drum_track_length = drum_midi.get_end_time()
    repetitions = int((bars * bar_len) // drum_track_length) + 1
    for rep in range(repetitions):
        offset = rep * drum_track_length
        for inst in drum_midi.instruments:
            new_inst = pretty_midi.Instrument(program=inst.program, is_drum=True)
            for note in inst.notes:
                new_note = pretty_midi.Note(
                    velocity=note.velocity,
                    pitch=note.pitch,
                    start=note.start + offset,
                    end=note.end + offset
                )
                new_inst.notes.append(new_note)
            master_midi.instruments.append(new_inst)




def main():
    meta = load_metadata()
    progressions = meta['progressions']
    progressions['key_norm'] = progressions['key'].apply(normalize_key)
    valid_progressions = progressions[progressions['key_norm'].isin(['cmajor', 'aminor'])]
    if valid_progressions.empty:
        print("Available keys in your chord_progressions.csv:")
        print(progressions['key'].unique())
        print("Normalized keys:")
        print(progressions['key_norm'].unique())
        raise ValueError("No progressions available for Cmaj or Amin!")
    progression = valid_progressions.sample(1).iloc[0]
    bpm = int(progression.get('bpm', 140))
    total_bars = 112
    # Select mood from palettes
    mood = random.choice(list(meta['mood_scales'].keys()))
    mood_notes = meta['mood_scales'][mood]

    print(f"Progression: {progression['progression']} | Mood: {mood} | BPM: {bpm}")

    master_midi = pretty_midi.PrettyMIDI()
    # Chords and bass
    chord_inst, bass_inst = merge_chord_midis(progression['progression'], total_bars, bpm)
    master_midi.instruments.append(chord_inst)
    master_midi.instruments.append(bass_inst)
    # Main and sub melody
    main_melody = add_generated_melody(total_bars, bpm, progression['progression'], mood_notes, is_main=True)
    sub_melody = add_generated_melody(total_bars, bpm, progression['progression'], mood_notes, is_main=False)
    master_midi.instruments.append(main_melody)
    master_midi.instruments.append(sub_melody)
    # Add drum parts (hihat, kick, perc, snare)
    for dtype, dpath in MIDI_DRUM_DIRS.items():
        add_drum_midi(master_midi, dpath, bpm, total_bars)
    # Save
    output_file = os.path.join(OUTPUT_DIR, 'generated_song_full.mid')
    master_midi.write(output_file)
    print(f"Exported full song MIDI to {output_file}")

if __name__ == "__main__":
    main()
