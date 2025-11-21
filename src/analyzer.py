import librosa
import numpy as np
from .utils import get_camelot_key

def analyze_audio(file_path):
    """
    Analyzes an audio file to find its BPM and Key.
    Returns a dictionary with 'bpm', 'key', and 'camelot'.
    """
    try:
        # Load audio
        # sr=None preserves the native sampling rate, but for speed we can use a lower one like 22050
        y, sr = librosa.load(file_path, sr=22050)

        # --- BPM Detection ---
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        # tempo is usually a float or array of floats. We want a scalar.
        if isinstance(tempo, np.ndarray):
            tempo = tempo[0]
        
        bpm = round(tempo)

        # --- Key Detection ---
        # Harmonic component is better for key detection
        y_harmonic, _ = librosa.effects.hpss(y)
        chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
        
        # Sum chroma over time to get a global chroma vector
        chroma_vals = np.sum(chroma, axis=1)
        
        # Krumhansl-Schmuckler key profiles
        maj_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
        min_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
        
        # Correlate chroma with profiles for all 12 pitches
        maj_corrs = []
        min_corrs = []
        
        for i in range(12):
            # Rotate profile to match the current root note
            maj_rotated = np.roll(maj_profile, i)
            min_rotated = np.roll(min_profile, i)
            
            maj_corrs.append(np.corrcoef(chroma_vals, maj_rotated)[0, 1])
            min_corrs.append(np.corrcoef(chroma_vals, min_rotated)[0, 1])
            
        # Find the best match
        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        max_maj_idx = np.argmax(maj_corrs)
        max_min_idx = np.argmax(min_corrs)
        
        if maj_corrs[max_maj_idx] > min_corrs[max_min_idx]:
            key = f"{key_names[max_maj_idx]} major"
        else:
            key = f"{key_names[max_min_idx]} minor"
            
        camelot = get_camelot_key(key)
        
        return {
            'bpm': bpm,
            'key': key,
            'camelot': camelot
        }

    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return None
