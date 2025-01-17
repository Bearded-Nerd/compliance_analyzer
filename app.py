from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scriptFetcher import analyze_transcript_compliance
import os
import logging
from os import environ

# Basic logging and app setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Add secret key from environment variable
app.secret_key = environ.get('FLASK_SECRET_KEY', 'bc413485091516d4a7fd5dcba443ad75')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        video_id = request.form.get('video_id')
        if not video_id:
            return jsonify({'error': 'No video ID provided'}), 400
            
        transcript_text, results, word_positions = analyze_transcript_compliance(video_id)
        
        if not transcript_text:
            return jsonify({'error': 'Failed to fetch transcript'}), 404
            
        return jsonify({
            'matches': results.to_dict('records') if not results.empty else [],
            'transcript': transcript_text,
            'positions': word_positions
        })
    except Exception as e:
        logger.error(f"Error in analyze route: {str(e)}")
        return jsonify({'error': str(e)}), 500
