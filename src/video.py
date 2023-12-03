import json
import os

from googleapiclient.discovery import build


class Video:

    api_key: str = os.getenv('Y_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video):
        try:
            video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=id_video
                                                   ).execute()
            self.video_id = id_video
            self.link = 'https://youtu.be/' + id_video
            self.title = video_response['items'][0]['snippet']['title']
            self.view_count = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except Exception:
            self.video_id = id_video
            self.link = None
            self.title = None
            self.view_count = None
            self.like_count = None


    def __str__(self):
        return f'{self.title}'



class PLVideo(Video):
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.playlist_id = id_playlist
