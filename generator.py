import pandas as pd
import os
import pretty_midi
import random

# === CONFIG ===
CSV_CHORD_PROG = 'metadata/chord_progressions.csv'
MIDI_CHORD_DIR = 'midi/chords'
MIDI_DRUM_DIR = 'midi/drums'
OUTPUT_DIR = 'output'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'generated_song_full.mid')
SONG_BARS = 112

# === UTILS ===
def select_progression(csv_path, midi_dir):
    df = pd.read_csv(csv_path)
    df['midi_exists'] = df['midi_filename'].apply(lambda x: os.path.isfile(os.path.join(midi_dir, x)))
    available = df[df['midi_exists']]
    if available.empty:
        raise ValueError("No progressions have matching MIDI files!")
    row = available.sample(1).iloc[0]
    print(f"Selected progression: {row['progression']} | File: {row['midi_filename']} | BPM: {row['bpm']} | Mood: {row['style']}")
    return row

def repeat_full_progression_midi(midi_path, bars_needed, bpm):
    midi = pretty_midi.PrettyMIDI(midi_path)
    bar_len = 60 / bpm * 4
    orig_bars = int(midi.get_end_time() // bar_len)
    if orig_bars == 0:
        raise ValueError(f"Original progression midi '{midi_path}' has zero bars!")
    repetitions = int(bars_needed // orig_bars) + 1
    instruments = []
    for inst in midi.instruments:
        new_inst = pretty_midi.Instrument(program=inst.program, is_drum=inst.is_drum, name=inst.name)
        for rep in range(repetitions):
            offset = rep * orig_bars * bar_len
            for note in inst.notes:
                new_note = pretty_midi.Note(
                    velocity=note.velocity,
                    pitch=note.pitch,
                    start=note.start + offset,
                    end=note.end + offset
                )
                new_inst.notes.append(new_note)
        instruments.append(new_inst)
    return instruments, orig_bars

def pick_drum_midi(genre, midi_drum_dir):
    """Pick a random drum midi for the genre (trap/drill)"""
    folder = os.path.join(midi_drum_dir, genre)
    if not os.path.isdir(folder):
        print(f"No drum folder for genre '{genre}'. Skipping drums.")
        return None
    files = [f for f in os.listdir(folder) if f.lower().endswith('.mid')]
    if not files:
        print(f"No drum midi files found in {folder}. Skipping drums.")
        return None
    chosen = random.choice(files)
    print(f"Selected drum midi: {chosen}")
    return os.path.join(folder, chosen)

def repeat_drum_midi(midi_path, bars_needed, bpm):
    midi = pretty_midi.PrettyMIDI(midi_path)
    bar_len = 60 / bpm * 4
    orig_bars = int(midi.get_end_time() // bar_len)
    if orig_bars == 0:
        raise ValueError(f"Drum midi '{midi_path}' has zero bars!")
    repetitions = int(bars_needed // orig_bars) + 1
    instruments = []
    for inst in midi.instruments:
        new_inst = pretty_midi.Instrument(program=inst.program, is_drum=inst.is_drum, name=inst.name)
        for rep in range(repetitions):
            offset = rep * orig_bars * bar_len
            for note in inst.notes:
                new_note = pretty_midi.Note(
                    velocity=note.velocity,
                    pitch=note.pitch,
                    start=note.start + offset,
                    end=note.end + offset
                )
                new_inst.notes.append(new_note)
        instruments.append(new_inst)
    return instruments

# === MAIN ===
def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Select progression from csv
    progression = select_progression(CSV_CHORD_PROG, MIDI_CHORD_DIR)
    midi_file = os.path.join(MIDI_CHORD_DIR, progression['midi_filename'])
    bpm = int(progression['bpm'])
    genre = progression.get('genre', 'trap')  # fallback

    # 2. Build master midi
    master_midi = pretty_midi.PrettyMIDI()
    # Chords/bass (from full progression MIDI)
    chord_tracks, orig_bars = repeat_full_progression_midi(midi_file, SONG_BARS, bpm)
    # Only keep up to SONG_BARS bars
    bar_len = 60 / bpm * 4
    song_len = SONG_BARS * bar_len
    for inst in chord_tracks:
        inst.notes = [note for note in inst.notes if note.start < song_len]
        master_midi.instruments.append(inst)

    # 3. Drums
    drum_midi_file = pick_drum_midi(genre, MIDI_DRUM_DIR)
    if drum_midi_file:
        drum_tracks = repeat_drum_midi(drum_midi_file, SONG_BARS, bpm)
        for inst in drum_tracks:
            inst.notes = [note for note in inst.notes if note.start < song_len]
            master_midi.instruments.append(inst)

    # 4. Export
    master_midi.write(OUTPUT_FILE)
    print(f"\n✅ Song generated: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
