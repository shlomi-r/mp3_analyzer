def get_camelot_key(key_name):
    """
    Maps a standard musical key (e.g., 'C major', 'A minor') to Camelot Wheel notation.
    """
    camelot_map = {
        'B major': '1B', 'G# minor': '1A', 'Ab minor': '1A',
        'F# major': '2B', 'Gb major': '2B', 'D# minor': '2A', 'Eb minor': '2A',
        'Db major': '3B', 'C# major': '3B', 'Bb minor': '3A', 'A# minor': '3A',
        'Ab major': '4B', 'G# major': '4B', 'F minor': '4A',
        'Eb major': '5B', 'D# major': '5B', 'C minor': '5A',
        'Bb major': '6B', 'A# major': '6B', 'G minor': '6A',
        'F major': '7B', 'D minor': '7A',
        'C major': '8B', 'A minor': '8A',
        'G major': '9B', 'E minor': '9A',
        'D major': '10B', 'B minor': '10A',
        'A major': '11B', 'F# minor': '11A', 'Gb minor': '11A',
        'E major': '12B', 'C# minor': '12A', 'Db minor': '12A'
    }
    
    # Normalize input
    key_name = key_name.strip()
    # Handle some variations if necessary, but librosa/our logic usually outputs standard names
    
    return camelot_map.get(key_name, key_name) # Return original if not found
