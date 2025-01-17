import pandas as pd
from youtube_dl import YoutubeDL
import logging

logger = logging.getLogger(__name__)

def get_transcript(video_id: str) -> str:
    """Get transcript using youtube-dl"""
    try:
        ydl_opts = {
            'writeautomaticsub': True,
            'skip_download': True,
            'quiet': True
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            if 'automatic_captions' in info and 'en' in info['automatic_captions']:
                captions = info['automatic_captions']['en']
                return ' '.join(caption['text'] for caption in captions if 'text' in caption)
    except Exception as e:
        logger.error(f"Error getting transcript: {str(e)}")
    return ""

def analyze_transcript_compliance(video_id: str) -> tuple:
    """Analyzes video transcript for compliance matches"""
    try:
        script_text = get_transcript(video_id)
        if not script_text:
            return "", pd.DataFrame(), {}
            
        # Read and process compliance word list
        word_list = pd.read_csv('compliant_word_list.csv')[['Name', 'Risk Rating']].dropna()
        
        # Find matches and their positions
        matches = []
        word_positions = {}
        script_text_lower = script_text.lower()
        
        for _, row in word_list.iterrows():
            word = row['Name'].lower()
            if word in script_text_lower:
                matches.append({
                    'Word': row['Name'],
                    'Risk Rating': row['Risk Rating']
                })
                
                # Find all word positions
                start = 0
                while True:
                    pos = script_text_lower.find(word, start)
                    if pos == -1:
                        break
                    word_positions[pos] = {
                        'word': row['Name'],
                        'risk': row['Risk Rating'],
                        'length': len(word)
                    }
                    start = pos + 1
        
        return script_text, pd.DataFrame(matches), word_positions
        
    except Exception as e:
        logger.error(f"Error analyzing transcript: {str(e)}")
        raise
