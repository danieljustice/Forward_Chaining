import re
import copy
import sys

class Atom:
    """The atom of FOL, includes the predicate and array of Arguments"""
    def __init__(self, atom):
        parts = self.split_atom(atom)
        self.predicate = parts[0]
        self.arguments = parts[1]

    def split_atom(self, atom):
        """Takes the atom string and splits it into its components:
        a predicate and array of arguments"""
        #remove all white spaces
        atom = "".join(atom.split())
        #expected to have only 1 pair of '()', remove the ')'
        atom = atom.replace(")", "")
        #since there is on 1 pair of '()', 
        #the predicate is to the right of the '('
        #and the arguments are to the left of the '('
        atom = atom.split("(")
        predicate = atom[0]
        arguments = atom[1].split(",")

        return predicate, arguments

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __cmp__(self, other): 
        print("woot")
        return self.__dict__ == other.__dict__

    def __str__(self):
        string = self.predicate + "("
        string = string + self.arguments[0]
        for i in range(1, len(self.arguments)):
            string = string + "," + self.arguments[i]
        string = string + ")"
        return string



class Sentence:
    def __init__(self, sentence = None):
        
        if(sentence is None):
            self.lhs = None
            self.rhs = None
        else:
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


    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __cmp__(self, other): 
        print("woot")
        return self.__dict__ == other.__dict__

    def __str__(self):
        string = self.lhs[0].__str__()
        for i in range(1, len(self.lhs)):
            string = string + "^" + self.lhs[i].__str__()
        if(self.rhs is not None):
            string = string + "->" + self.rhs[0].__str__()
        return string



def unify(atom1, atom2):
    compatible = compatible_atoms(atom1, atom2)
    if not compatible:
        return None
    substitutions = {}
    for a1, a2 in zip(atom1.arguments, atom2.arguments):
        if is_variable(a1):
            if a1 in substitutions:
                return None
            else:
                substitutions[a1] = a2
        elif a1 != a2:
            #if not a variable, it is a constant and return None if they dont match
            return None
    return substitutions

def compatible_atoms(atom1, atom2):
    have_same_num_of_args = (len(atom1.arguments) == len(atom2.arguments))
    have_same_predicates = (atom1.predicate == atom2.predicate)
    atom2_has_no_variables = len([arg for arg in atom2.arguments if arg[0].isupper()]) == len(atom2.arguments)
    
    fail = not (have_same_num_of_args and have_same_predicates and atom2_has_no_variables)
    
    if fail:
        return False
    else:
        return True

def is_variable(arg):
    return not arg[0].isupper()



def substitutions(rule, fact):
    """takes in a fact and a rule, returns all usable subs"""
    atom_pairs =  [(atom1, fact.lhs[0]) for atom1 in rule.lhs] 
    # F efficiency
    result = {}
    temp = [unify(atom1, atom2) for atom1, atom2 in atom_pairs if unify(atom1, atom2) is not None]
    for d in temp:
        result.update(d)
    return result


def subst(theta, rule):
    #subst in on the left side
    for atom in rule.lhs:
        for index in range(0, len(atom.arguments)):
            arg = atom.arguments[index]
            if arg in theta.keys():
                atom.arguments[index] = theta[arg]
    #subst in on the right side
    for atom in rule.rhs:
         for index in range(0, len(atom.arguments)):
            arg = atom.arguments[index]
            if arg in theta.keys():
                atom.arguments[index] = theta[arg]
    return rule



def fire(Rules, Facts, fact, infers):
    
    Facts.append(fact)
    addedFacts = []
    addedFacts.append(fact)
    while True:
        new = []    
        tempRules = copy.deepcopy(Rules)
        infered = []
        for rule in tempRules:
            for fac in Facts:
                theta = substitutions(rule, fac)         
                if len(theta) > 0:
                    newSentence = subst(theta, Sentence(rule.__str__()))
                    #if there are no variables, there are only instances, this is a fact
                    using_new_facts = False
                    for atom in newSentence.lhs:    
                        if atom in [fact.lhs[0] for fact in addedFacts]:
                            using_new_facts = True
                            
                        if any(atom == fact.lhs[0] for fact in Facts + new):
                            valid = True
                        else:
                            valid = False
                            break

                    if valid and using_new_facts:
                        newFact = Sentence()
                        newFact.lhs = newSentence.rhs
                        if newFact not in infered:
                            infers.append("Inferred: " + newFact.__str__())
                            infered.append(newFact)
                            if(newFact not in Facts and newFact not in new):                                
                                new.append(newFact)
                    
                    else:
                        tempRules.append(newSentence)
        if not new:
            break
        
        Facts.extend(new)
        addedFacts.clear()
        addedFacts.extend(new)
        tempRules.clear()
    return Facts, infers

    
    
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
