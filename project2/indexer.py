'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from linkedlist import LinkedList
from collections import OrderedDict


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        self.token_count_in_doc = {}

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        for t in tokenized_document:
            self.add_to_index(t, doc_id)
        self.token_count_in_doc[doc_id] = len(tokenized_document)

    def add_to_index(self, term_, doc_id_):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented."""
        #print("TERMMMM ---- " + term_)
        inverted_index = self.inverted_index
        if term_ not in inverted_index:
            #Create new postings list
            link_list = LinkedList()
            link_list.insert_at_end(doc_id_)
            inverted_index[term_] = link_list

        else:
            #Add it to the existing postings list
            link_list = inverted_index[term_]
            value = link_list.increment_tf_docID(doc_id_)
            if value == -1:
                link_list.insert_at_end(doc_id_)
        #link_list.print_linklist()

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index
        #print(self.inverted_index)

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        for key in self.inverted_index:
            #print("Calling skip connections: " + key)
            if(key == "epidemiolog"):
                #print("printing skip pointers")
                print(self.inverted_index[key])
            self.inverted_index[key].add_skip_connections()
        #raise NotImplementedError

    def calculate_tf_idf(self,count):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
        #total_docs = 5
        for key in self.inverted_index:
            print("scores for the term -------> " + key)
            self.inverted_index[key].calculate_doc_score(count,self.token_count_in_doc)
        #raise NotImplementedError

    def get_postings_list(self,term,isSkipPointer):
        postingslist = []
        if term not in self.inverted_index:
            return postingsList
        if isSkipPointer is False:
            postingsList = self.inverted_index[term].traverse_list()
        else:
            postingsList = self.inverted_index[term].traverse_skips()
        return postingsList

