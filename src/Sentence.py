from .Atom import Atom
class Sentence:
    def __init__(self, sentence):
        sides = self.split_sentence(sentence)
        #lhs == left hand side
        self.lhs = sides[0]
        #rhs == right hand side
        self.rhs = sides[1]

    def split_sentence(self, sentence):
        """splits sentence string into lhs and rhs and atoms within each"""
        lhs = None
        rhs = None
        #Remove whitespace first
        clean_sentence = "".join(sentence.split())
        #split on '->'
        sides = clean_sentence.split("->")
        #a sentence could be a rule with a lhs and rhs
        #or a fact with only a lhs. Account for this
        num_of_sides = len(sides)
        if num_of_sides == 1:
            lhs = sides[0]
        elif num_of_sides == 2:
            lhs = sides[0]
            rhs = sides[1]
        else:
            print("Can only have 0 or 1 '->' in a sentence")

        #split each side into string atoms
        lhs_arr = lhs.split("^")
         #handle if right side is none
        rhs_arr =[]
        if rhs is None:
            rhs_arr = None
        else:
            rhs_arr = rhs.split("^")

        #for each side, turn string atoms into atom objects
        lhs_atomized = []
        rhs_atomized = []
        for atom in lhs_arr:
            lhs_atomized.append(Atom(atom))

        rhs_atomized = []
        if rhs is None:
            #sentence is a fact, ensure that rhs is None
            rhs_atomized = None
        else:
            for atom in rhs_arr:
                rhs_atomized.append(Atom(atom))
        return [lhs_atomized, rhs_atomized]


        # def __eq__(self, other):
        #     print("woot")
        #     return True

        # def __cmp__(self, other):
        #     print("woot")
        #     return True
        
        # def __repr__(self):
        #     return "rawr" 
        # def __str__(self):
        #     return "woot"
            # lhs = self.lhs[0].predicate + "(" + self.lhs[0].arguments + ")"

            # for atom in range(1, len(self.lhs)):
            #     lhs = lhs + "^" + atom.predicate + "(" + atom.arguments + ")"

            # return lhs