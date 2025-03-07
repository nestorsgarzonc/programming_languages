from enum import Enum
import re

NUMBERS = "0123456789"

RESERVED_WORDS = {
    "AbsoluteValue",
    "and",
    "array",
    "decimal",
    "else",
    "elseif",
    "evaluates",
    "float",
    "for",
    "Function",
    "Get",
    "if",
    "input",
    "integer",
    "Main",
    "places",
    "nothing",
    "next",
    "not",
    "or",
    "output",
    "places",
    "Put",
    "RaiseToPower",
    "RandomNumber",
    "returns",
    "SeedRandomNumbers",
    "size",
    "SquareRoot",
    "to",
    "while",
    "with",
}

SPECIAL_CHARS_REGEX = r'[A-Za-z][A-Za-z0-9_]*'
NUMBERS_REGEX = r'[0-9]+'
FLOAT_REGEX = r'[0-9]+\.[0-9]+'

OPERATOR_SYMBOLS_TOKENS = {
    "-": "minus",
    ",": "comma",
    ";": "semicolon",
    "!=": "neq",
    "?": "question_mark",
    ".": "period",
    "(": "opening_par",
    ")": "closing_par",
    "[": "opening_bra",
    "]": "closing_bra",
    "*": "times",
    "/": "div",
    "%": "mod",
    "+": "plus",
    "<": "less",
    "<=": "leq",
    "=": "assign",
    "==": "equal",
    ">": "greater",
    ">=": "geq",
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


class SyntacticAnalyzer:
    def is_id(self, word: str) -> bool:
        return re.fullmatch(SPECIAL_CHARS_REGEX, word) is not None

    def get_number_type(self, word: str, next_char: str) -> TokenType:
        if re.fullmatch(NUMBERS_REGEX, word) is not None:
            return TokenType.INTEGER
        elif re.fullmatch(FLOAT_REGEX, word) is not None:
            return TokenType.FLOAT
        elif re.fullmatch(FLOAT_REGEX, word+next_char) is not None:
            return TokenType.FLOAT
        return None

    def analyze(self):
        self.tokens = []
        counter_line = 0
        try:
            while True:
                line = input()
                self.process_text(line, counter_line)
                counter_line += 1
        except ValueError as e:
            print(e)
        except EOFError:
            pass

    def add_to_token_list(self, token: Token):
        self.tokens.append(token)
        self.counter_line += 1
        token.print_token()

    def is_backslash(self, char: str) -> bool:
        return ord(char) == 92

    def manual_process(self, line: str):
        self.tokens = []
        self.process_text(line, 1)

    def process_text(self, line: str, row: int):
        i = row
        if line == '':
            return
        word = r''
        line += ' '
        line = line
        temp_i = None
        temp_j = None
        temp_token = None
        ignore_next = False
        is_string = False
        self.counter_line = 0
        for j, char in enumerate(line):
            next_char = ''
            try:
                next_char = line[j + 1]
            except:
                pass
            if ignore_next:
                ignore_next = False
            else:
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
                if is_string and self.is_backslash(char):
                    if next_char in ['"', "n", "t", chr(92)]:
                        ignore_next = True
                        word += next_char
                    pass
                elif char == '"':
                    if temp_token is not None and temp_token.type != TokenType.STRING:
                        self.add_to_token_list(temp_token)
                        temp_token = None
                        word = char
                        temp_i = i+1
                        temp_j = j+1
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
                elif self.get_number_type(word, next_char) is not None:
                    temp_token = Token(
                        self.get_number_type(
                            word, next_char), word, temp_i, temp_j
                    )
                elif char in OPERATOR_SYMBOLS_TOKENS:
                    if self.counter_line == 0 and char == "/":
                        try:
                            if line[j+1] == '/':
                                break
                        except:
                            pass
                    temp_char = char
                    try:
                        next_char = line[j+1]
                        if temp_char+next_char in OPERATOR_SYMBOLS_TOKENS:
                            temp_char = temp_char+next_char
                            ignore_next = True
                    except:
                        pass
                    if temp_token is not None:
                        self.add_to_token_list(temp_token)
                        temp_token = None
                        word = r''
                        temp_i = i+1
                        temp_j = j+1
                    temp_token = Token(
                        TokenType.RESERVED_WORD, f'tkn_{OPERATOR_SYMBOLS_TOKENS[temp_char]}', temp_i, temp_j
                    )
                    self.add_to_token_list(temp_token)
                    temp_token = None
                    word = r''
                    temp_i = None
                    temp_j = None
                elif char+next_char in OPERATOR_SYMBOLS_TOKENS:
                    if temp_token is not None:
                        self.add_to_token_list(temp_token)
                        temp_token = None
                        word = r''
                        temp_i = i+1
                        temp_j = j+1
                    ignore_next = True
                    temp_token = Token(
                        TokenType.RESERVED_WORD, f'tkn_{OPERATOR_SYMBOLS_TOKENS[char+next_char]}', temp_i, temp_j
                    )
                    self.add_to_token_list(temp_token)
                    temp_token = None
                    word = r''
                    temp_i = None
                    temp_j = None
                else:
                    if temp_token:
                        self.add_to_token_list(temp_token)
                        temp_token = None
                        word = r''+char
                        temp_i = None
                        temp_j = None
                        if temp_i is None and temp_j is None:
                            temp_i = i+1
                            temp_j = j+1
                        if char == '"':
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
                        elif self.get_number_type(word, next_char) is not None:
                            temp_token = Token(
                                self.get_number_type(
                                    word, next_char), word, temp_i, temp_j
                            )
                        elif char in OPERATOR_SYMBOLS_TOKENS:
                            temp_char = char
                            try:
                                next_char = line[j+1]
                                if temp_char+next_char in OPERATOR_SYMBOLS_TOKENS:
                                    temp_char = temp_char+next_char
                                    ignore_next = True
                            except:
                                pass
                            temp_token = Token(
                                TokenType.RESERVED_WORD, f'tkn_{OPERATOR_SYMBOLS_TOKENS[temp_char]}', temp_i, temp_j
                            )
                            self.add_to_token_list(temp_token)
                            temp_token = None
                            word = r''
                            temp_i = None
                            temp_j = None
                        elif char+next_char in OPERATOR_SYMBOLS_TOKENS:
                            ignore_next = True
                            temp_token = Token(
                                TokenType.RESERVED_WORD, f'tkn_{OPERATOR_SYMBOLS_TOKENS[char+next_char]}', temp_i, temp_j
                            )
                            self.add_to_token_list(temp_token)
                            temp_token = None
                            word = r''
                            temp_i = None
                            temp_j = None
                        else:
                            self.raise_error(i+1, j+1)
                    else:
                        self.raise_error(i+1, j+1)
        if is_string:
            self.raise_error(i+1, temp_j)
        return self.tokens

    def raise_error(self, i, j):
        raise ValueError(f'>>> Error lexico (linea: {i}, posicion: {j})')


SyntacticAnalyzer().analyze()
