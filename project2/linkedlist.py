'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math


class Node:

    def __init__(self, value=None, next=None,tf =None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.tf = tf
        self.skipPointer = None
        self.score = 0.0


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            return traversal
        else:
            """ Write logic to traverse the linked list.
                To be implemented."""
            n = self.start_node
            # Start traversal from head, and go on till you reach None
            while n is not None:
                traversal.append(n.value)
                n = n.next
            return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            n = self.start_node
            while n is not None:
                traversal.append(n.value)
                n = n.skipPointer
            return traversal

    def add_skip_connections(self):
        print("Length of the term posting list")
        n_skips = math.floor(math.sqrt(self.length))
        if n_skips * n_skips == self.length:
            n_skips = n_skips - 1
        """ Write logic to add skip pointers to the linked list. 
            This function does not return anything.
            To be implemented."""
        #self.skip_length = (int)self.length/self.n_skips
        self.skip_length = (int)(round(math.sqrt(self.length), 0))
        print('Skip length = ' + str(self.skip_length))
        n1 = self.start_node
        n2 = self.start_node
        while n1 is not None and n2 is not None:
            count = 0
            while n2 is not None and count < self.skip_length:
                count += 1
                n2 = n2.next
                if n2 is None:
                    break
                #print("Node 2 doc value: " + str(n2.value))
            if n2 is not None:
                #print("current pointer: " + str(n1.value) + "skip pointer value: " + str(n2.value))
                n1.skipPointer = n2
                n1 = n2

        # while count < self.length:
        #     #count = count + 1
        #     for i in range(self.skip_length,0):
        #         if n2 is None:
        #             continue
        #         n2 = n2.next
        #         print(n2.next)
        #     if n2 is not None:
        #         n1.skipPointer = n2
        #         print(n1.skipPointer)
        #         n1 = n2
        #     count = count + self.skip_length

    def insert_at_end(self, value,score=None):
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
            To be implemented. """
        new_node = Node(value=value, tf = 1)
        if score is not None:
            new_node.score = score
        self.length += 1
        n = self.start_node

        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
            return

        elif self.start_node.value >= value:
            self.start_node = new_node
            self.start_node.next = n
            return

        elif self.end_node.value <= value:
            self.end_node.next = new_node
            self.end_node = new_node
            return

        else:
            while n.value < value < self.end_node.value and n.next is not None:
                n = n.next

            m = self.start_node
            while m.next != n and m.next is not None:
                m = m.next
            m.next = new_node
            new_node.next = n
            return

    def calculate_doc_score(self,total_docs,count_list):
        self.idf = total_docs/self.length
        #print("self.length = " + str(self.length) + "--self.idf = " + str(self.idf))
        n = self.start_node
        while n is not None:
            total_tokens = count_list[n.value]
            term_freq_score = n.tf /total_tokens
            #print("total token = " + str(total_tokens) + "--term_freq_score = " + str(term_freq_score))
            n.score = term_freq_score * self.idf
            #print(str(n.value) + ": score = " + str(n.score))
            n = n.next

    def increment_tf_docID(self,doc_id):
        n = self.start_node
        while n is not None:
            if n.value == doc_id:
                n.tf = n.tf + 1
                return doc_id
            n = n.next
        return -1

    def print_linklist(self):
        print("-------Printing linkist------")
        n = self.start_node
        s = ""
        while n is not None:
            s= s + str(n.value)+ ',' + str(n.tf) + '-->'
            n = n.next
        print(s)
                
