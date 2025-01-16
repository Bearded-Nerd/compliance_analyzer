from flask import Flask, render_template, request, jsonify
from scriptFetcher import analyze_transcript_compliance

app = Flask(__name__)

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
    app.run(debug=True) 