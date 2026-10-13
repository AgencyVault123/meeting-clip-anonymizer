#!/usr/bin/env python3
"""
Automatic speaker detection using pyannote.audio
Identifies which speaker is which and returns intervals for anonymization
"""
import torch
import torchaudio
from pathlib import Path
import json

def detect_speakers(audio_path, num_speakers=2):
    """
    Detect speakers in audio file and return intervals for each speaker.
    
    Args:
        audio_path: Path to audio/video file
        num_speakers: Expected number of speakers (default 2 for calls)
    
    Returns:
        dict: {
            'speaker_1': [(start1, end1), (start2, end2), ...],
            'speaker_2': [(start1, end1), (start2, end2), ...]
        }
    """
    try:
        from pyannote.audio import Pipeline
        
        # Load pretrained speaker diarization pipeline
        # Note: Requires HuggingFace token for gated model
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=None  # Will use local cache or prompt for token
        )
        
        # Run diarization
        diarization = pipeline(audio_path, num_speakers=num_speakers)
        
        # Extract speaker intervals
        speaker_intervals = {}
        
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            if speaker not in speaker_intervals:
                speaker_intervals[speaker] = []
            
            speaker_intervals[speaker].append((turn.start, turn.end))
        
        return speaker_intervals
        
    except ImportError:
        # Fallback: Use simple voice activity detection
        return detect_speakers_vad(audio_path)

def detect_speakers_vad(audio_path):
    """
    Fallback speaker detection using voice activity detection.
    Assumes two speakers alternate in conversation.
    """
    try:
        import torchaudio
        from pyannote.audio import Model
        from pyannote.audio.pipelines import VoiceActivityDetection
        
        # Load VAD model
        model = Model.from_pretrained("pyannote/segmentation-3.0")
        vad_pipeline = VoiceActivityDetection(segmentation=model)
        
        # Detect speech segments
        vad = vad_pipeline(audio_path)
        
        # Split segments into two speakers (alternating assumption)
        speaker_1 = []
        speaker_2 = []
        
        for i, segment in enumerate(vad.get_timeline()):
            if i % 2 == 0:
                speaker_1.append((segment.start, segment.end))
            else:
                speaker_2.append((segment.start, segment.end))
        
        return {
            'SPEAKER_0': speaker_1,
            'SPEAKER_1': speaker_2
        }
        
    except Exception as e:
        print(f"VAD fallback failed: {e}")
        return None

def identify_primary_speaker(speaker_intervals):
    """
    Identify which speaker talks more (likely you vs client).
    Returns the speaker who talks LESS (likely the client to anonymize).
    """
    total_time = {}
    
    for speaker, intervals in speaker_intervals.items():
        total_time[speaker] = sum(end - start for start, end in intervals)
    
    # Speaker with LESS time is likely the client (you talk more as closer)
    client_speaker = min(total_time, key=total_time.get)
    
    return client_speaker, speaker_intervals[client_speaker]

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python speaker_detection.py <audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    speakers = detect_speakers(audio_file)
    
    if speakers:
        client_speaker, client_intervals = identify_primary_speaker(speakers)
        print(json.dumps({
            'client_speaker': client_speaker,
            'intervals': client_intervals
        }))
