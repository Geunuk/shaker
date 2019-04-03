import sys
import os
import re

import pickle
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from inverted_index import Dictionary, Document, Term

base_url = "http://shakespeare.mit.edu/"
doc_counter = 0

def open_url(url):
    try:
        html = urlopen(url)
        return html
    except:
        print("error in open :", url)
        sys.exit(0)

def already_download():
    if not os.path.exists("./data/"):
        return 0
    else:
        file_count = len([name for name in os.listdir("data/")])
        if file_count != 195:
            return file_count
        else:
            return True

def test_already_download():
    file_count = already_download()
    if file_count == 195:
        print("Already download dictionary data")
        return

def parser(string):
    string = string.lower()
    string = re.sub(r'[.,!?\'\"]', '', string)
    return re.findall(r"[\w']+", string)

def crawl_doc(doc_url):
    doc_html = open_url(doc_url)
    doc_bs = BeautifulSoup(doc_html, "html.parser")

    # remove <table> from parse tree
    doc_bs = doc_bs.find("body")
    for doc_table in doc_bs.find_all("table"):
        doc_table.decompose()

    term_list = []
    lines = doc_bs.find_all(string=True)
    for line in lines:
        term_list +=  parser(line)
    return term_list

def crawl_play(dic, genre, play_url):
    global doc_counter

    play_html = open_url(play_url)
    play_bs = BeautifulSoup(play_html, "html.parser")
    play_name = play_bs.find("td", class_="play").contents[0].strip()

    p_list = play_bs.find_all("p")
    for i, p in enumerate(p_list):
        if "Entire play" in p.text:
            scenes = p_list[i+1]

    scenes_text = scenes.text.replace('\n\n', '\n')
    scene_names = scenes_text.strip().split('\n')
    scene_urls = [urljoin(play_url,  x["href"]) for x in scenes.find_all('a')]

    doc_list = []
    for scene_name, scene_url in zip(scene_names, scene_urls):
        global doc_counter
        doc_id = doc_counter
        doc_counter += 1
        doc_list.append(Document(doc_id, genre, play_name, scene_name, scene_url))
        
        term_list = crawl_doc(scene_url)
        dic.add_document(doc_id, term_list)

        print("add", len(dic), play_name, scene_name)
    return doc_list

def crawl_genre(dic, genre, genre_bs):
    doc_list = []
    play_list = genre_bs.find_all("a")
    for play_bs in play_list:
        play_url = urljoin(base_url, play_bs["href"])
        doc_list += crawl_play(dic, genre, play_url)
        break

    return doc_list

def crawl_poetry_sonnet(dic, genre, genre_bs):
    global doc_counter

    poetry_name = genre_bs.find("a").text
    poetry_url = urljoin(base_url, genre_bs.find("a")["href"])
    poetry_html = open_url(poetry_url)
    poetry_bs = BeautifulSoup(poetry_html, "html.parser")

    sonnets = poetry_bs.find("dl")
    sonnet_list = sonnets.find_all("a")

    doc_list = []
    for sonnet_bs in sonnet_list:
        doc_id = doc_counter
        doc_counter += 1

        sonnet_name = sonnet_bs.text
        sonnet_url = urljoin(poetry_url, sonnet_bs["href"])
        doc_list.append(Document(doc_id, genre, poetry_name, sonnet_name, sonnet_url))
        
        term_list = crawl_doc(sonnet_url)
        dic.add_document(doc_id, term_list)

        heapq.heappush(self, posting)
        
        print("add", len(dic), sonnet_name)
    
    return doc_list

def crawl_poetry_not_sonnet(dic ,genre, genre_bs):
    global doc_counter

    doc_list = []
    poetry_list = genre_bs.find_all("a")[1:]
    for poetry_bs in poetry_list:
        doc_id = doc_counter
        doc_counter += 1

        poetry_name = poetry_bs.text.strip()
        poetry_url = urljoin(base_url, poetry_bs["href"])
        doc_list.append(Document(doc_id, genre, poetry_name, None, poetry_url))

        term_list = crawl_doc(poetry_url)
        dic.add_document(doc_id, term_list)

        print("add", len(dic), poetry_name)
    
    return doc_list

def indexing():
    """ donwload pickle file for each play """
    dic = Dictionary()
    #test_already_download()

    home_html = open_url(base_url)
    home_bs = BeautifulSoup(home_html, "html.parser")
    genre_list = home_bs.find_all("td", valign="BASELINE")
    genres = [name.text for name in home_bs.find_all("h2")]

    doc_list = []
    for genre_bs, genre in zip(genre_list[:-1], genres):
        doc_list += crawl_genre(dic, genre, genre_bs)
        break

    #doc_list += crawl_poetry_sonnet(dic, genres[3], genre_list[-1])
    #doc_list += crawl_poetry_not_sonnet(dic, genres[3], genre_list[-1])

    pickle.dump(dic, open("dictionary.pkl", "wb"))
    pickle.dump(doc_list, open("doc_list.pkl", "wb"))

    print("total docs:", len(doc_list))
    print("total terms:", len(dic))
    return

if __name__ == "__main__":
    indexing()
