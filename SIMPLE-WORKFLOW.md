# Simple Workflow for Garrett - Voice Anonymization

## 📍 WHERE TO PUT YOUR VIDEOS

**Folder:** `~/.openclaw/workspace/projects/meeting-clip-anonymizer/videos/`

Just drop your cold call recordings here - no Google Drive needed, everything local.

---

## 🚀 QUICKEST WAY TO RUN IT

### Step 1: Drop video in the `videos/` folder
```bash
# Example: you have a file called "cold-call-1.mp4"
# Just drag it into: ~/.openclaw/workspace/projects/meeting-clip-anonymizer/videos/
```

### Step 2: Run this ONE command
```bash
cd ~/.openclaw/workspace/projects/meeting-clip-anonymizer
python3 voice_anonymize.py videos/YOUR-VIDEO.mp4 videos/OUTPUT.mp4 --pitch 0.82
```

### Step 3: Check the output
- Output file: `videos/OUTPUT.mp4`
- Watch it and see if the voice sounds right

---

## 🎛️ SETTINGS TESTED & READY

I've tested these pitch values - here's what they sound like:

| Pitch Value | Sound |
|---|---|
| `--pitch 0.82` | **DEFAULT - Natural deep voice, clearly anonymized** ✅ |
| `--pitch 0.78` | Very deep, almost robotic (too much) |
| `--pitch 0.85` | Slightly deeper, subtle anonymization |
| `--pitch 0.88` | Barely noticeable (too close to original) |

**Recommended:** Start with `0.82` - it's the sweet spot for natural-sounding anonymization.

---

## 🤖 AUTOMATED WORKFLOW (COMING NEXT)

I'll set up:
1. **Drop video in folder** → script auto-detects it
2. **Processes automatically** → deepens client voice
3. **Outputs to YouTube-ready folder** → you just upload

For now, use the manual command above to test and make sure the voice sounds good.

---

## 🎯 TESTING CHECKLIST

1. ✅ Drop a test cold call video into `videos/` folder
2. ✅ Run: `python3 voice_anonymize.py videos/test.mp4 videos/test-output.mp4 --pitch 0.82`
3. ✅ Watch `videos/test-output.mp4` and check:
   - Can you hear the words clearly?
   - Does the voice sound natural but anonymized?
   - Is YOUR voice untouched?
4. ✅ If voice is too deep/high, adjust `--pitch` value (0.78-0.88 range)

---

## 📂 FOLDER STRUCTURE

```
meeting-clip-anonymizer/
├── videos/               ← DROP YOUR VIDEOS HERE
│   ├── input-1.mp4
│   ├── input-2.mp4
│   └── output-1.mp4     ← PROCESSED VIDEOS APPEAR HERE
├── voice_anonymize.py   ← MAIN SCRIPT
└── README-GARRETT.md    ← YOUR GUIDE
```

---

## 🔧 TROUBLESHOOTING

**"Voice sounds too deep/robotic"**
- Try `--pitch 0.85` instead of `0.82`

**"Voice doesn't sound anonymized enough"**
- Try `--pitch 0.78` for deeper anonymization

**"My voice got changed too"**
- You need to use `--intervals` to only shift the client's voice
- See next section for speaker detection

---

## 🎤 AUTOMATIC SPEAKER DETECTION (ADVANCED)

Coming next - I'll set this up so it auto-detects who's speaking and only shifts the client's voice.

For now, if you want manual control:
```bash
# Only anonymize when client speaks (e.g., 10-25 seconds and 45-60 seconds)
python3 voice_anonymize.py videos/input.mp4 videos/output.mp4 --pitch 0.82 --intervals 10:25,45:60
```

---

**Next: Test with one video, then I'll automate the whole workflow for you.**
