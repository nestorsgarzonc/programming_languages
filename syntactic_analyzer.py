from enum import Enum


RESERVED_WORDS = {
    'if',
    'elseif',
    'else',
    'while',
    'for',
    'integer'
    'float',
    'Put',
    'RandomNumber',
    'SeedRandomNumbers',
    'SquareRoot',
    'RaiseToPower',
    'AbsoluteValue',
    'to',
    'output',
    'Function',
    'Get'
    'returns',
    'or',
    'and',
    'input',
    'next',
}


OPERATOR_SYMBOLS_TOKENS = {
    '=': 'assign',
    '.': 'period',
    ',': 'comma',
    ';': 'semicolon',
    ']': 'closing_bra',
    '[': 'opening_bra',
    ')': 'closing_par',
    '(': 'opening_par',
    '+': 'plus',
    '-': 'minus',
    '*': 'times',
    '/': 'div',
    '%': 'mod',
    '==': 'equal',
    '!=': 'neq',
    '<': 'less',
    '<=': 'leq',
    '>': 'greater',
    '>=': 'geq',
    '?': 'question_mark',
}


class TokenType(Enum):
    RESERVED_WORD = 'reserved_word'
    ID = 'id'
    NUMBER = 'number'


class Token:
    def __init__(self, t_type: TokenType, value: str, row: int, column: int):
        self.type = t_type
        self.value = value
        self.row = row
        self.column = column

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value and self.row == other.row and self.column == other.column

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return f'Token(type: {self.type}, value: {self.value}, row: {self.row}, column: {self.column})'

    def __repr__(self):
        return self.__str__()

    def reserved_word_str(self) -> str:
        # return self.type in ['program', 'var', 'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'read', 'write']
        return f'Token(reserved word|value|: {self.value}, row: {self.row}, column: {self.column})'

    def is_reserved_word(self) -> bool:
        return self.type in RESERVED_WORDS
