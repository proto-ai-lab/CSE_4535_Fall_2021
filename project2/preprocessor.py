'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""
        text.lower()
        preprocessed_text = ""
        token_list = []
        plain_text = re.sub(r"[^a-zA-Z0-9]+",' ', text)
        preprocessed_text = plain_text.strip()
        for token in preprocessed_text.split(" "):
            if(token not in self.stop_words):
                stemmed_word = self.ps.stem(token)
                token_list.append(stemmed_word)
        print(token_list)

        return token_list
        
        #raise NotImplementedError
