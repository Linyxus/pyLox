from lox.TokenType import TokenType


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return str(self.type) + " " + self.lexeme + " " + str(self.literal)
