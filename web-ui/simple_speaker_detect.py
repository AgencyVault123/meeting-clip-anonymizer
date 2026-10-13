#!/usr/bin/env python3
"""
Simple speaker detection using audio energy and silence detection.
Assumes 2 speakers alternating - identifies who talks more (you) vs less (client).
"""
import subprocess
import json
import sys
from pathlib import Path

def detect_speakers_simple(video_path):
    """
    Simple speaker detection:
    1. Extract audio
    2. Detect speech segments using ffmpeg silencedetect
    3. Split into 2 speakers (alternating)
    4. Return intervals for speaker who talks LESS (client to anonymize)
    """
    # Use ffmpeg to detect silence and get speech segments
    cmd = [
        'ffmpeg', '-i', str(video_path),
        '-af', 'silencedetect=noise=-30dB:d=0.5',
        '-f', 'null', '-'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.STDOUT)
    output = result.stdout
    
    # Parse silence detection output
    speech_segments = []
    silence_end = 0
    
    for line in output.split('\n'):
        if 'silencedetect' in line:
            if 'silence_end' in line:
                # Extract silence end time
                parts = line.split('silence_end:')
                if len(parts) > 1:
                    time_str = parts[1].split('|')[0].strip()
                    try:
                        silence_end = float(time_str)
                    except:
                        pass
            elif 'silence_start' in line:
                # Extract silence start time
                parts = line.split('silence_start:')
                if len(parts) > 1:
                    time_str = parts[1].strip()
                    try:
                        silence_start = float(time_str)
                        if silence_end < silence_start:
                            speech_segments.append((silence_end, silence_start))
                    except:
                        pass
    
    if not speech_segments:
        # No silence detected - return empty (will anonymize whole video as fallback)
        return []
    
    # Alternate assignment: odd segments = speaker 1, even = speaker 2
    speaker_1 = []
    speaker_2 = []
    
    for i, segment in enumerate(speech_segments):
        if i % 2 == 0:
            speaker_1.append(segment)
        else:
            speaker_2.append(segment)
    
    # Calculate total speaking time for each
    time_1 = sum(end - start for start, end in speaker_1)
    time_2 = sum(end - start for start, end in speaker_2)
    
    # Return intervals for speaker who talks LESS (likely the client)
    if time_1 < time_2:
        return speaker_1
    else:
        return speaker_2

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({'intervals': []}))
        sys.exit(0)
    
    video_path = sys.argv[1]
    intervals = detect_speakers_simple(video_path)
    
    print(json.dumps({
        'intervals': intervals
    }))
