import sqlite3
import sys


def insert_post(post_dict):
    print("here")
    #print(post_dict)

    con = None

    try:
        con = sqlite3.connect("posts.db")

        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE posts(utc_time INTEGER PRIMARY KEY, web_domain TEXT, thumbnail_link TEXT, url_link TEXT, title_name TEXT);")

    except sqlite3.OperationalError:

        pass

    with con:
        cur = con.cursor()
        for dicts in post_dict:
            print(dicts)
            cur.execute("INSERT INTO posts values ({0}, {1}), {2}, {3}, {4});".format(int(dicts["created_utc"]), str(dicts["domain"]), str(dicts["thumbnail"]), str(dicts["url"]), str(dicts["title"])))


    #except sqlite3.Error as e:

    #    print("Error: {0}".format(e.args[0]))
    #    sys.exit(1)

   # finally:
#
 #       if con:
  #          con.close()