from slack_wrapper import SlackWrapper
import config


def test_get_channel():
    slack = SlackWrapper()
    channel_info = slack.get_channel(config.DELL_SLACK_CHANNEL_ID)
    assert channel_info is not None


def test_get_channel_age_in_days():
    slack = SlackWrapper()
    age = slack.get_channel_age_in_days(config.DELL_SLACK_CHANNEL_ID)
    assert age > 0

def test_get_all_channels():
    slack = SlackWrapper()
    channels = slack.get_all_channels()
    assert channels is not None

def test_get_channel_bookmarks():
    channel_id = 'C0713543Z6Z'
    slack = SlackWrapper()
    bookmarks = slack.get_channel_bookmarks(config.ACME_SLACK_CHANNEL_ID)
    assert bookmarks is not None

def test_get_all_channels_with_placeholder_bookmark_link_urls():
    """This verifies that we can find the Slack channel_id list where
    any bookmark.link='www.google.com' """
    slack = SlackWrapper()
    channels = slack.get_all_channels_with_placeholder_bookmark_link_urls()
    channel_ids = [channel['channel_id'] for channel in channels]
    channel_count = len(channel_ids)
    assert channel_count > 0


def test_get_all_recently_created_channels():
    slack = SlackWrapper()
    channels = slack.get_all_recently_created_channels(days_ago=90)
    assert channels is not None

if __name__ == "__main__":
    test_get_all_channels()
    test_get_channel_bookmarks()
    test_get_all_channels_with_placeholder_bookmark_link_urls()
