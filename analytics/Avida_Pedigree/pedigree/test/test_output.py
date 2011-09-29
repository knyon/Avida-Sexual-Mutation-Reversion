import unittest
import os
from pedigree.output import *
from pedigree.genealogy import *

simpleDetailDump = '''\
5 4,3 Md1e Swp0-0 heads_sex e
4 3,2 Mc1d Swp0-0 heads_sex d
3 2,1 Mb1c Swp0-0 heads_sex c
2 1,1 Ma1b Swp0-0 heads_sex b
1 (none)  heads_sex a'''

#class Test_Genealogy(unittest.TestCase):

    #def test_print_genealogy(self):
        #genealogy = GenealogyMaker.make_genealogy_from_string(simpleDetailDump)
        #treePrinter = GraphvizFamilyTree()
        #treePrinter.write_genealogy_to_file(genealogy)
        #self.assertTrue(os.path.exists('genealogy.dot'))

    #def tearDown(self):
        #if os.path.exists('genealogy.dot'):
            #os.remove('genealogy.dot')
