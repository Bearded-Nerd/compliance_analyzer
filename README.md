# YouTube Script Compliance Checker

A web application that analyzes YouTube video transcripts for compliance-sensitive words and phrases, helping content creators and marketers identify potential regulatory risks.

## Features

- Extracts transcripts from YouTube videos using video ID
- Analyzes content against a comprehensive compliance word list
- Identifies high, medium, and low-risk terms
- Simple web interface for easy use by non-technical users
- Color-coded risk levels in results

## Demo

Enter a YouTube video ID (the part after `v=` in the URL) and get instant feedback on potential compliance issues in the video's transcript.

## Installation

1. Clone the repository: 
bash
git clone https://github.com/yourusername/youtube-compliance-checker.git
cd youtube-compliance-checker

2. Install dependencies:
bash
pip install -r requirements.txt


3. Make sure you have the required files:
- `compliant_word_list.csv` - Database of compliance terms and risk levels
- `.env` file (if using environment variables)

## Usage

1. Start the Flask server:
bash
python app.py

2. Access the application at `http://localhost:5000` in your web browser.


3. Enter a YouTube video ID and click "Analyze"

## API Endpoints

### POST /analyze
Analyzes a YouTube video transcript for compliance issues.

**Parameters:**
- `video_id`: The YouTube video ID to analyze

**Response:**
json
{
"matches": [
{
"Word": "example",
"Risk Rating": "high"
}
]
}

## Dependencies

- Flask
- pandas
- youtube_transcript_api
- gunicorn (for production deployment)

## Deployment

This application can be deployed on Render.com:

1. Push your code to GitHub
2. Connect your repository to Render
3. Create a new Web Service
4. Use the following settings:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

## Deployment to Render

1. In Google Cloud Console:
   - Add your Render domain to authorized domains
   - Add `https://your-app.onrender.com/oauth2callback` to authorized redirect URIs

2. In Render.com, set these environment variables:
   - RENDER=true
   - GOOGLE_CLIENT_SECRETS=(contents of your client_secrets.json)
   - FLASK_SECRET_KEY=(your secret key)
   - GOOGLE_OAUTH_CREDENTIALS=(will be populated after first OAuth flow)

3. Deploy your application:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- YouTube Transcript API for providing transcript access
- Flask for the web framework
- Render for hosting services
