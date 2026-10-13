# Meeting Clip Anonymizer - Setup for Garrett's Cold Call Videos

## What This Does
Automatically anonymizes cold call videos for YouTube:
- **Detects speakers automatically** (you vs client)
- **Deepens client's voice** with natural pitch shift (not AI voice)
- **Keeps your voice untouched**
- **One-command processing**

## Quick Start

### 1. Install Dependencies
```bash
cd ~/.openclaw/workspace/projects/meeting-clip-anonymizer
pip install -r requirements.txt

# Install ffmpeg if not already installed:
brew install ffmpeg
```

### 2. Basic Usage (Just Voice Anonymization)
```bash
# Simplest: anonymize entire video (deepens all voices)
python voice_anonymize.py input.mp4 output.mp4 --pitch 0.82

# Better: only anonymize client's speaking intervals
# (you'll need to identify when they're speaking - see below)
python voice_anonymize.py input.mp4 output.mp4 --intervals 0:9,41:48 --pitch 0.82
```

### 3. How to Get Client's Speaking Intervals

**Option A: Manual (easiest to start)**
1. Watch your video
2. Note timestamps when client speaks (format: start:end in seconds)
3. Use `--intervals` flag

**Option B: Automatic Speaker Detection (requires setup)**
- Use Zoom/Meet speaker view recording
- The tool detects when the client's name label appears on screen
- See `pipeline/classify_speakers.py` for details

## Parameters

### Pitch Values
- `--pitch 0.82` = default deep anonymization (recommended)
- `--pitch 0.80-0.86` = range for natural male voice anonymization
- Lower = deeper voice

### Bleep PII (names, amounts)
```bash
python voice_anonymize.py input.mp4 output.mp4 --intervals 0:9,41:48 --pitch 0.82 \
       --bleep 12.3:12.8,40.1:41.0
```

## Example Workflow

```bash
# 1. Put your cold call recording in this folder
# 2. Run anonymization
python voice_anonymize.py my-cold-call.mp4 anonymized-output.mp4 --pitch 0.82 --intervals 10:25,45:60

# 3. Upload anonymized-output.mp4 to YouTube
```

## Config for Full Pipeline (Optional)

Edit `config.json` for advanced features:
- Automatic silence removal
- Hide client's face with branded card
- Add captions/overlays
- Background music

See original README.md for full pipeline details.

## Files You Need
- `voice_anonymize.py` - Main script (standalone, works without the rest)
- `requirements.txt` - Python dependencies
- `config.json` - Configuration (copy from config.example.json)

## Troubleshooting

**"ffmpeg not found"**
```bash
brew install ffmpeg
```

**"Module not found"**
```bash
pip install -r requirements.txt
```

**Need help identifying intervals?**
- Use a video player with timestamp display
- Pause when client starts/stops speaking
- Write down timestamps

## Next Steps

Once you've tested basic anonymization:
1. Set up automatic speaker detection (pipeline/classify_speakers.py)
2. Configure branded cards for face hiding
3. Add silence removal for tighter edits
4. Set up cloud rendering for hands-off processing

---

**Quick Reference:**
```bash
# Basic anonymization (whole video)
python voice_anonymize.py input.mp4 output.mp4 --pitch 0.82

# With intervals (client speaks 10-25sec and 45-60sec)
python voice_anonymize.py input.mp4 output.mp4 --pitch 0.82 --intervals 10:25,45:60

# With PII bleeping (bleep 12.3-12.8sec)
python voice_anonymize.py input.mp4 output.mp4 --pitch 0.82 --intervals 10:25,45:60 --bleep 12.3:12.8
```
