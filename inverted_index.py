import heapq

class Dictionary(list):
    def __init__(self, term_list=[]):
        self.extend(term_list)
    
    def __contains__(self, item):
        return item in  {x.word for x in self}
    
    def find(self, term):
        for x in self:
            if x.word == term:
                return x
        else:
            return None

    def add_term(self, term):
        self.append(term)

    def add_term_list(self, term_list):
        self.extend(term_list)

    def add_document(self, doc_id, term_list):
        for t1 in term_list:
            for t2 in self:
                if t1 == t2.word:
                    t2.postings_list.add_posting(Posting(doc_id))
                    break
            else:
                new_term = Term(t1)
                new_term.postings_list.add_posting(Posting(doc_id))
                self.add_term(new_term)

class PostingsList(list):
    def intersect(self, pl2):
        pl1 = self
        i, j = 0, 0

        while i != len(pl1) and j != len(pl2):
            if pl1[i].doc_id == pl2[j].doc_id:
                i += 1
                j += 1
            elif pl1[i].doc_id < pl2[j].doc_id:
                pl1.pop(i)
            else:
                j += 1

        del pl1[i:len(pl1)]

    def add_posting(self, posting):
        if len(self) == 0:
            self.append(posting)
            return

        for i in range(len(self)):
            if self[i].doc_id == posting.doc_id:
                break
            elif self[i].doc_id < posting.doc_id:
                pass
            else:
                self.insert(i, posting)
        else:
            self.append(posting)
    """
    def add_posting(self, posting):
        #print('add_posting')
        for p in self:
            if p.doc_id == posting.doc_id:
                break
        else:
            self.append(posting)
    """
class Term():
    def __init__(self, word):
        self.word = word
        self.postings_list = PostingsList()

    def intersect(self, t2):
        return self.postings_list.intersect(t2.postings_list)
    
    @staticmethod
    def make_term_list(list_of_string):
        return [Term(word) for word in list_of_string]

class Posting():
    def __init__(self, doc_id):
        self.doc_id = doc_id
    
    def __lt__(self, p2):
        return self.doc_id < p2.doc_id

class Document():
    def __init__(self, doc_id, genre, name_1, name_2, doc_url):
        self.doc_id = doc_id
        self.name_1 = name_1
        self.name_2 = name_2
        self.doc_url = doc_url

if __name__ == '__main__':
    t1 = Term('ape')
    t2 = Term('bus')
    
    t1.postings_list.add_posting(Posting(1))
    t1.postings_list.add_posting(Posting(3))
    t2.postings_list.add_posting(Posting(5))

    d = Dictionary([t1, t2])
