import json
from urllib.request import urlopen


def reddit_update():

    to_send = []

    while True:
        try:
            print("Collecting json")
            get_url = urlopen("http://www.reddit.com/r/freegamesonsteam/new.json?sort=new")
            formatted = get_url.read().decode('utf-8')
            d = json.loads(formatted)
            break
        except Exception as e:
            print(e)
            continue

    items_to_store = ["domain", "thumbnail", "url", "title", "created_utc"]

    for objects in d['data']['children']:
        tmp_data = objects['data']
        game_dict = {}
        for keys in items_to_store:
            game_dict[keys] = tmp_data[keys]
        if tmp_data["link_flair_text"] in ("ended", "Ended"):
            game_dict["link_flair_text"] = tmp_data["link_flair_text"]
        else:
            game_dict["link_flair_text"] = "None"
        to_send.append(game_dict)

    return to_send