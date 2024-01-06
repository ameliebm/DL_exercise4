from lark import Lark, Transformer

grammar = r"""
    start: disjunction

    disjunction: conjunction
        | disjunction "or" conjunction

    conjunction: atom
        | conjunction "and" atom

    atom: "not" atom
        | "(" disjunction ")"
        | NAME

    %import common.CNAME -> NAME
    %import common.WS
    %ignore WS
"""
class LogicTransformer(Transformer):
    def disjunction(self, items):
        if len(items) == 1:
            return items[0]
        print("Disjunction:", items)
        return ("or", items[0], items[2])

    def conjunction(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            print("Conjunction:", items)
            return ("and", items[0], items[2])
        else:
            raise ValueError("Invalid conjunction structure")

    def atom(self, items):
        if len(items) == 1:
            return items[0]
        elif items[0] == "not":
            return ("not", items[1])
        else:
            return items[1]
        
logic_parser = Lark(grammar, parser='lalr', transformer=LogicTransformer())

def parse_formula(formula):
    return logic_parser.parse(formula)

formula = "A and B"
parsed = parse_formula(formula)
print("Parsed Logical Expression:", parsed)