from src.video import Video
import os
import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('Y_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):

        playlist = PlayList.youtube.playlists().list(id = playlist_id,
                                             part='snippet',
                                             ).execute()
        playlist_videos = PlayList.youtube.playlistItems().list(playlistId=playlist_id,
                                                                part='contentDetails',
                                                                maxResults=50,
                                                                ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        self.video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                        id=','.join(video_ids)
                                                        ).execute()
        self.id_= playlist_id
        self.title = playlist['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + playlist_id


    @property
    def total_duration(self):
        sum_time = isodate.parse_duration('PT0M0S')
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']

            duration = isodate.parse_duration(iso_8601_duration)
            sum_time += duration

        return sum_time

    def show_best_video(self):
        count_like = 0
        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > count_like:
                count_like = int(video['statistics']['likeCount'])
                best_video = 'https://youtu.be/' + video['id']
        return best_video



