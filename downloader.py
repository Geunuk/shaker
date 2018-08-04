import sys
import os
import re

import pickle
from urllib.request import urlopen
from bs4 import BeautifulSoup

from inverted_index import Dictionary, Document, Term

dic = None
url_base = "http://shakespeare.mit.edu/"
doc_counter = 0

def url_opener(url):
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

def get_term_list(doc_bs):
    # remove <table> from parse tree
    doc_bs = doc_bs.find("body")
    for table_in_doc in doc_bs.find_all("table"):
        table_in_doc.decompose()

    lines = doc_bs.find_all(string=True)
    result = []
    for line in lines:
        line = line.lower()
        line = re.sub(r'[.,!?\'\"]', '', line)
        word = re.findall(r"[\w']+", line)
        if not word == []:
            result += word
    return result

def make_document(doc_url):
    global doc_counter

    doc_html = url_opener(doc_url)
    doc_bs = BeautifulSoup(doc_html, "html.parser")
    doc_name = doc_bs.find("title").get_text().strip()
    term_list = get_term_list(doc_bs)
    doc_id = doc_counter
    doc_counter += 1

    print(doc_id, doc_name)
    return Document(doc_id, doc_url, doc_name, term_list)

def download_comedy_history_tragedy(bs):
    doc_bs_list = bs.find_all("a")
    for doc_bs in doc_bs_list:
        doc_url = url_base + doc_bs["href"].split('/')[0] + "/full.html"
        doc = make_document(doc_url)
        dic.add_document(doc)

def download_sonnet(bs):
    sonnet_url = url_base + bs.find_all("a")[0]["href"]
    sonnet_html = url_opener(sonnet_url)
    sonnet_bs = BeautifulSoup(sonnet_html, "html.parser")

    doc_bs_list = sonnet_bs.find_all("a")[3:]
    for doc_bs in doc_bs_list:
        doc_url = url_base + "Poetry/" + doc_bs["href"]
        doc = make_document(doc_url)
        dic.add_document(doc)

def downlaod_poetry(bs):
    doc_bs_list = bs.find_all("a")[1:]
    for doc_bs in doc_bs_list:
        doc_url = url_base + doc_bs["href"]
        doc = make_document(doc_url)
        dic.add_document(doc)

def download():
    """ donwload pickle file for each play """
    global dic

    test_already_download()

    index_html = url_opener(url_base + "index.html")
    index_bs = BeautifulSoup(index_html, "html.parser")
    bs_list = index_bs.find_all("td", valign="BASELINE")

    for bs_obj in bs_list[:-1]:
        download_comedy_history_tragedy(bs_obj)
    download_sonnet(bs_list[-1])
    downlaod_poetry(bs_list[-1])

    pickle.dump(dic, open("dictionary.p", "wb"))

if __name__ == "__main__":
    dic = Dictionary("shakespeare")
    download()

"""
    for play in play_list:
        play_id = play_list.index(play)
        play_name = play.get_text().strip()
        if play_id == 6:
            play_name = "The Merry Wives of Windsor"
        get_html(play_id, play_name, url_base + play["href"])

    print("total %(p) plays and %(d) docs" % {'p':str(len(play_list)), 'd':str(doc_counter)})
"""
"""
# get html file for each play
def get_html(play_id, play_name, play_url):
    global doc_counter, file_count

    try:
        play_html = urlopen(play_url)
    except:
        print("error in urlopen!")

    doc_id = doc_counter
    file_name = str(doc_id) + "-" + play_name
    play_bs = BeautifulSoup(play_html, "html.parser")

    if play_id == 37:
        sonnet_list = play_bs.find("dl").findAll("a")
        for sonnet in sonnet_list:
            doc_id = doc_counter
            doc_counter += 1
            if doc_id < file_count:
                return

            sonnet_url = sonnet.attrs["href"]
            sonnet_url = play_url.rpartition('/')[0] + "/" + sonnet_url
          
            file_name = sonnet.get_text().replace('.', ' ')
            file_name = str(doc_id) + "-" + file_name

            result = get_word_list(sonnet_url)
            #download_word_list(result, file_name)


    
    elif 38 <= play_id and play_id <= 41 :
        if doc_id < file_count:
            return
        doc_counter += 1
        script_url = play_url

        result = get_word_list(script_url)
        #download_word_list(result, file_name)

        
    else:
        if doc_id < file_count: 
            return

        doc_counter += 1
        script_url = play_bs.find("a", href="full.html").attrs["href"]
        script_url = play_url.rpartition('/')[0] + "/" + script_url 
        ''''''
        list_of_term = get_word_list(script_url)
        dic.add_term_list(list_of_term)
        for term in result:
            dic.add_term(term)
            term.postings_list.add_posting(Posting(doc_id))
        #download_word_list(result, file_name)
"""
"""
def get_word_list(script_url):
    script_html = urlopen(script_url)
    script_bs = BeautifulSoup(script_html, "html.parser")

    # remove <table> from parse tree
    lines = script_bs.find("body")
    for table_in_script in lines.findAll("table"):
        table_in_script.decompose()

    lines = lines.find_all(string=True)
    result = []
    for line in lines:
        line = line.lower()
        line = re.sub(r'[.,!?\'\"]', '', line)
        word = re.findall(r"[\w']+", line)
        if not word == []:
            result += word

    return result
"""

""" 이제 안써
class Dictionary:
    def __init__(self, name):
        self.name = name
        self.word_list = []

    def add_word(self, word):
        self.word_list.append(word)

class Word:
    def __init__(self, name, doc_id):
        self.name = name
        self.frequency = 1
        self.posting_list = [doc_id]

    def insert_posting(self):
        self.frequency += 1
"""

""" 주인 없다...
def already_download_file(file_path):
    if not os.path.exists(file_path):
        return False
    else:
        return True
"""


""" ??? 이것도 주인이 없다
def sort_word_dic(result, doc_id):
    dic = Dictionary(doc_id)
    for i in range(0, len(result)):
        if i != 0 and result[i-1] == result[i]:
            dic.word_list[-1].insert_posting()
        else:
            dic.add_word(Word(result[i],1))
            
    download_word_dic(result)
"""
""" 필요없다 download dictionary 하면 댐 
def download_word_list(result, file_name):
    file_name += ".p"
    os.makedirs("data", exist_ok=True)
    file_path = "data/" + file_name


    if not os.path.exists(file_path):
        print("Download", file_name, "...")
        pickle.dump(result, open(file_path, "wb"))
"""

""" ??? 주인 없는 함수
def download_script(file_name, script_url):
    try:
        script_html = urlopen(script_url)
    except:
        print("error in urlopen!")

    os.makedirs("html", exist_ok=True)
    file_path = "html/" + file_name
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(script_html.read())
"""
