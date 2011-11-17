from collections import deque

GENESIS = '1'

class Tracer:

    def __init__(self, genealogy, tracePattern):
        self.genealogy = genealogy
        self.tracePattern = tracePattern

    def make_trace(self, startGenotype):
        trace = []
        queue = deque(startGenotype)
        while queue:
            baseNode = queue.popleft()
            relatedNodes = self.tracePattern.get_related_nodes(baseNode)
            for relatedNode in relatedNodes:
                if relatedNode and self.tracePattern.precondition_met(relatedNode):
                    trace.append((baseNode.ID, relatedNode.ID))
                    queue.append(relatedNode)
        return set(trace)

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

class MutRevTracePattern(TopDownTracePattern):
    
    def _init__(self, trackedMutation):
        self.trackedMutation = trackedMutation
        self.evaluator = MutationEvaluator()

    def precondition_met(node):
        if node.sequence_contains_mutation(mutation)\
        and self.evaluator.evaluate_effect_of_mutation(node, mutation) > 0:
            return True
