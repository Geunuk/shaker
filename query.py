import pickle
from inverted_index import PostingsList
from indexer import parser, indexing

def query(qstr):
    # and AND 뚤따까능
    qterms = qstr.split(" and ")
    with open("dictionary.pkl", 'rb') as f:
        dic = pickle.load(f)
        result = PostingsList()
        result.extend(dic.find(qterms[0]).postings_list)
        #[print(x.doc_id, end= ', ') for x in dic[0].postings_list]
        #[print(x.doc_id, end= ', ') for x in result]
        #print()

        for t in qterms:
            print(t, end=": ")
            [print(x.doc_id, end= ', ') for x in dic.find(t).postings_list]
            print()

        for t in qterms[1:]:
            #[print(x.doc_id, end= ', ') for x in result]
            result.intersect(dic.find(t).postings_list)
            [print(x.doc_id, end= ', ') for x in result]
            print()
        return result
if __name__ == "__main__":
    indexing()
    query("wrong and stay")
    """
    x_postings_list, y_postings_list =  set(), set()
    for t in dic:
        if t.word == x:
            x_postings_list = {posting.doc_id for posting in  t.postings_list}
            print("x", x_postings_list)
        if t.word == y:
            y_postings_list = {posting.doc_id for posting in  t.postings_list}
            print("y", y_postings_list)
    return x_postings_list & y_postings_list
    """
