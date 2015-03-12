#!/usr/bin/env python
import ply.lex as lex
# from helpers import debug as debug

reserved = {
    'my': 'MY',
    'use': 'USE',
    'if' : 'IF',
    'else' : 'ELSE',
    'elsif' : 'ELSIF',
    'switch' : 'SWITCH',
    'unless' : 'UNLESS',
    'while' : 'WHILE',
    'do' : 'DO',
    'for' : 'FOR',
    'foreach' : 'FOREACH',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'function' : 'FUNCTION',
    'return' : 'RETURN',
    'print' : 'PRINT',
    'die' : 'DIE',
    'open': 'OPEN',
    'close':'CLOSE',
    'write':'WRITE',
    'format':'FORMAT',
    'warnings': 'WARNINGS',
    'chdir': 'CHDIR',
    'chomp': 'CHOMP',
    'strict':'STRICT',
    'case':'CASE',
    'keys':'KEYS',
    'values':'VALUES',
    'sub':'SUB',
    'each':'EACH'

 }

tokens = [
   'ARRAY_VARIABLE',
   'HASH_VARIABLE',
   'SCALAR_VARIABLE',
   'IDENTIFIER',
   'INTEGER',
   'FLOAT',
   'EXPONANTIAL',
   'BINARY',
   'HEXADECIMAL',
   'OCTAL',
   'STRING',
   'PLUS',
   'MINUS',
   'MULTIPLY',
   'DIVIDE',
   'MODULUS',
   'LPAR',
   'RPAR',
   'OPEN_BRACKET',
   'CLOSE_BRACKET',
   'SEMICOLON',
   'COLON',
   'Q_MARK',
   'AND',
   'OR',
   'NOT',
   'NOT_EQUAL',
   'ASSIGNMENT',
   'SIMULT_ASSIGNMENT',
   'EQUAL',
   'BLOCK_BEGIN',
   'BLOCK_END',
   'OP_GREATER_THAN',
   'OP_GREATER_THAN_E',
   'OP_LESS_THAN',
   'OP_LESS_THAN_E',
   'OP_LESS_EQUAL_GREATER',
   'EXPONENT',
   'INCREAMENT',
   'DCREAMENT',
   'STR_OP',
   'DOT',
   'DOUBLE_DOT',
   'COMMENT',
   'COMMA',
   'TILDA',
   'WHITESPACE',
   'BACKSLASH',
   'STRING_CMP',
   'INPUT',
   'PSEUDO_STRING',
   'TERNARY'
]+list(reserved.values())
       
t_PLUS = r'\+'
t_MINUS   = r'-'
t_MULTIPLY   = r'\*'
t_DIVIDE  = r'/'
t_MODULUS  = r'\%'
t_LPAR = r'\('
t_RPAR = r'\)'
t_OPEN_BRACKET = r'\['
t_CLOSE_BRACKET = r'\]'
t_SEMICOLON = r';'
t_AND = r'&&|'r'[\s]and[\s]'
t_OR = r'\|\||'r'[\s]or[\s] '
t_NOT = r'!'
t_NOT_EQUAL = r'!='
t_BLOCK_BEGIN = r'\{'
t_BLOCK_END = r'\}'
t_DOT = r'\.'
t_Q_MARK = r'\?'
t_COLON = r':'
t_DOUBLE_DOT = r'\.\.'
t_EXPONENT = r'\*\*'
t_INCREAMENT =r'\+\+'
t_DCREAMENT = r'--'
t_OP_GREATER_THAN = r'\>'
t_OP_GREATER_THAN_E = r'\>='
t_OP_LESS_THAN = r'\<'
t_OP_LESS_THAN_E = r'\<='
t_OP_LESS_EQUAL_GREATER = r'\<=\>'
t_EQUAL = r"==" 
t_ASSIGNMENT = r'='
t_SIMULT_ASSIGNMENT = r'\+=|'r'-=|'r'\*=|'r'/=|'r'%=|'r'\*\*='
t_STRING_CMP = r'[\s]lt[\s]|'r'[\s]gt[\s]|'r'[\s]le[\s]|'r'[\s]ge[\s]|'r'[\s]eq[\s]|'r'[\s]ne[\s]|'r'[\s]cmp[\s]'
t_COMMA = r','
t_BACKSLASH = r'\\'
t_TILDA = r'\~'
t_ignore_WHITESPACE = r"\s"
t_INPUT = r'<STDIN>|'r'<>'

def t_ignore_COMMENT(t):
   r"\#[^\n]+|"r"\=[^(=)]+\=cut"


def t_ignore_newline(t):
  r'\n+'

def t_STRING(t):
    r"[\"][^\"]*[\"]"
    t.value = t.value[1:-1]
    return t
    
def t_PSEUDO_STRING(t):
  r"['][^']*[']"
  t.value = t.value[1:-1]
  return t

def t_IDENTIFIER(t):
    r"[a-z_A-Z][\w]*"
    t.type = reserved.get(t.value,'IDENTIFIER')    
    return t
    
def t_SCALAR_VARIABLE(t):
    r"[$][a-zA-Z_][\w]*"
    return t

def t_ARRAY_VARIABLE(t):
    r"[@][a-zA-Z_][\w]*"
    return t;

def t_HASH_VARIABLE(t):
    r"[%][a-zA-Z_][\w]*"
    return t;

def t_EXPONANTIAL(t):
  r"\d+\.\d+[eE][-]?\d+"
  return t

def t_FLOAT(t):
     r"\d+\.\d+"
     return t



def t_BINARY(t):
  r"0b[01]+"
  return t

def t_OCTAL(t):
  r"0[0-7]+"
  return t

def t_HEXADECIMAL(t):
    r"0x[0-9a-fA-F]+"
    return t  

def t_INTEGER(t):
    r"[1-9]\d*|"r"0"
    return t

       
    
def t_error(t):
    print "Illegal character" 
    t.lexer.skip(1)
      


lexer=lex.lex()   
def testLex(inputFile):
    program = open(inputFile).read()
    lexer.input(program)

    # This iterates over the function lex.token and converts the returned object into an iterator
    print "\tTYPE \t\t\t\t\t\t VALUE"
    print "\t---- \t\t\t\t\t\t -----"
    for tok in iter(lexer.token, None):
        print "%-25s \t\t\t\t %s" %(repr(tok.type), repr(tok.value))

if __name__ == '__main__':
  from sys import argv
  filename, inputFile = argv
  testLex(inputFile)
