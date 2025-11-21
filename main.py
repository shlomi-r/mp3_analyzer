import os
import argparse
import sys
from src.analyzer import analyze_audio
from src.tagger import update_tags

def main():
    parser = argparse.ArgumentParser(description="Scan MP3 files and update BPM and Key tags.")
    parser.add_argument("path", help="Path to a file or directory to scan")
    args = parser.parse_args()
    
    target_path = args.path
    
    if not os.path.exists(target_path):
        print(f"Error: Path '{target_path}' does not exist.")
        sys.exit(1)
        
    files_to_process = []
    
    if os.path.isfile(target_path):
        if target_path.lower().endswith('.mp3'):
            files_to_process.append(target_path)
    else:
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if file.lower().endswith('.mp3'):
                    files_to_process.append(os.path.join(root, file))
                    
    if not files_to_process:
        print("No MP3 files found.")
        sys.exit(0)
        
    print(f"Found {len(files_to_process)} MP3 files. Starting analysis...")
    
    for i, file_path in enumerate(files_to_process):
        print(f"[{i+1}/{len(files_to_process)}] Processing: {file_path}")
        
        result = analyze_audio(file_path)
        
        if result:
            bpm = result['bpm']
            camelot = result['camelot']
            musical_key = result['key']
            
            print(f"  -> Detected: {bpm} BPM, Key: {musical_key} ({camelot})")
            
            # We write the Camelot key to the TKEY tag as it's often more useful for DJs
            # You could also write "{musical_key} - {camelot}" if preferred
            if update_tags(file_path, bpm, camelot):
                print("  -> Tags updated successfully.")
            else:
                print("  -> Failed to update tags.")
        else:
            print("  -> Analysis failed.")
            
    print("\nDone!")

if __name__ == "__main__":
    main()
