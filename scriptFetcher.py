import json
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
from youtube_dl import YoutubeDL
import logging

logger = logging.getLogger(__name__)

def get_auto_transcript(video_id: str) -> str:
    """
    Attempts to get auto-generated transcript using youtube-dl as fallback
    """
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
                text_parts = []
                for caption in captions:
                    if 'text' in caption:
                        text_parts.append(caption['text'])
                return ' '.join(text_parts)
    except Exception as e:
        logger.error(f"Error getting auto transcript: {str(e)}")
    return ""

def analyze_transcript_compliance(video_id: str) -> tuple:
    """
    Analyzes a video transcript and returns both full text and compliance matches.
    
    Returns:
        tuple: (full_text, matches_df, word_positions)
    """
    try:
        # First try with youtube_transcript_api
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            script_text = ' '.join(entry['text'] for entry in transcript)
        except Exception as e:
            logger.warning(f"Could not get transcript with primary method: {str(e)}")
            # Fallback to youtube-dl method
            script_text = get_auto_transcript(video_id)
            if not script_text:
                raise Exception("Could not retrieve transcript with any method")
        
        # Read the compliant words list CSV file
        compliant_words_df = pd.read_csv('compliant_word_list.csv')
        word_list = compliant_words_df[['Name', 'Risk Rating']].dropna()
        
        # Convert script to lowercase for case-insensitive matching
        script_text_lower = script_text.lower()
        
        # Find matches and their positions
        matches = []
        word_positions = {}  # Store word positions for highlighting
        
        for _, row in word_list.iterrows():
            word = row['Name'].lower()
            if word in script_text_lower:
                matches.append({
                    'Word': row['Name'],
                    'Risk Rating': row['Risk Rating']
                })
                # Find all occurrences of the word
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
        
        matches_df = pd.DataFrame(matches)
        return script_text, matches_df if not matches_df.empty else pd.DataFrame(columns=['Word', 'Risk Rating']), word_positions
        
    except Exception as e:
        logger.error(f"Error analyzing transcript: {str(e)}")
        return "", pd.DataFrame(columns=['Word', 'Risk Rating']), {}
