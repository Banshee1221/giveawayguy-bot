import sqlite3


def check_post(post_dict):

    to_post = []
    print("here")
    con = None

    try:
        con = sqlite3.connect("posts.db")

        with con:
            cur = con.cursor()
            cur.execute(
                "CREATE TABLE posts(utc_time INTEGER PRIMARY KEY, web_domain TEXT, thumbnail_link TEXT, url_link TEXT, title_name TEXT, active TEXT);")

    except sqlite3.OperationalError:

        pass

    with con:
        cur = con.cursor()
        for dicts in post_dict:
            print(dicts)
            try:
                print("{0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(int(dicts["created_utc"]),
                                                            str(dicts["domain"]),
                                                            str(dicts["thumbnail"]),
                                                            str(dicts["url"]),
                                                            str(dicts["title"]),
                                                            str(dicts["link_flair_text"])))

                cur.execute('INSERT INTO posts values ({0}, "{1}", "{2}", "{3}", "{4}", "{5}");'.format(
                    int(dicts["created_utc"]), str(dicts["domain"]), str(dicts["thumbnail"]), str(dicts["url"]),
                    str(dicts["title"]), str(dicts["link_flair_text"])))
                to_post.append(dicts)
            except sqlite3.IntegrityError:
                continue

    return to_post
