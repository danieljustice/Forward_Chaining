import unittest
import unittest.mock
from unittest.mock import MagicMock
from ..src.Sentence import Sentence
from ..src.Atom import Atom
from ..src.forward_chaining import (parse_definite_clause, 
                                    variables,
                                    instances,
                                    subst,
                                    fol_fc_ask,
                                    fire,
                                    substitutions)

class TestFCClass(unittest.TestCase):
    # def test_fc(self):
    #     meat_rule = Sentence("Meat(x)->Is(x)")
    #     assert meat_rule.rhs == [Atom("Is(x)")]
    #     meat_fact = Sentence("Meat(Tasty)")
    #     assert meat_fact.rhs is None
    #     KB = [meat_rule]

    #     print(fol_fc_ask(KB,meat_fact, Atom("Is(Tasty)")))
    #     assert 1 ==fol_fc_ask(meat_rule,meat_fact, Atom("Is(Tasty)"))


    # def test_fire(self):
    #     meat_rule = Sentence("Meat(x) ^ Fruit(y)->Tasty(x, y)")
    #     meat_fact = Sentence("Meat(Steak)")
    #     fruit_fact = Sentence("Fruit(Steak)")
    #     assert fire([meat_rule], [fruit_fact], meat_fact) == True

    def test_substitutions(self):
        meat_rule = Sentence("Meat(x)^Fruit(y)->Tasty(x,y)")
        meat_fact = Sentence("Meat(Steak)")
        fruit_fact = Sentence("Fruit(Banana)")
        assert substitutions(meat_rule, meat_fact) == {'x': 'Steak'}
        assert substitutions(meat_rule, fruit_fact) == {'y': 'Banana'}
        sub = subst({'x': 'Steak'}, meat_rule)
        man_sub = Sentence("Meat(Steak)^Fruit(y)->Tasty(Steak,y)")
        assert sub.lhs == man_sub.lhs
        assert sub.rhs == man_sub.rhs