import unittest
import unittest.mock
from unittest.mock import MagicMock
from ..src.Sentence import Sentence
from ..src.Atom import Atom
from ..src.forward_chaining import (parse_definite_clause, 
                                    variables,
                                    instances,
                                    subst,
                                    fol_fc_ask)

class TestFCClass(unittest.TestCase):
    def test_fc(self):
        meat_rule = Sentence("Meat(x)->Is(x)")
        assert meat_rule.rhs == [Atom("Is(x)")]
        meat_fact = Sentence("Meat(Tasty)")
        assert meat_fact.rhs is None
        KB = [meat_rule]

        print(fol_fc_ask(KB,meat_fact, Atom("Is(Tasty)")))
        assert 1 ==fol_fc_ask(meat_rule,meat_fact, Atom("Is(Tasty)"))
        