import sys
import os
import numpy as np
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'mp3_analyzer'))

from src.analyzer import analyze_audio
from src.tagger import update_tags

def test_analysis_logic():
    print("Testing Analysis Logic...")
    
    # Create a synthetic signal: A440 sine wave (should be A major-ish or just A)
    sr = 22050
    t = np.linspace(0, 5, int(5 * sr))
    y = 0.5 * np.sin(2 * np.pi * 440 * t)
    
    # Mock librosa.load to return this signal
    with patch('librosa.load', return_value=(y, sr)):
        # We also need to mock beat_track to return a dummy BPM because a pure sine wave has no beat
        with patch('librosa.beat.beat_track', return_value=(120.0, None)):
             # Mock chroma_cqt to return something that looks like A major
             # A major: A, B, C#, D, E, F#, G#
             # Indices: 9, 11, 1, 2, 4, 6, 8
             # We'll just mock the output of analyze_audio's internal logic by mocking the function itself?
             # No, let's try to let it run. But hpss might fail on pure sine.
             
             # Let's just mock the whole analyze_audio for the integration test, 
             # BUT to test the logic we should try to feed it data.
             # Given the complexity of mocking audio math, I will verify the *flow* mostly.
             pass

    # Let's test the analyze_audio function with a mocked librosa
    with patch('librosa.load') as mock_load:
        with patch('librosa.onset.onset_strength') as mock_onset:
            with patch('librosa.beat.beat_track') as mock_beat:
                with patch('librosa.effects.hpss') as mock_hpss:
                    with patch('librosa.feature.chroma_cqt') as mock_chroma:
                        
                        # Setup mocks
                        mock_load.return_value = (np.zeros(22050*5), 22050)
                        mock_beat.return_value = (128.0, None)
                        mock_hpss.return_value = (np.zeros(22050*5), None)
                        # Mock chroma: 12 bins, 100 frames. 
                        # Make bin 0 (C) high to simulate C Major
                        chroma_data = np.zeros((12, 100))
                        chroma_data[0, :] = 1.0 # C
                        chroma_data[4, :] = 1.0 # E
                        chroma_data[7, :] = 1.0 # G
                        mock_chroma.return_value = chroma_data
                        
                        result = analyze_audio("dummy.mp3")
                        
                        print(f"Analysis Result: {result}")
                        
                        if result['bpm'] == 128 and result['camelot'] == '8B': # C Major is 8B
                            print("SUCCESS: Analysis logic verified (Mocked).")
                        else:
                            print(f"FAILURE: Analysis logic unexpected result. Key: {result['key']}, Camelot: {result['camelot']}")

def test_tagging_logic():
    print("\nTesting Tagging Logic...")
    
    with patch('src.tagger.ID3') as MockID3:
        mock_tags = MagicMock()
        MockID3.return_value = mock_tags
        
        update_tags("dummy.mp3", 128, "8B")
        
        # Verify save was called
        mock_tags.save.assert_called_with("dummy.mp3")
        print("SUCCESS: Tagging logic verified (Mocked).")

if __name__ == "__main__":
    test_analysis_logic()
    test_tagging_logic()
