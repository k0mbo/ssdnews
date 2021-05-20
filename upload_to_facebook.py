import requests
import sqlite3


def retrieve_data():
    """" Retrieves articles from the sqlite database """
    con = sqlite3.connect("thecomradenews.db")
    cur = con.cursor()
    try:
        rows = cur.execute("SELECT * FROM articles ORDER BY pubdate")
    except sqlite3.OperationalError as e:
        print(f"Failed: {e}")
    return rows


def upload_to_page(articles):
    """ Upload to the facebook page """
    graph_api = "https://graph.facebook.com/"
    access_token = "EAALc0Lt6BcoBAP2WD5HpQ2fe2iiuCTQg2L0sbVOP1jQPMELuZAXNmFnu3v7yZALHwGgjuFpNfm3b\
            EplQArOD3nIxnQRYrfcHpAXWvWmtx96xX3ZBTeY6fkwTZBucz1Nlm70tLO5tiEWb281X1aXV7rv6qBVkqvuF1n7TZBv7dpQTpzCtK1kGo"
    id = "112365750247736"
    for article in articles:
        a_id = article[4]
        if article[0] == "Sudans Post":
            guid = f"{str(a_id)}000"
            source = "Sudans Post"
            cat = article[7].replace(' ', '_')
            categories = cat.replace('/', ' #')
            like_page = "Like and follow our page for more updates."
            the_post = article[1] + "\n\n\n" + article[6] + "\n\t" + like_page + "\n\n" + source + "\n\n" + categories
        elif article[0] == "Radio Tamazuj - Latest news":
            e_guid = str(a_id)
            guid = e_guid[:8]
            source = "Radio Tamazuj - Latest news"
            the_post = article[1] + "\n\n\n" + article[6] + "\n\t" + source

        j = requests.post(f"{graph_api}{id}/feed?message={the_post}&access_token={access_token}")
        if j.status_code != 200:
            print(f"Unsuccessful: {j.status_code}")
        elif j.status_code == 200:
            if check_article(guid):
                continue
            else:
                print(f"Uploading and saving article to log: {article[1]}.")


def check_article(article_id: str):
    """
    Checks if article was already uploaded.
        False: means not uploaded
        True: means uploaded
    """
    with open('articles_log.txt', 'r') as read_lf:
        article_ids = read_lf.readlines()
    guids_list = []
    for i in article_ids:
        guids_list.append(i.rstrip())

    if article_id in guids_list:
        return True
    else:
        with open('articles_log.txt', 'a') as write_lf:
            write_lf.write(article_id + "\n")
        return False


article_data = retrieve_data()
upload_to_page(article_data)
