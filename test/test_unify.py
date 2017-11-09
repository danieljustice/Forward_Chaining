import unittest
import unittest.mock
from unittest.mock import MagicMock
from ..src.unify import compatible_atoms
from ..src.unify import is_variable
from ..src.unify import unify
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
        
    def test_unify_single_arg(self):
        test_sub = {}
        test_sub["x"] = "Steak"
        atom1 = Atom("Meat(x)")
        atom2 = Atom("Meat(Steak)")
        assert test_sub == unify(atom1, atom2)

    def test_unify_multi_arg(self):
        test_sub = {}
        test_sub["x"] = "Steak"
        test_sub["y"] = "Lamb"
        atom1 = Atom("Meat(x,y)")
        atom2 = Atom("Meat(Steak,Lamb)")
        assert test_sub == unify(atom1, atom2)

    def test_unify_diff_pred(self):
        atom1 = Atom("Meat(x)")
        atom2 = Atom("Woot(Steak)")
        assert None == unify(atom1, atom2)

    def test_unify_non_fact_in_atom2(self):
        atom1 = Atom("Meat(x)")
        atom2 = Atom("Meat(steak)")
        assert None == unify(atom1, atom2)
