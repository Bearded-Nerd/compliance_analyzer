import pandas as pd
import logging

logger = logging.getLogger(__name__)

def analyze_transcript_compliance(transcript_text):
    """Analyze transcript text for compliance issues"""
    try:
        # Load compliance word list
        compliance_df = pd.read_csv('compliant_word_list.csv')
        
        # Convert transcript to lowercase for case-insensitive matching
        transcript_lower = transcript_text.lower()
        
        # Find matches and their positions
        matches = []
        word_positions = {}
        
        for _, row in compliance_df.iterrows():
            word = row['Word'].lower()
            risk = row['Risk Rating']
            
            # Find all occurrences of the word
            start = 0
            while True:
                pos = transcript_lower.find(word, start)
                if pos == -1:
                    break
                    
                matches.append({
                    'Word': row['Word'],
                    'Risk Rating': risk,
                    'Position': pos
                })
                
                # Store position for highlighting
                word_positions[pos] = {
                    'word': row['Word'],
                    'length': len(word),
                    'risk': risk
                }
                
                start = pos + 1
        
        # Convert matches to DataFrame for consistent output
        results = pd.DataFrame(matches)
        
        return transcript_text, results, word_positions
        
    except Exception as e:
        logger.error(f"Error analyzing transcript: {str(e)}")
        raise
