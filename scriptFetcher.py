import pandas as pd
from yt_dlp import YoutubeDL
import logging

logger = logging.getLogger(__name__)

def get_transcript(video_url: str) -> str:
    """Get transcript using yt-dlp"""
    try:
        ydl_opts = {
            'writeautomaticsub': True,
            'skip_download': True,
            'quiet': True,
            # Add these options to help avoid the bot detection
            'no_warnings': True,
            'ignoreerrors': True,
            # Add cookies if needed
            'cookiefile': 'cookies.txt',
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            url = f"{video_url}"
            info = ydl.extract_info(url, download=False)
            
            if info and 'automatic_captions' in info:
                # Try to get English captions
                captions = info['automatic_captions'].get('en', [])
                if not captions:
                    # Fallback to any available captions
                    captions = next(iter(info['automatic_captions'].values()), [])
                    
                return ' '.join(caption['text'] for caption in captions if 'text' in caption)
                
    except Exception as e:
        logger.error(f"Error getting transcript: {str(e)}")
    return ""

def analyze_transcript_compliance(video_url: str) -> tuple:
    """Analyzes video transcript for compliance matches"""
    try:
        script_text = get_transcript(video_url)
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
