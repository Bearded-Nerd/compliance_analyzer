# Script Compliance Checker

A web application that analyzes text transcripts for compliance-sensitive words and phrases, helping content creators and marketers identify potential regulatory risks.

## Features

- Analyzes pasted transcripts against a comprehensive compliance word list
- Identifies high, medium, and low-risk terms
- Simple web interface for easy use by non-technical users
- Color-coded risk levels in results

## Demo

Paste your transcript text and get instant feedback on potential compliance issues.

## Installation

1. Clone the repository: 
bash
git clone https://github.com/yourusername/script-compliance-checker.git
cd script-compliance-checker

2. Install dependencies:
bash
pip install -r requirements.txt



3. Make sure you have the required file:
- `compliant_word_list.csv` - Database of compliance terms and risk levels

## Usage

1. Start the Flask server:
bash
python app.py


2. Access the application at `http://localhost:5000` in your web browser.

3. Paste your transcript and click "Analyze"

## API Endpoints

### POST /analyze
Analyzes a transcript for compliance issues.

**Parameters:**
- `transcript`: The text to analyze

**Response:**
json
{
"matches": [
{
"Word": "example",
"Risk Rating": "high"
}
],
"transcript": "original text",
"positions": {}
}


## Dependencies

- Flask
- pandas
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask for the web framework
- Render for hosting services
