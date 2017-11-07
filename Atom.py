class Atom:
    """The atom of FOL, includes the predicate and array of Arguments"""
    def __init__(self, atom):
        #self.predicate = predicate
        #copy argument list to self arguments
        #self.arguments = arguments[:]
        parts = self.Split_Atom(atom)
        self.predicate = parts[0]
        self.arguments = parts[1]

    def Split_Atom(self, atom):
            


        return predicate, arguments