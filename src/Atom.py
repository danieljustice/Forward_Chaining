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
        print("woot1")
        return self.__dict__ == other.__dict__

    def __cmp__(self, other): 
        print("woot")
        return self.__dict__ == other.__dict__
