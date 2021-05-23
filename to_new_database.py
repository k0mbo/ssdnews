import sqlite3

new_database = "../ssdnewsnow/thecomradenews.db"
old_database = "thecomradenews.db"


def save_data(data_tuple_list: list):
    """
    Saves data into the database
    """
    con = sqlite3.connect(new_database)
    cur = con.cursor()

    for i in data_tuple_list:
        try:
            cur.execute("INSERT INTO news_articles values (?, ?, ?, ?, ?, ?, ?, ?, ?)", i)
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
    data_tuple = (
        article_id,
        source,
        article_title,
        article_link,
        article_pubdate,
        article_guid,
        article_description,
        article_content,
        categories
    )

    data_list.append(data_tuple)
    id_ = id_ + 1

save_data(data_list)
