from Sentence import Sentence
# from . import Atom
from incremental import (parse_definite_clause, 
                                    variables,
                                    instances,
                                    subst,
                                    fol_fc_ask,
                                    fire,
                                    substitutions)
import sys

    
    
if __name__ == '__main__':
    text_file = sys.argv[1]
    logic_file = open(text_file, "r")
    logic_sentences = logic_file.read().splitlines()

    Rules = []
    Facts = []
    end_sentences = []
    for line in logic_sentences:
        if "->" in line:
            Rules.append(Sentence(line))
        elif "PROVE" in line:
            goal = line[5:]
            goal_sentence = Sentence(goal)
            if goal_sentence in Facts:
                end_sentences.insert(0, "True")
                end_sentences.append("Proved: " + goal_sentence.__str__())
            else:
                end_sentences.insert(0, "False")
        else:
            fact = Sentence(line)
            Facts, end_sentences = fire(Rules, Facts, fact, end_sentences)

    for line in end_sentences:
        print(line)