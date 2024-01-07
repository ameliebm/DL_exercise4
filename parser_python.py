from lark import Lark, Transformer, tree


# Load the grammar
grammar = r"""
    start: disjunction

    disjunction: conjunction
        | disjunction "or" conjunction

    conjunction: atom
        | conjunction "and" atom

    atom: "not" atom
        | "(" disjunction ")"
        | VAR

    VAR: /[a-z]/

    %ignore /\s+/
"""



# Define a transformer to process the parsed tree
class PropositionalLogicTransformer(Transformer):
    def VAR(self, token):
        return ('VAR', token[0])

    def not_(self, tokens):
        return ('NOT', tokens[0])

    def and_(self, tokens):
        return ('AND', tokens[0], tokens[1])

    def or_(self, tokens):
        return ('OR', tokens[0], tokens[1])
    
# Test the parser
formula = "(p or q)"
# Create the Lark parser
parser = Lark(grammar, start='disjunction')
parsed_tree = parser.parse(formula)
#print(parsed_tree)
#print(parsed_tree.pretty())

#transformer = PropositionalLogicTransformer()
#parsed_formula = transformer.transform(parsed_tree)

# Visualize and save the parse tree as a PNG image
tree_png = tree.pydot__tree_to_png(parsed_tree, "parse_tree.png")

#lark.tree.pydot__tree_to_png()
#transformer = PropositionalLogicTransformer()
#parsed_formula = transformer.transform(parsed_tree)
#print(parsed_formula)