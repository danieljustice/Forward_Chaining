from .Atom import Atom
class Sentence:
    def __init__(self, sentence):
        sides = self.Split_Sentence(sentence)
        self.lhs = sides[0]
        self.rhs = sides[1]

    def Split_Sentence(self, sentence):
        lhs = None
        rhs = None
        #Remove whitespace first
        clean_sentence = "".join(sentence.split())
        #split on '->'
        sides = clean_sentence.split("->")
        num_of_sides = len(sides)
        if num_of_sides == 1:
            lhs = sides[0]
        elif num_of_sides == 2:
            lhs = sides[0]
            rhs = sides[1]
        else:
            print("Can only have 0 or 1 '->' in a sentence")

        lhs_arr = lhs.split("^")
        rhs_arr = rhs.split("^")
    
        lhs_atomized = []
        rhs_atomized = []
        for atom in lhs_arr:
            lhs_atomized.append(Atom(atom))

        rhs_atomized = []
        if rhs is None:
            rhs_atomized = None
        else:
            for atom in rhs_arr:
                rhs_atomized.append(Atom(atom))
        return [lhs_atomized, rhs_atomized]