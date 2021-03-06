"""
Transfers data from old database to new database
TODO: Add 'image link to news_article table' & Change pubdate value from text to datetime
"""
import sqlite3

new_database = "/home/cyxnide/websites/ssdnewsnow/ssdnewsnow.sqlite3"
old_database = "thecomradenews.db"


def save_data(data_tuple_list: list):
    """
    Saves data into the database
    """
    con = sqlite3.connect(new_database)
    cur = con.cursor()
    """  cur.execute('''CREATE TABLE "news_articles"(
        "id" integer NOT NULL,
        "source" text,
        "title" text,
        "link" text,
        "pubdate" TEXT,
        "guid" integer,
        "description" text,
        "content" text,
        "categories" text,
        PRIMARY KEY("id" AUTOINCREMENT)
    )''')  """

    for i in data_tuple_list:
        try:
            cur.execute("INSERT INTO news_article values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", i)
            print(f"Article Added: 'id={i[0]}-{i[2]}'")
            con.commit()
        except sqlite3.OperationalError as e:
            print(e)
        except sqlite3.IntegrityError:
            print(f"Article Already Exists: 'id={i[0]}-{i[2]}'")
    con.close()


def retrieve_data():
    """" Retrieves articles from the sqlite database """
    con = sqlite3.connect("thecomradenews.db")
    cur = con.cursor()
    try:
        rows = cur.execute("SELECT * FROM articles ORDER BY pubdate")
    except sqlite3.OperationalError as e:
        print(f"Failed: {e}")
    return rows


id_ = 1
data_list = []
for j in retrieve_data():
    article_id = id_
    source = j[0]
    article_title = j[1]
    article_link = j[2]
    article_pubdate = j[3]
    article_guid = j[4]
    article_description = j[5]
    article_content = j[6]
    categories = j[7]
    image_link = j[8]

    data_tuple = (
        article_id,
        source,
        article_title,
        article_link,
        article_pubdate,
        article_guid,
        article_description,
        article_content,
        categories,
        image_link,
    )

    data_list.append(data_tuple)
    id_ = id_ + 1

save_data(data_list)
