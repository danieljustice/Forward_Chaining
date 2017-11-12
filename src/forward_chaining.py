from .Sentence import Sentence
from .unify import (is_variable, unify)
from .Atom import Atom
import itertools

def parse_definite_clause(s):
    """Return the antecedents and the consequent of a definite clause."""
    if s.rhs is None:
        return [], s.lhs
    else:
        return s.lhs, s.rhs


def variables(side):
    args = {atom for atom in side}
    return {arg for arg in args if is_variable(arg)}

def instances(side):
    args = {atom for atom in side}
    return {arg for arg in args.arguments if not is_variable(arg)}

def subst(s, x):
    """Substitute the substitution s into the expression x.
    >>> subst({x: 42, y:0}, F(x) + y)
    (F(42) + 0)
    """
    if isinstance(x, list):
        return [subst(s, xi) for xi in x]
    elif isinstance(x, tuple):
        return tuple([subst(s, xi) for xi in x])
    else:
        return None
    # elif not isinstance(x, Expr):
    #     return x
    # elif is_var_symbol(x.op):
    #     return s.get(x, x)
    # else:
    #     return Expr(x.op, *[subst(s, arg) for arg in x.args])

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


def

