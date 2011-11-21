from collections import deque

GENESIS = '1'

class Tracer:

    def __init__(self, genealogy, tracePattern):
        self.genealogy = genealogy
        self.tracePattern = tracePattern

    def make_trace(self, startGenotype):
        statusCount = 0
        trace = []
        markedNodes = []
        queue = deque()
        queue.append(startGenotype.ID)
        while queue:
            baseNode = self.genealogy.genotypes[queue.popleft()]
            relatedNodeIDs = self.tracePattern.get_related_nodes(baseNode)
            for nodeID in relatedNodeIDs:
                relatedNode = self.genealogy.genotypes[nodeID]
                if not relatedNode.isMarked() and self.tracePattern.precondition_met(relatedNode):
                    trace.append((baseNode.ID, relatedNode.ID))
                    queue.append(relatedNode.ID)
                    relatedNode.mark()
                    markedNodes.append(relatedNode.ID)
            statusCount += 1
            if statusCount % 1000 == 0:
                print("I've gone {} times throught the queue".format(statusCount))
                print("The queue has {} members".format(len(queue)))
        self.unmarkNodes(markedNodes)
        return set(trace)

    def unmarkNodes(self, markedNodes):
        for node in markedNodes:
            self.genealogy[node].unmark()

class TopDownTracePattern:
    
    def get_related_nodes(self, baseNode):
        return baseNode.children

    def precondition_met(self, node):
        return True

class BottomUpTracePattern:
    
    def get_related_nodes(self, baseNode):
        return baseNode.parents

    def precondition_met(self, node):
        return True

class SubMutTDTracePattern(TopDownTracePattern):

    def __init__(self, trackedMutation):
        self.trackedMutation = trackedMutation

    def precondition_met(self, node):
        return node.sequence_contains_mutation(self.trackedMutation)

class SubMutBUTracePattern(BottomUpTracePattern):

    def __init__(self, trackedMutation):
        self.trackedMutation = trackedMutation

    def precondition_met(self, node):
        return node.sequence_contains_mutation(self.trackedMutation)
