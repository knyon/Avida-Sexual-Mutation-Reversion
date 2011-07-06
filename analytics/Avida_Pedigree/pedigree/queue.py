from collections import deque

class PedigreeQueue(deque):
    '''Extension of the deque collection that allows for
    appending multiple items at once'''

    def __init__(self, *items):
        super(pedigree_queue, self).__init__(self)
        self.append(*items)

    def append(self, *items):
        for i in items:
            super(pedigree_queue, self).append(i)
