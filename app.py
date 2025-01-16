from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scriptFetcher import analyze_transcript_compliance
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-please-change')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_id = request.form.get('video_id')
    if not video_id:
        return jsonify({'error': 'No video ID provided'})
    
    results = analyze_transcript_compliance(video_id)
    
    if results.empty:
        return jsonify({'message': 'No compliance issues found'})
    
    return jsonify({
        'matches': results.to_dict('records')
    })

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', 'True') == 'True') 
