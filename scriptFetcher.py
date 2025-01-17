import json
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd

def fetch_transcript(video_id: str) -> None:
    """
    Fetches transcript for a YouTube video and saves it as JSON.
    
    Args:
        video_id (str): YouTube video ID
    """
    try:
        # Get transcript for the specified video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Create output filename using video ID
        output_file = f"transcript_{video_id}.json"
        
        # Write transcript to JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Error fetching transcript: {str(e)}")

# Example usage:
# fetch_transcript("pxiP-HJLCx0")

def analyze_transcript_compliance(video_id: str) -> tuple:
    """
    Analyzes a video transcript and returns both full text and compliance matches.
    
    Returns:
        tuple: (full_text, matches_df, word_positions)
    """
    try:
        # Get transcript for the specified video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all text from transcript
        script_text = ' '.join(entry['text'] for entry in transcript)
        
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
        print(f"Error analyzing transcript: {str(e)}")
        return "", pd.DataFrame(columns=['Word', 'Risk Rating']), {}
