import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import List
from datetime import datetime, timedelta

class SlackWrapper:
    def __init__(self):
        load_dotenv()
        self.client = WebClient(token=os.getenv("SLACK_BOT_USER_OAUTH_TOKEN"))

    def get_channel(self, channel_id: str):
        try:
            return self.client.conversations_info(channel=channel_id).get("channel", {})
        except SlackApiError as e:
            raise HTTPException(status_code=400, detail=f"Error getting channel info: {str(e)}")

    def get_channel_age_in_days(self, channel_id: str):
        return (datetime.now() - datetime.fromtimestamp(self.get_channel(channel_id).get('created'))).days

    def get_all_channels(self):
        all_channels, cursor = [], None
        while True:
            try:
                response = self.client.conversations_list(types="public_channel,private_channel", limit=1000, cursor=cursor)
                all_channels.extend(response['channels'])
                if not (cursor := response['response_metadata'].get('next_cursor')): break
            except SlackApiError as e:
                raise HTTPException(status_code=400, detail=f"Error getting channels: {str(e)}")
        print(f"Total channels: {len(all_channels)}")
        return all_channels

    def get_all_recently_created_channels(self, days_ago: int = 30) -> List[dict]:
        all_channels = self.get_all_channels()
        recently_created_channels = []
        for channel in all_channels:
            created_timestamp = channel.get('created')
            if created_timestamp:
                age_in_days = (datetime.now() - datetime.fromtimestamp(created_timestamp)).days
                if age_in_days <= days_ago:
                    channel['age_in_days'] = age_in_days
                    recently_created_channels.append(channel)
        return recently_created_channels

    def get_channel_bookmarks(self, channel_id: str):
        try:
            return self.client.bookmarks_list(channel_id=channel_id).get("bookmarks", [])
        except SlackApiError:
            return []

    def find_matching_bookmarks(self, bookmarks: List[dict], url: str, channel_id: str):
        return [{**bookmark, 'channel_id': channel_id} for bookmark in bookmarks if bookmark.get("link") == url]

    def find_bookmarks_by_url(self, url: str):
        try:
            return [bookmark for channel in self.get_all_channels() for bookmark in self.find_matching_bookmarks(self.get_channel_bookmarks(channel['id']), url, channel['id'])]
        except SlackApiError as e:
            raise HTTPException(status_code=400, detail=f"Error listing bookmarks: {str(e)}")

    def delete_bookmarks(self, channel_id: str, bookmark_ids: List[str]):
        return [{"bookmark_id": bookmark_id, "status": "deleted" if self.client.bookmarks_remove(channel_id=channel_id, bookmark_id=bookmark_id) else "error"} for bookmark_id in bookmark_ids]

    def get_all_channels_with_placeholder_bookmark_link_urls(self):
        channels_with_bookmarks = []
        all_channels = self.get_all_recently_created_channels(days_ago=30)
        for i, channel in enumerate(all_channels, 1):
            print(f"Checking channel {i} of {len(all_channels)}: {channel.get('name')}")
            for bookmark in self.get_channel_bookmarks(channel['id']):
                if bookmark.get('link') and 'google.com' in bookmark['link']:
                    channels_with_bookmarks.append({'channel_id': channel['id'], 'channel_name': channel.get('name'), 'bookmark': bookmark})
                    print(f"Channel ID: {channel['id']}, Channel Name: {channel.get('name')}, Bookmark Title: {bookmark.get('title')}, Bookmark Link: {bookmark.get('link')}")
                    break
        return sorted(channels_with_bookmarks, key=lambda x: x['channel_name'])

if __name__ == "__main__":
    slack = SlackWrapper()
