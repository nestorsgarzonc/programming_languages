from enum import Enum
import re

NUMBERS = '0123456789'

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
    'Main',
    'size',
}

SPECIAL_CHARS_REGEX = r'[A-Za-z][A-Za-z0-9_]*'

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
    INTEGER = 'tkn_integer'
    FLOAT = 'tkn_float'


class Token:
    def __init__(self, t_type: TokenType, value: str, column: int, row: int):
        self.type = t_type
        self.value = value
        self.row = row
        self.column = column

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value and self.row == other.row and self.column == other.column

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return f'Token(type: {self.type.name}, value: {self.value}, row: {self.row}, column: {self.column})'

    def __repr__(self):
        return self.__str__()

    def reserved_word_str(self) -> str:
        return f'<{self.value}, {self.column}, {self.row}>'

    def id_word_str(self) -> str:
        return f'<{self.type.value}, {self.value}, {self.column}, {self.row}>'

    def print_token(self):
        if self.type == TokenType.RESERVED_WORD:
            print(self.reserved_word_str())
        else:
            print(self.id_word_str())

    def is_reserved_word(self) -> bool:
        return self.value in RESERVED_WORDS

    def is_operator(self) -> str:
        val = self.value in OPERATOR_SYMBOLS_TOKENS
        if not val:
            return None
        return f'tkn_{OPERATOR_SYMBOLS_TOKENS[self.value]}'

    def is_id(self) -> bool:
        return self.type == TokenType.ID


class SyntacticAnalyzer:
    def is_id(self, word: str) -> bool:
        return re.match(SPECIAL_CHARS_REGEX, word) is not None

    def get_number_type(self, word: str) -> TokenType:
        number_type = None
        for i in word:
            if i in NUMBERS and number_type == TokenType.FLOAT:
                number_type = TokenType.FLOAT
            elif i in NUMBERS:
                number_type = TokenType.INTEGER
            elif i == '.':
                number_type = TokenType.FLOAT
            else:
                return None
        return number_type

    def process_text(self, text: str):
        tokens = []
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line == '':
                continue
            word = ''
            line += ' '
            temp_i = None
            temp_j = None
            temp_token = None
            #TODO: CHECK FOR STRIGNS
            for j, char in enumerate(line):
                if char == ' ':
                    word = ''
                    temp_i = None
                    temp_j = None
                    if temp_token is not None:
                        tokens.append(temp_token)
                        temp_token = None
                    continue
                word += char
                if temp_i is None and temp_j is None:
                    temp_i = i+1
                    temp_j = j+1
                if word in RESERVED_WORDS:
                    temp_token = Token(
                        TokenType.RESERVED_WORD, word, temp_i, temp_j
                    )
                elif word in OPERATOR_SYMBOLS_TOKENS:
                    temp_token = Token(
                        TokenType.RESERVED_WORD, f'tkn_{OPERATOR_SYMBOLS_TOKENS[word]}', temp_i, temp_j
                    )
                    tokens.append(temp_token)
                    temp_token = None
                    word = ''
                    temp_i = None
                    temp_j = None
                elif self.is_id(word):
                    temp_token = Token(
                        TokenType.ID, word, temp_i, temp_j
                    )
                elif self.get_number_type(word) is not None:
                    temp_token = Token(
                        self.get_number_type(word), word, temp_i, temp_j
                    )
                else:
                    raise Exception(
                        f'Invalid token {word} at row {temp_i} and column {temp_j}')
        return tokens


#token = Token(TokenType.ID, 'if', 1, 1)
# token.print_token()
# print(token.is_operator())
res = SyntacticAnalyzer().process_text('''my_Var1 = +05
my_Var_2 = -3.330''')
for i in res:
    i.print_token()
