"""
REQUIRES REWRITING BEFORE ANYMORE USAGE!!!!!
"""


from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests
import sqlite3
from time import strptime


def save_data(data_tuple_list: list):
    """
    Saves data into the database
    """
    con = sqlite3.connect("thecomradenews.db")
    cur = con.cursor()
    try:
        cur.execute('''CREATE TABLE articles
                        (source text,
                        title text,
                        link text,
                        pubdate date,
                        guid integer,
                        description text,
                        content text,
                        categories text,
                        image_link TEXT,
                        UNIQUE(source, title, link, pubdate, guid, description, content, categories, image_link)
                        )''')
    except sqlite3.OperationalError as e:
        print(e)
    for i in data_tuple_list:
        try:
            cur.execute("INSERT INTO articles values (?, ?, ?, ?, ?, ?, ?, ?, ?)", i)
            print(f"Article Added: '{i[1]}'")
            con.commit()
        except sqlite3.OperationalError as e:
            print(e)
        except sqlite3.IntegrityError:
            print(f"Article Already Exists: '{i[1]}'")
    con.close()


def retrieve_data():
    """" Retrieves articles from the sqlite database """
    con = sqlite3.connect("/home/cyxnide/websites/ssdnewsnow/ssdnewsnow.sqlite3")
    cur = con.cursor()
    iid = cur.execute("SELECT max(id) FROM news_article")
    return iid


id_ = iid[0]


def article_cleanser(dirty_content):
    """Cleanse the articles and call the saving function to save it"""
    global id_

    articles_dict = {}
    source = dirty_content.find("title").get_text()
    data_tuple_list = []

    for item in dirty_content.find_all("item"):
        article_link = item.link.get_text()

        jj = item.pubDate.get_text().split(' ')
        article_pubdate = datetime(int(jj[3]), int(strptime(jj[2], '%b').tm_mon), int(jj[1]), int(jj[4][:2]),
                                   int(jj[4][3:5]),
                                   int(jj[4][6:])).isoformat(' ')

        if source == "Sudans Post":
            """ If the feed is for Sudans Post then it should scrap accordingly"""
            article_number = item.guid.get_text()
            guid_list = re.findall("(?<=p=)[0-9]{5}", article_number)
            article_guid = int(guid_list[0] + '000')
            article_description = item.description.get_text().replace('[&#8230;]', '....')
            article_description = article_description.replace('&#8217;', "'")
            article_title = item.title.get_text().replace(u'\xa0', ' ')
            article_text = item.encoded.get_text()  # gives a not-navigable string

            """
            So to make the article_content navigable  I write it into a html file
            and retrieving it again below
            """
            with open("article_content.html", 'w') as fp:
                fp.write(article_text)

            with open("article_content.html", "r") as fp:
                article_soup = BeautifulSoup(fp, "lxml")

            article_content = ""
            for c in article_soup.find_all('p'):
                article_content += "\n" + c.get_text()

            image_link = article_soup.find('a')["href"]

            categories = ""
            for cat in item.find_all("category"):
                categories += f"/{cat.get_text().lower()}"

        elif source == "Radio Tamazuj - Latest news":
            """If the feed is for Radio tamazuj, scrap accordingly """

            article_title = item.title.get_text()
            article_description = item.description.get_text()
            article_guid = item.guid.get_text()[:8]
            categories = "Not available"

            def get_content_from_link(link):
                """ 
                Gets the article from the link, because radio tamazuj doesn't 
                post the article content on the rss feed
                """

                page = requests.get(link)
                soup = BeautifulSoup(page.text, "lxml")
                return soup

            soup = get_content_from_link(article_link)
            image_link = "https://radiotamazuj.org" + soup.find("img")["src"]

            body = soup.select(".body-text")
            content = ""
            for i in body:
                content += i.get_text()
            article_content = content.replace(u'\xa0', ' ')

        articles_dict[id_] = {
            "id": id_,
            "source": source,
            "Title": article_title,
            "Link": article_link,
            "PubDate": article_pubdate,
            "guid": article_guid,
            "Description": article_description,
            "Content": article_content,
            "categories": categories,
            "image_link": image_link,
        }
        data_tuple = (
            id_,
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
        id_ += 1  # counts number of articles
        data_tuple_list.append(data_tuple)
    return data_tuple_list


def article_extractor(rss_feed_link):
    """ Extracts the article from the feed"""
    user_agent = {"user-agent": "Mozilla/5.0 (Windows NT 6.2; Win64;\
            x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"}
    try:
        feed = requests.get(rss_feed_link, headers=user_agent)
    except requests.exceptions.ConnectionError:
        print("No internet connection")
        exit()

    dirty_content = BeautifulSoup(feed.text, "xml")
    return dirty_content


rss_feeds = ["https://radiotamazuj.org/en/rss/news.xml",
             "https://www.sudanspost.com/feed/", ]


def main():
    for i in rss_feeds:
        d = article_extractor(i)
        save_data(article_cleanser(d))




main()
