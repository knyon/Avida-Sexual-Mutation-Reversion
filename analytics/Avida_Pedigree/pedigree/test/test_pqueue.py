import unittest
from pedigree.pqueue import PedigreeQueue

class Test_PedigreeQueue(unittest.TestCase):

    def setUp(self):
        self.someList = [1,2,3]

    def test_initializing_with_multiple_objects(self):
        somePedigreeQueue = PedigreeQueue(*self.someList)
        for obj in self.someList:
            self.assertEquals(obj, somePedigreeQueue.popleft())
    
    def test_adding_multiple_objects_to_preinitialized_queue(self):
        somePedigreeQueue = PedigreeQueue()
        somePedigreeQueue.append(*self.someList)
        for obj in self.someList:
            self.assertEquals(obj, somePedigreeQueue.popleft())
