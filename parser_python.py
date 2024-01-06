from lark import Lark, Transformer

# Load the grammar from the file
with open("propositional_logic.lark.txt", "r") as f:
    grammar = f.read()



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
formula = "(p and q) or not r"
# Create the Lark parser
parser = Lark(grammar, start='expr')
parsed_tree = parser.parse(formula)
print(parsed_tree)
print(parsed_tree.pretty())
lark.tree.pydot__tree_to_png()
#transformer = PropositionalLogicTransformer()
#parsed_formula = transformer.transform(parsed_tree)
#print(parsed_formula)