from enum import Enum
from lib2to3.pgen2 import token
import re
from typing import List

NUMBERS = "0123456789"

IDENTIFIERS_TYPE_DATA = {
    "Get",
    "or"
}

RESERVED_WORDS = {
    "if",
    "elseif",
    "else",
    "while",
    "for",
    "integer",
    "float",
    "Put",
    "RandomNumber",
    "SeedRandomNumbers",
    "SquareRoot",
    "RaiseToPower",
    "AbsoluteValue",
    "to",
    "output",
    "Function",
    "Get",
    "returns",
    "or",
    "and",
    "input",
    "next",
    "Main",
    "size",
}

SPECIAL_CHARS_REGEX = r'[A-Za-z][A-Za-z0-9_]*'

OPERATOR_SYMBOLS_TOKENS = {
    "=": "assign",
    ".": "period",
    ",": "comma",
    ";": "semicolon",
    "]": "closing_bra",
    "[": "opening_bra",
    ")": "closing_par",
    "(": "opening_par",
    "+": "plus",
    "-": "minus",
    "*": "times",
    "/": "div",
    "%": "mod",
    "==": "equal",
    "!=": "neq",
    "<": "less",
    "<=": "leq",
    ">": "greater",
    ">=": "geq",
    "?": "question_mark",
}


class TokenType(Enum):
    RESERVED_WORD = 'reserved_word'
    ID = 'id'
    INTEGER = 'tkn_integer'
    FLOAT = 'tkn_float'
    STRING = 'tkn_str'


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
        return rf'<{self.value},{self.column},{self.row}>'

    def id_word_str(self) -> str:
        return rf'<{self.type.value},{self.value},{self.column},{self.row}>'

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

    def analyze(self, lines: List[str]):
        try:
            self.process_text(lines)
        except Exception as e:
            print(e)

    def add_to_token_list(self, token: Token):
        self.tokens.append(token)
        token.print_token()

    def process_text(self, lines: List[str]):
        self.tokens = []
        for i, line in enumerate(lines):
            if line == '':
                continue
            word = r''
            line += ' '
            line = rf'{repr(line)[1:-1]}'
            temp_i = None
            temp_j = None
            temp_token = None
            is_string = False
            for j, char in enumerate(line):
                if char == ' ' and not is_string:
                    word = r''
                    temp_i = None
                    temp_j = None
                    if temp_token is not None:
                        self.add_to_token_list(temp_token)
                        temp_token = None
                    continue
                word += char
                if temp_i is None and temp_j is None:
                    temp_i = i+1
                    temp_j = j+1
                if char == '"':
                    word = word[:-1]
                    if is_string:
                        temp_token = Token(
                            TokenType.STRING, word, temp_i, temp_j
                        )
                        self.add_to_token_list(temp_token)
                        temp_token = None
                        is_string = False
                        word = r''
                        temp_i = None
                        temp_j = None
                    else:
                        is_string = True
                elif is_string:
                    pass
                elif word in RESERVED_WORDS:
                    temp_token = Token(
                        TokenType.RESERVED_WORD, word, temp_i, temp_j
                    )
                elif self.is_id(word):
                    temp_token = Token(
                        TokenType.ID, word, temp_i, temp_j
                    )
                elif self.get_number_type(word) is not None:
                    temp_token = Token(
                        self.get_number_type(word), word, temp_i, temp_j
                    )
                elif char in OPERATOR_SYMBOLS_TOKENS:
                    if char == "/":
                        try:
                            prev_token = tokens[-1]
                            if prev_token.value == 'tkn_div':
                                tokens = tokens[:-1]
                                break
                        except:
                            pass
                    if temp_token is not None:
                        self.add_to_token_list(temp_token)
                        temp_token = None
                        word = r''
                        temp_i = i+1
                        temp_j = j+1
                    temp_token = Token(
                        TokenType.RESERVED_WORD, f'tkn_{OPERATOR_SYMBOLS_TOKENS[char]}', temp_i, temp_j
                    )
                    self.add_to_token_list(temp_token)
                    temp_token = None
                    word = r''
                    temp_i = None
                    temp_j = None
                else:
                    raise Exception(
                        f'>>> Error lexico(linea: {i+1}, posicion: {j+1})'
                    )
        return tokens


#token = Token(TokenType.ID, 'if', 1, 1)
# token.print_token()
# print(token.is_operator())
text0 = [
    'Get integer or float',
    '',
    '   and',
    '         Put input next',
    '',
    '',
    '',
    'to',
    '      output',
    '',
]

text1 = ["// This does not look good.",
         "   put next To OuTpUt",
         "",
         "      // Now it’s almost fixed.",
         "         Put NEXT to outPUT", ]
text2 = ['float i',
         '',
         'for i = 0.0; i < 5; i = i + 1',
         '   Put i to output',
         '   Put " es un número.\n" to output', ]

text3 = [
    'my_Var1 = +05',
    'my_Var_2 = -3.330',
]

text4 = ['if x >= 20:',
         '   Put "Large" to output',
         'elseif x <= 10:',
         '   Put "Small" to output', ]


res = SyntacticAnalyzer().analyze(text4)
