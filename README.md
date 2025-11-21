# MP3 BPM and Key Analyzer

A Python tool that scans MP3 files, detects their BPM (Beats Per Minute) and Musical Key, and writes this information to the ID3 tags.

## Features

- **BPM Detection**: Automatically detects the tempo of the track.
- **Key Detection**: Analyzes the harmonic content to detect the musical key.
- **Camelot Notation**: Converts standard keys (e.g., "C Major") to Camelot notation (e.g., "8B") which is preferred by DJs for harmonic mixing.
- **Tag Updates**: Writes the detected BPM to the `TBPM` tag and the Key/Camelot notation to the `TKEY` tag.
- **Batch Processing**: Can process a single file or an entire directory recursively.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/shlomi-r/mp3_analyzer.git
    cd mp3_analyzer
    ```

2.  **Install dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You will need `ffmpeg` installed on your system for `librosa` to process audio files.*

## Usage

Run the script by providing the path to an MP3 file or a directory containing MP3 files.

```bash
python main.py "path/to/your/music"
```

### Example

```bash
python main.py "C:\Music\Tracks"
```

Output:
```text
Found 5 MP3 files. Starting analysis...
[1/5] Processing: C:\Music\Tracks\song1.mp3
  -> Detected: 124 BPM, Key: A minor (8A)
  -> Tags updated successfully.
...
Done!
```

## Dependencies

- `librosa`: For audio analysis (BPM and Key detection).
- `mutagen`: For reading and writing ID3 tags.
- `numpy`: For numerical operations.

## License

[MIT](LICENSE)
