import json
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
from youtube_dl import YoutubeDL
import logging
from functools import lru_cache
import concurrent.futures
import threading

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

# Add caching to transcript fetching
@lru_cache(maxsize=100)
def get_cached_transcript(video_id: str) -> str:
    return get_auto_transcript(video_id)

def analyze_transcript_compliance(video_id: str) -> tuple:
    """
    Analyzes a video transcript and returns both full text and compliance matches.
    
    Returns:
        tuple: (full_text, matches_df, word_positions)
    """
    try:
        # Use ThreadPoolExecutor with timeout
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(get_cached_transcript, video_id)
            try:
                script_text = future.result(timeout=20)  # 20 second timeout
            except concurrent.futures.TimeoutError:
                raise Exception("Transcript fetching timed out")
            
        if not script_text:
            raise Exception("Could not retrieve transcript")
            
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
        logger.error(f"Error in analyze_transcript_compliance: {str(e)}")
        raise
