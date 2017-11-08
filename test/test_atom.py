import unittest
import unittest.mock
from unittest.mock import MagicMock
from ..src.Atom import Atom


class TestAtomClass(unittest.TestCase):
    def test_init(self):
        atom = Atom("Meat(x)")
        assert atom is not None

    
    def test_arguments(self):
        #test that we get 1 argument "x" back in an array
        meat_atom = Atom("Meat(x)")
        assert meat_atom.arguments == ["x"]
        #test for white space confusion
        meat_atom = Atom("  \rMeat \n (     x   )   \n")
        assert meat_atom.arguments == ["x"]
        #test for multiple arguments
        fruit_atom = Atom("Fruit(Banana, Grape)")
        assert fruit_atom.arguments == ["Banana", "Grape"]

    def test_predicate(self):
        meat_atom = Atom("Meat(x)")
        assert meat_atom.predicate == "Meat"