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

def analyze_transcript_compliance(video_id: str) -> pd.DataFrame:
    """
    Analyzes a video transcript for compliance words and returns matches with risk levels.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        pd.DataFrame: DataFrame containing matched words and their risk levels
    """
    try:
        # Get transcript for the specified video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all text from transcript
        script_text = ' '.join(entry['text'] for entry in transcript)
        
        # Read the compliant words list CSV file
        compliant_words_df = pd.read_csv('Compliant Word List.csv')
        word_list = compliant_words_df[['Name', 'Risk Rating']].dropna()
        
        # Convert script to lowercase for case-insensitive matching
        script_text_lower = script_text.lower()
        
        # Find matches
        matches = []
        for _, row in word_list.iterrows():
            word = row['Name'].lower()
            if word in script_text_lower:
                matches.append({
                    'Word': row['Name'],
                    'Risk Rating': row['Risk Rating']
                })
        
        # Create DataFrame from matches
        matches_df = pd.DataFrame(matches)
        return matches_df if not matches_df.empty else pd.DataFrame(columns=['Word', 'Risk Rating'])
        
    except Exception as e:
        print(f"Error analyzing transcript: {str(e)}")
        return pd.DataFrame(columns=['Word', 'Risk Rating'])
