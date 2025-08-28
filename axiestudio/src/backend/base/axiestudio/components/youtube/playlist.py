from pytube import Playlist  # Ensure you have pytube installed

from axiestudio.custom.custom_component.component import Component
from axiestudio.inputs.inputs import MessageTextInput
from axiestudio.schema.data import Data
from axiestudio.schema.dataframe import DataFrame
from axiestudio.template.field.base import Output


class YouTubePlaylistComponent(Component):
    display_name = "YouTube-spellista"
    description = "Extraherar alla video-URL:er från en YouTube-spellista."
    icon = "YouTube"  # Replace with a suitable icon

    inputs = [
        MessageTextInput(
            name="playlist_url",
            display_name="Spelliste-URL",
            info="URL för YouTube-spellistan.",
            required=True,
        ),
    ]

    outputs = [
        Output(display_name="Video-URL:er", name="video_urls", method="extract_video_urls"),
    ]

    def extract_video_urls(self) -> DataFrame:
        playlist_url = self.playlist_url
        playlist = Playlist(playlist_url)
        video_urls = [video.watch_url for video in playlist.videos]

        return DataFrame([Data(data={"video_url": url}) for url in video_urls])
