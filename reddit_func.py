import json
from extra import qsort
from urllib.request import urlopen


def reddit_update():

    to_send = []

    id_counter = open("ids.txt", "r+")
    id_counter_content = id_counter.read()
    id_list = id_counter_content.splitlines(True)
    id_list = [line.rstrip('\n') for line in id_list]
    id_counter.seek(0)

    while True:
        try:
            print("Collecting json")
            get_url = urlopen("http://www.reddit.com/r/me_irl/new.json?sort=new")
            formatted = get_url.read().decode('utf-8')
            d = json.loads(formatted)
            print(d)
            break
        except Exception as e:
            print(e)
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