import ply.lex as lex

# coding: utf-8

#Keywords for our interpreter
keywords = {
    "for": "FOR",
    "do": "DO",
    "endfor": "ENDFOR",
    "in": "IN",
    "print": "PRINT",

    #DLC
    "true": "TRUE",
    "false": "FALSE",
    "or": "OR",
    "and": "AND",
    "if": "IF",
    "endif": "ENDIF",
}

tokens = [
    "TXT",
    "VARIABLE",
    "DUMBO_BLOCK_START",
    "DUMBO_BLOCK_END",
    "LPAREN",
    "RPAREN",
    "ASSIGN",
    "STRING",
    "DOT",
    "COMMA",
    "SEMICOLON",
    "NUMBER",
    "PLUS",
    "MINUS",
    "MULT",
    "DIV",
    "UNARY_MINUS",
    "COMPARATOR",
] + list(keywords.values())

states = (("DBLOCK", "inclusive"), ("TEXT", "inclusive"))

def t_TEXT_DUMBO_BLOCK_START(t):
    r"{{"
    t.lexer.begin("DBLOCK")
    return t


def t_DBLOCK_DUMBO_BLOCK_END(t):
    r"}}"
    t.lexer.begin("TEXT")
    return t

t_TEXT_TXT = r'[a-zA-Z0-9;&<>"_=.\/ \n\s:,"-]+'
t_DBLOCK_LPAREN = r"\("
t_DBLOCK_RPAREN = r"\)"
t_DBLOCK_ASSIGN = r":="
t_DBLOCK_DOT = r"\."
t_DBLOCK_COMMA = r","
t_DBLOCK_SEMICOLON = r";"
t_DBLOCK_PLUS = r"\+"
t_DBLOCK_MINUS = r"-"
t_DBLOCK_MULT = r"[*/]"
t_DBLOCK_COMPARATOR = r"[<>=]|!="


def t_DBLOCK_NUMBER(t): #Had to manage real number, since we can divide
    r"\d+(\.\d*)?"
    try:
        t.value = int(t.value)
    except:
        t.value = float(t.value)
    return t


def t_DBLOCK_VARIABLE(t):
    r"[a-zA-Z0-9_]+"
    #Avoids using keywords
    t.type = keywords.get(t.value, "VARIABLE") 
    return t


def t_DBLOCK_STRING(t):
    r'\'[a-zA-Z0-9;&<>"_=.\/ \n\s:,"-]+\''
    t.value = t.value[1:-1] #https://stackoverflow.com/a/3085402
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


t_DBLOCK_ignore = " \t"


def t_error(t):
    print("Illegalcharacter '{}' at line {}".format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)


lexer = lex.lex()
lexer.begin("TEXT")

if __name__ == "__main__":
    import sys

    # lexer.input(sys.stdin.read())
    file = open(sys.argv[1]).read()
    lexer.input(file)

    for token in lexer:
        print("line %d : %s (%s) " % (token.lineno, token.type, token.value))
