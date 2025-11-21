from mutagen.id3 import ID3, TBPM, TKEY, ID3NoHeaderError

def update_tags(file_path, bpm, key):
    """
    Updates the ID3 tags of an MP3 file with BPM and Key.
    """
    try:
        try:
            tags = ID3(file_path)
        except ID3NoHeaderError:
            tags = ID3()
        
        # Update BPM
        # TBPM frame stores BPM as a string
        tags.add(TBPM(encoding=3, text=str(bpm)))
        
        # Update Key
        # TKEY frame stores the initial key
        tags.add(TKEY(encoding=3, text=key))
        
        tags.save(file_path)
        return True
    except Exception as e:
        print(f"Error tagging {file_path}: {e}")
        return False
