from pedigree.genotype import Genotype
from pedigree.parsing import DetailParser
from Queue import Queue

class GenealogyMaker:
    ##'''Class with only static methods used in creating a genealogy from a
    ##detail dump. A detail dump may be either a detail dump file created by
    ##Avida or a string, which is useful in testing.'''

    def make_genealogy_from_file(self, fileName, domID):
        detailDump = open(fileName,"r")
        return self.build_genealogy(detailDump.readlines(), domID)

    def make_genealogy_from_string(self, inputString, domID):
        detailDump = inputString.split('\n')
        return self.build_genealogy(detailDump, domID)

    ## add the geneome IDs for children and grand children from a given starting point (assume final dominant)
    ## Start with given genome and proceed in a BFS fashion
    def add_children_in_lineage(self, genealogy, genome):
        q = Queue()
        q.put(genome)
        q.put(None)

        generation = 1
        width = 0
        total = 0

        fml = 0

        while not q.empty():
            ## meaty part of the BFS, get the genotype object and add its id to its parent's children
            c = q.get()
            if(c != None):
                curr = genealogy.get_genome(c)
                if (not curr.isMarked() and curr.ID != "1"):
                    parents = curr.parents

                    for rent in parents:
                        p = genealogy.get_genome(rent)
                        if (not p.isMarked()):
                            q.put(rent)
                        p.add_child(curr.ID)
                    
                    curr.mark()
                    width += 1
                
                ## cycle handeling -- should never every happen
                else:
                    if(curr.ID != "1"):
                        ##print "FML!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                        fml += 1

            ##Marker has found the end of a generation
            ##spit out some interesting stats about what we found
            elif (c == None ):
                print "Pocessed generation {0:d} containing {1:d} members".format(generation, width)

                ## keep house
                total += width
                width = 0
                generation += 1

                ## add a new marker for the next generation  -- assuming there is one
                if(not q.empty()):
                    q.put(None) 

        print "Processed {0:d} generations with {1:d} total genomes".format(generation, total)
        print "FML count: " + str(fml)
        return None
        
        ##'''Build and return a Genealogy object by adding Genotypes parsed from
        ##a detail dump'''
    def build_genealogy(self, detailDump, dom_genome_ID):
        parser = DetailParser()
        genealogy = Genealogy()
        count = 0
        for i in range(0,len(detailDump)):
            if(i % 1000 == 0):
                print "Processing line {:d}".format(i)

            ## everything before pos 26 is junk
            if i > 26:
                if detailDump[i] != "":
                    details = parser.process_line(detailDump[i])
                    if details:
                        try:
                            genealogy.add_genotype(details)
                        except:
                            print "DOh!!!"
                            print details
                            print detailDump[i]
                            genealogy.add_genotype(details)
                            

        print "FINISHED LOADING!!! HAPPY DANCE TIME!!!"

        self.add_children_in_lineage(genealogy, dom_genome_ID)

        #raw_input("****If you can read this then good things have transpired!****")
        
        return genealogy


class Genealogy():
    ##'''Class to contain all of the Genotype objects.'''

    def __init__(self):
        self.genotypes = {}

    def __getitem__(self, i):
        return self.genotypes[i]

    def has_genotype_id(self, genotypeID):
        return genotypeID in self.genotypes.keys()

    def get_genome(self, genomeID):
        if genomeID in self.genotypes:
            return self.genotypes[genomeID]
        else:
            return None

    def add_genotype(self, details):
        '''Add new genotype to the genealogy'''
        #key = details[0]
        self.genotypes[details[0]] = Genotype(*details)

    def unmark_all_genotypes(self):
        for genotype in self.genotypes.values():
            genotype.unmark()
            

##class GenotypeRelationshipTool():

##    def create_relationships_between_genotypes_in_genealogy(self, genealogy):
##        ##'''For all genotypes, add their related Genotype objects (children and
##        ##parents)'''
##        print "Creating relationships"
##        for genotype in genealogy.genotypes.values():
##            #this shouldn't be needed -- we already know the parents!!!
##            #self.add_parent_objects_to_genotype(genotype, genealogy)
##            self.add_child_to_parent_genotype(genotype)

##    def add_parent_objects_to_genotype(self, genotype, genealogy):
##        ##'''Genotype object initially created with just the parents' IDs.
##        ##Replace them with the parents' Genotype objects'''
##        for idx,parentID in enumerate(genotype.parents):
##            if parentID and genealogy.has_genotype_id(parentID):
##                genotype.parents[idx] = genealogy.genotypes[parentID]
##            else:
##                genotype.parents[idx] = None

##    def add_child_to_parent_genotype(self, genotype):
##        ##'''Add the genotype to it\'s parent'''
##        for parent in genotype.parents:
##            if parent:
##                parent.add_child(genotype)

