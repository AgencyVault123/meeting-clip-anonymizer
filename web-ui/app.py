#!/usr/bin/env python3
"""
Simple web UI for voice anonymization - drag and drop videos, download results
"""
from flask import Flask, render_template, request, send_file, jsonify
import os
import subprocess
import uuid
from pathlib import Path
import tempfile
import shutil
import json

app = Flask(__name__)

# Create upload and output directories
UPLOAD_FOLDER = Path(tempfile.gettempdir()) / 'voice-anon-uploads'
OUTPUT_FOLDER = Path(tempfile.gettempdir()) / 'voice-anon-outputs'
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Max file size: 500MB
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Get pitch setting (default 0.82)
        pitch = float(request.form.get('pitch', 0.82))
        auto_detect = request.form.get('auto_detect', 'true').lower() == 'true'
        
        # Generate unique ID for this job
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        input_path = UPLOAD_FOLDER / f"{job_id}_input.mp4"
        output_path = OUTPUT_FOLDER / f"{job_id}_output.mp4"
        
        file.save(input_path)
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    
    try:
        # Check if ffmpeg is available
        ffmpeg_check = subprocess.run(['which', 'ffmpeg'], capture_output=True)
        if ffmpeg_check.returncode != 0:
            return jsonify({'error': 'ffmpeg not found on server - contact admin'}), 500
        
        # Get the path to voice_anonymize.py (parent directory)
        script_path = Path(__file__).parent.parent / 'voice_anonymize.py'
        speaker_detect_script = Path(__file__).parent / 'simple_speaker_detect.py'
        
        if not script_path.exists():
            return jsonify({'error': 'Voice anonymization script not found'}), 500
        
        # Build command args
        cmd_args = [
            'python3',
            str(script_path),
            str(input_path),
            str(output_path),
            '--pitch', str(pitch)
        ]
        
        # Auto-detect speaker intervals if enabled
        if auto_detect:
            try:
                # Run speaker detection
                result = subprocess.run([
                    'python3',
                    str(speaker_detect_script),
                    str(input_path)
                ], capture_output=True, text=True, check=True)
                
                detection_data = json.loads(result.stdout)
                intervals = detection_data.get('intervals', [])
                
                if intervals:
                    # Format intervals for voice_anonymize.py
                    interval_str = ','.join(f"{start}:{end}" for start, end in intervals)
                    cmd_args.extend(['--intervals', interval_str])
            except Exception as e:
                # Fall back to anonymizing entire video if detection fails
                print(f"Speaker detection failed, anonymizing entire video: {e}")
        
        # Run voice anonymization
        subprocess.run(cmd_args, check=True, capture_output=True, text=True)
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'download_url': f'/download/{job_id}'
        })
    
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': f'Processing failed: {e.stderr}'
        }), 500
    except Exception as e:
        return jsonify({
            'error': f'Error: {str(e)}'
        }), 500

@app.route('/download/<job_id>')
def download_file(job_id):
    output_path = OUTPUT_FOLDER / f"{job_id}_output.mp4"
    
    if not output_path.exists():
        return "File not found", 404
    
    return send_file(
        output_path,
        as_attachment=True,
        download_name='anonymized_video.mp4',
        mimetype='video/mp4'
    )

@app.route('/cleanup/<job_id>', methods=['POST'])
def cleanup(job_id):
    """Clean up files after download"""
    input_path = UPLOAD_FOLDER / f"{job_id}_input.mp4"
    output_path = OUTPUT_FOLDER / f"{job_id}_output.mp4"
    
    input_path.unlink(missing_ok=True)
    output_path.unlink(missing_ok=True)
    
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
