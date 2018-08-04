class Dictionary(list):
    def __init__(self, dic_name = None, term_list=[]):
        self.dic_name = dic_name
        self.extend(term_list)

    def add_term(self, term):
        #print('add_term')
        self.append(term)

    def add_term_list(self, term_list):
        #print('add_term_list')
        self.extend(term_list)

    def add_document(self, doc):
        for t1 in doc.term_list:
            for t2 in self:
                if t1 == t2.word:
                    t2.postings_list.add_posting(Posting(doc.doc_id))
                    break
            else:
                t = Term(t1)
                t.postings_list.add_posting(Posting(doc.doc_id))
                self.add_term(t)



class PostingsList(list):
    def __init__(self, list_of_postings=[]):
        self.extend(list_of_postings)

    def add_posting(self, posting):
        #print('add_posting')
        for p in self:
            if p.doc_id == posting.doc_id:
                break
        else:
            self.append(posting)

class Term():
    def __init__(self, word, postings_list=PostingsList()):
        self._word = word
        self.postings_list = postings_list

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, value):
        self._word = value

    @word.deleter
    def word(self):
        del self._word

    @staticmethod
    def make_term_list(list_of_string):
        return [Term(word) for word in list_of_string]

class Posting():
    def __init__(self, doc_id):
        self._doc_id = doc_id

    @property
    def doc_id(self):
        return self._doc_id

    @doc_id.setter
    def doc(self, value):
        self._doc_id = value

    @doc_id.deleter
    def doc_id(self):
        del self._doc_id

class Document():
    def __init__(self, doc_id, doc_url, doc_name, term_list):
        self.doc_id = doc_id
        self.doc_url = doc_url
        self.doc_name = doc_name
        self.term_list = term_list

if __name__ == '__main__':
    t1 = Term('ape')
    t2 = Term('bus')
    
    t1.postings_list.add_posting(Posting(1))
    t1.postings_list.add_posting(Posting(3))
    t2.postings_list.add_posting(Posting(5))

    d = Dictionary([t1, t2])
