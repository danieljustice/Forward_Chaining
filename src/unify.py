from Atom import Atom
import re

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