#!/bin/bash
# Simple script to process a cold call video
# Usage: ./process-video.sh input.mp4 output.mp4

INPUT="$1"
OUTPUT="$2"
PITCH="${3:-0.82}"  # Default pitch 0.82 if not specified

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: ./process-video.sh input.mp4 output.mp4 [pitch]"
    echo ""
    echo "Example: ./process-video.sh videos/cold-call.mp4 videos/anonymized.mp4"
    echo "         ./process-video.sh videos/cold-call.mp4 videos/anonymized.mp4 0.85"
    exit 1
fi

echo "🎬 Processing video..."
echo "   Input:  $INPUT"
echo "   Output: $OUTPUT"
echo "   Pitch:  $PITCH (lower = deeper voice)"
echo ""

python3 voice_anonymize.py "$INPUT" "$OUTPUT" --pitch "$PITCH"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ DONE! Your anonymized video is ready:"
    echo "   $OUTPUT"
    echo ""
    echo "📺 Next steps:"
    echo "   1. Watch the output to check if the voice sounds good"
    echo "   2. If too deep, run again with higher pitch (e.g., 0.85)"
    echo "   3. If not deep enough, run again with lower pitch (e.g., 0.78)"
    echo "   4. Upload to YouTube when happy with the result"
else
    echo ""
    echo "❌ Error processing video. Check the error message above."
fi
