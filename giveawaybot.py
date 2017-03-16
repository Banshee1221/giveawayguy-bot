import os
import time
import datetime
from slackclient import SlackClient
import json
from urllib.request import urlopen

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def qsort(inlist):
    if inlist == []:
        return []
    else:
        pivot = inlist[0]
        lesser = qsort([x for x in inlist[1:] if x < pivot])
        greater = qsort([x for x in inlist[1:] if x >= pivot])
        return lesser + [pivot] + greater

def reddit_update():

    to_send = []

    id_counter = open("ids.txt", "r+")
    id_counter_content = id_counter.read()
    id_list = id_counter_content.splitlines(True)
    id_list = [line.rstrip('\n') for line in id_list]
    id_counter.seek(0)

    while True:
        try:
            d = json.load(urlopen("http://www.reddit.com/r/freegamesonsteam/new.json?sort=new"))
            break
        except:
            continue

    items_to_store = ["domain", "thumbnail", "url", "title", "created_utc"]

    for objects in d['data']['children']:
        if str(objects['data']['created_utc']) in id_counter_content:
            continue
        tmp_data = objects['data']
        if len(id_list) == 25:
            id_list = id_list[1:]
        #print(id_list[1:])
        id_list.append(str(tmp_data['created_utc']).strip())
        game_dict = {}
        for keys in items_to_store:
            game_dict[keys] = tmp_data[keys]
        to_send.append(game_dict)
        #print(json.dumps(game_dict, indent=2))x

    id_list = qsort(id_list)
    for tstamps in id_list:
        id_counter.write("{0}\n".format(tstamps))

    id_counter.close()

    return to_send

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
    READ_WEBSOCKET_DELAY = 600
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            time.sleep(READ_WEBSOCKET_DELAY)
            print("running handler")
            post_handler(reddit_update())
            #reddit_update()
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
