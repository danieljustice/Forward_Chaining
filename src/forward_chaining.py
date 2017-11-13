from Sentence import Sentence
from unify import (is_variable, unify)
from Atom import Atom
import itertools
import copy

# Rules = []
# Facts = []


def parse_definite_clause(s):
    """Return the antecedents and the consequent of a definite clause."""
    if s.rhs is None:
        return [], s.lhs
    else:
        return s.lhs, s.rhs


def variables(side):
    # print("This is a side")
    # print(side[0].predicate)
    # for item in side:
    #     for argument in item.arguments:
    #         print(argument)
    # atoms = side[:]
    
    # print([arg for arg in (atom.arguments for atom in atoms)])
    # return {atom.arguments for atom in atoms if is_variable(atom.arguments)}

    variable_set = set()
    for item in side:
        for argument in item.arguments:
            # print(argument)
            if(is_variable(argument)):
                variable_set.add(argument)
    return variable_set

def instances(side):
    instance_set = set()
    for item in side:
        for argument in item.arguments:
            # print(argument)
            if(not is_variable(argument)):
                instance_set.add(argument)
    return instance_set
def subst(theta, rule):
    #subst in on the left side
    #print("Theta:")
    #for i in theta:
        #print (i + ":" +  theta[i])
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
    
    # """Substitute the substitution s into the expression x.
    # >>> subst({x: 42, y:0}, F(x) + y)
    # (F(42) + 0)
    # """
    # if isinstance(x, list):
    #     # print("is a list")
    #     # print([xi for xi in x])
    #     return [subst(s, xi) for xi in x]
    # elif isinstance(x, tuple):
    #     return tuple([subst(s, xi) for xi in x])
    # elif type(x) is not Atom and is_variable(x):
    #     # print(type(x))
    #     return s.get(x, x)
    # else:
    #     return x
    # # elif not isinstance(x, Expr):
    # #     return x
    # # elif is_var_symbol(x.op):
    # #     return s.get(x, x)
    # # else:
    # #     return Expr(x.op, *[subst(s, arg) for arg in x.args])

def fol_fc_ask(KB, fact, alpha):
    def enum_subst(p, fact):
        query_vars = variables(p)       #list({v for clause in p for v in variables(clause)})
        facts = instances(fact)
        for assignment_list in itertools.product(facts, repeat=len(query_vars)):
            theta = {x: y for x, y in zip(query_vars, assignment_list)}
            yield theta

    while True:
        new = []
        for rule in KB:
            p, q = parse_definite_clause(rule)  
            for theta in enum_subst(p, fact):
                if set(subst(theta, p)).issubset(set(KB)):
                    q_ = subst(theta, q)
                    if all([unify(x, q_) is None for x in KB + new]):
                        new.append(q_)
                        phi = unify(q_, alpha)
                        if phi is not None:
                            return phi
        
        if not new:
            break
        for clause in new:
            KB.append(clause)
    return None


def enum_subst(p, fact):
    return None
#     # query_vars = variables(p)       #list({v for clause in p for v in variables(clause)})
#     # facts = instances(fact.lhs)
#     # for assignment_list in itertools.product(facts, repeat=len(query_vars)):
#     #     theta = {x: y for x, y in zip(query_vars, assignment_list)}
#     #     yield theta



def fire(Rules, Facts, fact, infers):
    # print("New Fact: " + fact.__str__())
    
    Facts.append(fact)
    while True:
        new = []    
        tempRules = copy.deepcopy(Rules)
        for rule in tempRules:
            for fac in Facts:
                # print("Fact: " + fac.__str__())
                theta = substitutions(rule, fac)         
                # print( rule.__str__() + " and " + fac.__str__() + " subs to: " + theta.__str__())
                if len(theta) > 0:
                    newSentence = subst(theta, rule)
                    #if there are no variables, there are only instances, this is a fact
                    # print(newSentence.__str__())
                    for atom in newSentence.lhs:
                        if any(atom == fact.lhs[0] for fact in Facts + new):
                            valid = True
                        else:
                            valid = False
                            break

                    if valid:
                        newFact = Sentence()
                        newFact.lhs = newSentence.rhs
                        infers.append("Inferred: " + newFact.__str__())
                        if(newFact not in Facts and newFact not in new):
                            new.append(newFact)
                        
                    else:
                        tempRules.append(newSentence)
        if not new:
            break
        Facts.extend(new)
        # print("\nNew was added \n")
        # for Sent in Rules:
        #     print(Sent.__str__())
        #     print("")
    # for fact in Facts:
    #     print(fact.lhs[0].predicate + "(" + ''.join(fact.lhs[0].arguments) + ")")

    return Facts, infers

def substitutions(rule, fact):
    """takes in a fact and a rule, returns all usable subs"""
    atom_pairs =  [(atom1, fact.lhs[0]) for atom1 in rule.lhs] 
    # F efficiency
    result = {}
    temp = [unify(atom1, atom2) for atom1, atom2 in atom_pairs if unify(atom1, atom2) is not None]
    for d in temp:
        result.update(d)
    return result

#takes in fact
#adds fact to fact list
#goes through each rule
#   Goes through each fact and attempts to unify it with each atom in a lhs rule
#       if a unify succeeded, add to fact list, substitute
#           if full of instances, add rhs to facts
#            if not full of instances, add back to rules
        