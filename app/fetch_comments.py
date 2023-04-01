import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yaml

def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_file = os.path.join(current_dir, "app.yaml")

    with open(yaml_file, "r") as f:
        config = yaml.safe_load(f)

    return config

config = load_config()
YOUTUBE_API_KEY = config["env_variables"]["YOUTUBE_API_KEY"]

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_authenticated_service():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)

def is_video_id_valid(video_id):
    youtube = get_authenticated_service()

    try:
        response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()
        
        if response["pageInfo"]["totalResults"] > 0:
            return True
    except Exception as e:
        print(f"Error occurred: {e}")
        
    return False

def get_video_comments(video_id, max_results=100):
    if not is_video_id_valid(video_id):
        print("Invalid video ID")
        return []

    youtube = get_authenticated_service()

    try:
        results = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=max_results,
            order='relevance'
        ).execute()
    except HttpError as e:
        print(f'An error occurred: {e}')
        return []
    
    comments = []
    for item in results['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    return comments
