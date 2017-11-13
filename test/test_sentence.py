import unittest
import unittest.mock
from unittest.mock import MagicMock
from ..src.Sentence import Sentence
from ..src.Atom import Atom


class TestSentenceClass(unittest.TestCase):
    def test_init_fact(self):
        meat_fact = Sentence("Meat(Tasty)")
        assert meat_fact is not None
    
    def test_init_rule(self):
        meat_rule = Sentence("Meat(x)->Is(Tasty)")
        assert meat_rule is not None

    def test_sentence_lhs(self):
        meat_rule = Sentence("Meat(x)->Is(Tasty)")
        assert meat_rule.lhs == [Atom("Meat(x)")]
        fruit_rule = Sentence("Fruit(x) ^ Fruit(y) -> Nom(Rawr)")
        assert fruit_rule.lhs == [Atom("Fruit(x)"), Atom("Fruit(y)")]

    def test_sentence_rhs(self):
        meat_rule = Sentence("Meat(x)->Is(Tasty)")
        assert meat_rule.rhs == [Atom("Is(Tasty)")]
        meat_fact = Sentence("Meat(Tasty)")
        assert meat_fact.rhs is None

    def test_eq(self):
        meat_fact1 = Sentence("Meat(Tasty)->Is(Tasty)")
        meat_fact2 = Sentence("Meat(Tasty)")
        assert meat_fact1.lhs == meat_fact2.lhs
        assert meat_fact1.rhs != meat_fact2.rhs
        

    # def test_str(self):
    #     meat_rule = Sentence("Meat(x)->Is(Tasty)")
    #     assert meat_rule.__str__() == "awoot"