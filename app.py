from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scriptFetcher import analyze_transcript_compliance
import logging
from os import environ

# Basic logging and app setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        transcript_text = request.form.get('transcript')
        if not transcript_text:
            return jsonify({'error': 'No transcript provided'}), 400
            
        transcript_text, results, word_positions = analyze_transcript_compliance(transcript_text)
        
        return jsonify({
            'matches': results.to_dict('records') if not results.empty else [],
            'transcript': transcript_text,
            'positions': word_positions
        })
    except Exception as e:
        logger.error(f"Error in analyze route: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
