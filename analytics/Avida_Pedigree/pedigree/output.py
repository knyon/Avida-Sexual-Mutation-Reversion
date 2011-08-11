from pedigree.genealogy import *

GENESIS = '1'

class GraphvizFamilyTree:

    def write_genealogy_to_file(self, genealogy, filename = "genealogy.dot"):
        fo = open(filename, 'w')
        familyTree = self.make_family_tree(genealogy)
        fo.write(self.family_tree_to_output_string(familyTree))
        fo.close()


    def make_family_tree(self, genealogy):
        genesisGenotype = genealogy.genotypes[GENESIS]
        familyTree = set()
        queue = ExtndDeque(genesisGenotype)
        while queue:
            genotype = queue.popleft()
            children = genotype.children
            if children:
                familyTree = familyTree.union(self.make_relationship_set(genotype, children))
                queue.append(*children)
        return familyTree

    def make_relationship_set(self, parent, children):
        relationships = set()
        for child in children:
            relationship = "\t{0} -> {1};\n".format(parent.ID, child.ID)
            relationships.add(relationship)
        return relationships

    def family_tree_to_output_string(self, familyTree):
        head = "digraph FamilyTree {\n"
        body = ''.join(familyTree)
        end = "}"
        return head + body + end
