
"""
    for play in play_list:
        play_id = play_list.index(play)
        play_name = play.get_text().strip()
        if play_id == 6:
            play_name = "The Merry Wives of Windsor"
        get_html(play_id, play_name, base_url + play["href"])

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
            #crawl_word_list(result, file_name)


    
    elif 38 <= play_id and play_id <= 41 :
        if doc_id < file_count:
            return
        doc_counter += 1
        script_url = play_url

        result = get_word_list(script_url)
        #crawl_word_list(result, file_name)

