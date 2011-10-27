from collections import deque

GENESIS = '1'

class Tracer:
    def __init__(self, genealogy):
        self.genealogy = genealogy

    def make_trace(self, startGenotype):
        trace = []
        queue = ExtndDeque(startGenotype)
        while queue:
            node = queue.popleft()
            relatedNodes = self.getRelatedNodes(baseNode)
            for node in relatedNodes:
                if self.precondition_met(node):
                    trace.append((baseNode.ID, relatedNode.ID))
                    queue.append(relatedNode)
        return set(trace)

    def precondition_met(self, baseNode, relatedNode):
        return True #No precondition

    def get_related_nodes(self, baseNode):
        pass

class TopDownTracer(Tracer):
    
    def get_related_nodes(self, baseNode):
        return baseNode.children

class BottomUpTracer(Tracer):
    
    def get_related_nodes(self, baseNode):
        return baseNode.parents

class SubMutTDTracer(TopDownTracer):

    def __init__(mutationToTrace):
        self.tracedMutation = mutationToTrace

    def precondition_met(node):
        return node.sequence_contains_mutation(mutation)

class SubMutBUTracer(BottomUpTracer):

    def __init__(mutationToTrace):
        self.tracedMutation = mutationToTrace

    def precondition_met(node):
        return node.sequence_contains_mutation(mutation)

class ExtndDeque(deque):
    '''Extension of the deque collection that allows for appending multiple
    items at once'''

    def __init__(self, *items):
        super(ExtndDeque, self).__init__(self)
        self.append(*items)

    def append(self, *items):
        for i in items:
            super(ExtndDeque, self).append(i)
