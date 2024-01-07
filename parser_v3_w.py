from lark import Lark, Transformer, tree


# Load the grammar
grammar = r"""
    start: formula
    ?formula: prop_equivalence

    ?prop_equivalence: prop_implication (EQUIVALENCE prop_implication)*
    ?prop_implication: prop_or (IMPLY prop_or)*
    ?prop_or: prop_and (OR prop_and)*
    ?prop_and: prop_not (AND prop_not)*
    ?prop_not: NOT* modal

    ?modal: prop_atom
            | BOX* prop_parenthesis
            | DIAMOND* prop_parenthesis

    ?prop_parenthesis: prop_atom
            | LEFT_P formula RIGHT_P
    ?prop_atom: atom
    atom: SYMBOL_NAME


    NOT: "!"
    OR: "|"
    AND: "&"
    IMPLY : "->"
    EQUIVALENCE : "<->"
    BOX : "□"
    DIAMOND : "◇"
    LEFT_P : "("
    RIGHT_P : ")"

    SYMBOL_NAME: FIRST_SYMBOL_CHAR _SYMBOL_1_BODY _SYMBOL_1_TAIL
           | FIRST_SYMBOL_CHAR _SYMBOL_2_BODY
           | DOUBLE_QUOTES _SYMBOL_3_BODY DOUBLE_QUOTES

    _SYMBOL_QUOTED: DOUBLE_QUOTES _SYMBOL_3_BODY DOUBLE_QUOTES
    _SYMBOL_1_BODY: /[a-zA-Z0-9_\-]+/
    _SYMBOL_1_TAIL: /[a-zA-Z0-9_]/
    _SYMBOL_2_BODY: /[a-zA-Z0-9_]*/
    _SYMBOL_3_BODY: /[ -!#-~]+?/

    DOUBLE_QUOTES: "\""
    FIRST_SYMBOL_CHAR: /[a-z_]/


%ignore /\s+/
"""


# Define a transformer to process the parsed tree
class ModalLogicTransformer(Transformer):
    def SYMBOL_NAME(self, token):
        return ('SYMBOL_NAME', token[0])

    def NOT(self, tokens):
        return ('NOT', tokens[0])

    def AND(self, tokens):
        return ('AND', *tokens)

    def OR(self, tokens):
        return ('OR', *tokens)
    
    def IMPLY(self, tokens):
        return ('IMPLY', tokens[0], tokens[1])
    
    def EQUIVALENCE(self, tokens):
        return ('EQUIVALENCE', tokens[0], tokens[1])
    
    def BOX(self, tokens):
        return ('BOX', tokens[0])
    
    def DIAMOND(self, tokens):
        return ('DIAMOND', tokens[0])
    
# Test the parser
formula = "(◇p & q)"
# Create the Lark parser
parser = Lark(grammar, start='formula')
parsed_tree = parser.parse(formula)
print(parsed_tree.pretty())
transformer = ModalLogicTransformer()
parsed_formula = transformer.transform(parsed_tree)

#Print the list
print(parsed_formula)

# Visualize and save the parse tree as a PNG image, so we have a graphical idea of the tree
#tree_png = tree.pydot__tree_to_png(parsed_tree, "parse_tree.png")

