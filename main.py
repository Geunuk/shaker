from urllib.request import urlopen
from bs4 import BeautifulSoup
import os.path

url_base = "http://shakespeare.mit.edu/"

def download():
    try:
        html = urlopen(url_base + "index.html")
    except:
        print("error in urlopen!")
        return

    main_bs_obj = BeautifulSoup(html, "html.parser")
    play_list = main_bs_obj.findAll("tr")[2].findAll("a")

    print("total : " + str(len(play_list)) + " plays")
    for play in play_list:
        idx = play_list.index(play)
        name = play.get_text().strip()
        if idx == 6:
            name = "The Merry Wives of Windsor"
        find_play(idx, name, url_base + play["href"])

def find_play(idx, name, play_url):
    print("Download", idx, name,"...")
    try:
        play_html = urlopen(play_url)
    except:
        print("error in urlopen!")

    play_bs_obj = BeautifulSoup(play_html, "html.parser")
    if idx == 37:
        sonnet_list = play_bs_obj.find("dl").findAll("a")
        print(sonnet_list)
        for sonnet in sonnet_list:
            sonnet_url = sonnet.attrs["href"]
            sonnet_url = play_url.rpartition('/')[0] + "/" + sonnet_url
            file_name = sonnet.get_text().replace('.', ' ')
            print("Download", idx, file_name,"...")
            file_name = str(idx + 1) + "-" + file_name + ".html"
            download_script(file_name, sonnet_url)
    
    elif 38 <= idx and idx <= 41 :
        script_url = play_url
        file_name = str(idx + 1) + "-" + name + "html"
        download_script(file_name, script_url)
    else:
        script_url = play_bs_obj.find("a", href="full.html").attrs["href"]
        script_url = play_url.rpartition('/')[0] + "/" + script_url 
        file_name = str(idx + 1) + "-" + name + ".html"
        download_script(file_name, script_url)

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

def main():
    download()

if __name__ == "__main__":
    main()
