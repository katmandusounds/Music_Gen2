# 🎛️ One-Shot & Loop Song Generator

*A smart, modular Python audio engine that auto-generates structured songs using loops, one-shots, and MIDI—guided by musical key, chord progression, genre, and mood metadata. Designed for next-generation music production, creative coding, and AI audio workflows.*

---

## 🧠 Overview

This project creates complete, musically correct songs by algorithmically arranging modular audio and MIDI building blocks, all driven by rich metadata and customizable palettes.

- **Randomly selects** musical key, BPM, and chord progression
- **Filters** audio/MIDI by mood, genre, theme, and instrument
- **Loads and arranges** loops, one-shots, and MIDI from a modular folder structure
- **Builds** a full 112-bar song structure with intro, hooks, verses, and outro
- **Exports** finished tracks as MIDI (and can be extended to .wav)

---

## 🚀 Features

- **Musically correct**: All melodies, chords, and basslines match the selected key and progression
- **Flexible arrangement**: Supports both loops and one-shots; auto-generates main and sub melodies using user-defined note palettes
- **Genre/mood aware**: Uses metadata for intelligent genre, mood, and theme selection
- **Extensible**: Designed for adding AI/machine learning, user feedback, or procedural generation
- **Export**: Outputs full-length `.mid` files, ready for DAWs or further audio rendering

---

## 📂 Folder Structure

<pre>
project/
├── oneshots/
│   └── drums/ (kicks, snares, hihats, perc, etc.)
├── loops/
│   └── chords, bass, melody, vocals, drums/
├── midi/
│   ├── chords/
│   └── drums/
├── metadata/
│   ├── oneshot_metadata.csv
│   ├── loops_metadata.csv
│   └── chord_progressions.csv
├── palettes/
│   └── mood_scales.json
├── output/
│   └── generated_song_full.mid
├── generator.py
└── README.md
</pre>

---

## 🛠️ Technologies Used

- **Python** (main engine)
- `pretty_midi` for MIDI processing and generation
- `pandas` for data/metadata handling
- `json` for palettes and scales
- *Ready to extend with* `pydub` or `librosa` for audio export

---

## 🎼 Song Structure (112 Bars)

| Section   | Bars   | Components                           |
|-----------|--------|--------------------------------------|
| Intro A   | 0–8    | chords + sub melody                  |
| Intro B   | 8–16   | add bass + snare + hihat             |
| Hook A    | 16–24  | bass + chords + main melody + drums  |
| Hook B    | 24–32  | add sub melody + vocal               |
| Verse A   | 32–40  | bass + chords + basic drums          |
| ...       | ...    | ...                                  |
| Outro     | 96–112 | fade out                             |

---


## 📝 How to Run

1. **Install dependencies:**

    ```bash
    pip install pretty_midi pandas
    ```

2. **Clone this repo and add your MIDI/oneshot/loop files**  
   *(See folder structure above.)*

3. **Run the generator:**

    ```bash
    python3 generator.py
    ```

4. **Output:**
    - Your generated `.mid` will be in `/output/generated_song_full.mid`
    - *(To convert to audio: import into a DAW, or extend with audio rendering tools)*

---

## 📋 Example Metadata (`chord_progressions.csv`)

| name                  | key    | bpm | progression |
|-----------------------|--------|-----|-------------|
| Aminor_Cmaj_Amin_1    | Aminor | 120 | 6,5,4,1     |
| CMajor_Cmaj_Cmaj_2    | CMajor | 120 | 1,4,5,1     |
| ...                   | ...    | ... | ...         |

---

## 💡 Project Motivation

I built this engine to explore the intersection of **music theory, generative coding, and procedural audio**—showcasing both technical and creative skills.  
The project demonstrates:
- Complex Python scripting and data handling
- MIDI/music theory knowledge
- System design for modular, metadata-driven workflows

---

## 🎧 Demo

> **[Link to example MIDI output]**  
*(Add a .mid or .mp3 export here if you wish!)*

---

## 📚 Further Development

- Add AI/machine learning for new loop/melody creation
- Render directly to audio using pydub/librosa and mapped one-shots
- Build a web interface (Gradio/Tkinter) for live song generation

---

## 👤 Author

**Rabin Bhatta**  
[LinkedIn](#) \| [GitHub](#)  
*Open to collaboration & further research!*

---

## 🪪 License

MIT License (c) 2024 Rabin Bhatta

---

> **Ready to revolutionize creative music workflows.**

