import pandas as pd
import logging

logger = logging.getLogger(__name__)

def analyze_transcript_compliance(transcript_text):
    """Analyze transcript text for compliance issues"""
    try:
        # Load compliance word list
        compliance_df = pd.read_csv('compliant_word_list.csv')
        
        # Initialize empty list for matches
        matches = []
        
        # Convert transcript to lowercase for case-insensitive matching
        transcript_lower = transcript_text.lower()
        
        # Iterate through compliance words
        for index, row in compliance_df.iterrows():
            try:
                word = str(row['Word']).lower()  # Ensure word is string and lowercase
                risk = str(row['Risk Rating'])   # Ensure risk is string
                
                # Check if word appears in transcript
                if word in transcript_lower:
                    matches.append({
                        'Word': str(row['Word']),  # Use original case from CSV
                        'Risk Rating': risk
                    })
            except KeyError as e:
                logger.error(f"Column missing in CSV: {e}")
                continue
            except Exception as e:
                logger.error(f"Error processing word: {e}")
                continue
        
        # Create DataFrame from matches
        results = pd.DataFrame(matches) if matches else pd.DataFrame(columns=['Word', 'Risk_Rating'])
        
        return transcript_text, results, {}  # Empty dict for positions as we're not using them
        
    except Exception as e:
        logger.error(f"Error analyzing transcript: {e}")
        raise
