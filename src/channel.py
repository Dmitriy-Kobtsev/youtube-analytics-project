import json
import os

from googleapiclient.discovery import build

import isodate

class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('Y_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.__channel_id = self.channel["items"][0]["id"]
        self.about_channel = self.channel["items"][0]["snippet"]["description"]
        self.url = "https://www.youtube.com/channel/"+str(self.__channel_id)
        self.countsubScriber = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.viewCount = self.channel["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls, channel_id):
        return cls(channel_id)

    def to_json(self, path):
        """Метод сохранения атрибутов в фаил json"""
        data = {
            'channel_id': self.__channel_id,
            'name_channel': self.title,
            'about_channel': self.about_channel,
            'link_channel': self.url,
            'countsubScriber': self.countsubScriber,
            'videoCount': self.video_count,
            'viewCount': self.viewCount
        }
        with open(path, 'w') as file:
            json.dump(data, file)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
