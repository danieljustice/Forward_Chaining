import unittest
import unittest.mock
from unittest.mock import MagicMock
from ..src.unify import compatible_atoms
from ..src.unify import is_variable
from ..src.Atom import Atom

class TestUnifyClass(unittest.TestCase):
    def test_first_fail(self):
        assert True == compatible_atoms(Atom("Meat(x)"), Atom("Meat(Chicken)"))

    def test_failed_diff_predicates(self):
        atom1 = Atom("Meat(x)")
        atom2 = Atom("Fruit(Banana)")    
        assert False == compatible_atoms(atom1, atom2)

    def test_failed_diff_num_args(self):
        atom1 = Atom("Meat(x,y)")
        atom2 = Atom("Fruit(Banana)")    
        assert False == compatible_atoms(atom1, atom2)

    def test_is_variable(self):
        assert True == is_variable("x")
        assert False == is_variable("X")
        assert True == is_variable("xX")
        assert False == is_variable("Xx")
        