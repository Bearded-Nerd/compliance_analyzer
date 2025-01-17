from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scriptFetcher import analyze_transcript_compliance
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Use environment variable for secret key
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-please-change')

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        video_id = request.form.get('video_id')
        if not video_id:
            return jsonify({'error': 'No video ID provided'}), 400
            
        try:
            transcript_text, results, word_positions = analyze_transcript_compliance(video_id)
        except Exception as e:
            if "timed out" in str(e).lower():
                return jsonify({'error': 'Analysis timed out. Please try again.'}), 504
            raise
            
        if not transcript_text:
            return jsonify({'error': 'Failed to fetch transcript. The video might be unavailable or have no captions.'}), 404
            
        if results.empty:
            return jsonify({
                'message': 'No compliance issues found',
                'transcript': transcript_text,
                'positions': word_positions
            })
        
        return jsonify({
            'matches': results.to_dict('records'),
            'transcript': transcript_text,
            'positions': word_positions
        })
    except Exception as e:
        logger.error(f"Error in analyze route: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Add health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG', 'False') == 'True') 
