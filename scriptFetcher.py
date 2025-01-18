import pandas as pd
import logging
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from os import environ

logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com//auth/userinfo.email','https://www.googleapis.com/auth/youtube.force-ssl']

def get_youtube_service():
    """Get authenticated YouTube service"""
    creds = None
    
    # Try to load credentials from environment variable first (for Render)
    if environ.get('GOOGLE_OAUTH_CREDENTIALS'):
        try:
            creds_dict = pickle.loads(environ.get('GOOGLE_OAUTH_CREDENTIALS').encode())
            creds = Credentials.from_authorized_user_info(creds_dict, SCOPES)
        except Exception as e:
            logger.error(f"Error loading credentials from environment: {str(e)}")
    
    # If no environment credentials, try local file
    if not creds and os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                # Save refreshed credentials
                if environ.get('RENDER'):
                    # Save to environment variable for Render
                    environ['GOOGLE_OAUTH_CREDENTIALS'] = pickle.dumps(creds.to_authorized_user_info())
                else:
                    # Save locally for development
                    with open('token.pickle', 'wb') as token:
                        pickle.dump(creds, token)
            except Exception as e:
                logger.error(f"Error refreshing token: {str(e)}")
                creds = None
        
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json' if not environ.get('GOOGLE_CLIENT_SECRETS') else environ.get('GOOGLE_CLIENT_SECRETS'),
                SCOPES,
                redirect_uri='https://your-render-domain.onrender.com/oauth2callback' if environ.get('RENDER') else 'http://localhost:8080/oauth2callback'
            )
            creds = flow.run_local_server(
                port=8080,
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'  # Force prompt to ensure we get refresh token
            )
            
            # Save the credentials
            if environ.get('RENDER'):
                environ['GOOGLE_OAUTH_CREDENTIALS'] = pickle.dumps(creds.to_authorized_user_info())
            else:
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

def get_transcript(video_id: str) -> str:
    """Get transcript using YouTube Data API with OAuth"""
    try:
        youtube = get_youtube_service()
        
        # Get video captions
        captions_response = youtube.captions().list(
            part='snippet',
            videoId=video_id
        ).execute()
        
        # Get the first available caption track
        if 'items' in captions_response and captions_response['items']:
            caption_id = captions_response['items'][0]['id']
            
            # Download the caption track
            caption = youtube.captions().download(
                id=caption_id,
                tfmt='srt'
            ).execute()
            
            # Convert caption to text
            return ' '.join(line for line in caption.decode('utf-8').split('\n') 
                          if not line.strip().isdigit() and 
                          not '-->' in line and 
                          line.strip())
        
        return ""
        
    except HttpError as e:
        logger.error(f"YouTube API error: {str(e)}")
        return ""
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
