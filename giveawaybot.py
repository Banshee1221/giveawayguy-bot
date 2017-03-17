import os
import time
import sys
import datetime
from slackclient import SlackClient
from reddit_func import reddit_update
from db import check_post

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def post_handler(list_to_post):

    channel_list = slack_client.api_call(
        "channels.list",
        exclude_archived="true"
    )

    channels_belonging_to = []

    for channels in channel_list['channels']:
        if channels['is_member']:
            for dictionaries in list_to_post:
                to_send = """Free game for Steam found!
---------------------------------

*{0}*
>>> Link:\t\t   {1}
Host:\t\t  {2}
Found:\t\t{3}""".format(dictionaries["title"], dictionaries["url"], dictionaries["domain"], datetime.datetime.fromtimestamp(int(dictionaries["created_utc"])).strftime('%Y-%m-%d %H:%M:%S'))
                print("sending message")
                slack_client.api_call(
                    "chat.postMessage",
                    channel=channels['id'],
                    text=str(to_send),
                    as_user="true",
                    username="giveawayguy"
                )


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 10
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            # time.sleep(READ_WEBSOCKET_DELAY)
            print("running handler")
            print(check_post(reddit_update()))
            for i in range(READ_WEBSOCKET_DELAY):
                sys.stdout.write("{0}s\r".format(i))
                sys.stdout.flush()
                time.sleep(1)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
