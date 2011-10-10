from collections import deque

GENESIS = '1'

class Tracer:
    
    def __init__(self, genealogy):
        self.genealogy = genealogy

    def make_trace(self, startID=GENESIS):
        origin = self.genealogy.genotypes[startID]
        trace = []
        queue = ExtndDeque(origin)
        while queue:
            parent = queue.popleft()
            children = parent.children
            for child in children:
                trace.append((parent.ID, child.ID))
                queue.append(child)
        return set(trace)


#I really want to make this DRYer, not sure how :\
class SubMutTracer(Tracer):

    def make_trace(self, startID):
        origin = self.genealogy.genotypes[startID]
        mutation = origin.subMutA
        trace = []
        queue = ExtndDeque(origin)
        while queue:
            parent = queue.popleft()
            children = parent.children
            for child in children:
                if child.sequence_contains_mutation(mutation):
                    trace.append((parent.ID, child.ID))
                    queue.append(child)
        return set(trace)

class ExtndDeque(deque):
    '''Extension of the deque collection that allows for appending multiple
    items at once'''

    def __init__(self, *items):
        super(ExtndDeque, self).__init__(self)
        self.append(*items)

    def append(self, *items):
        for i in items:
            super(ExtndDeque, self).append(i)
