from lox.Token import Token, TokenType
import lox.Lox as Lox


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []

        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> [Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", "", self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()
        singleton_map = {
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            '-': TokenType.MINUS,
            '+': TokenType.PLUS,
            ';': TokenType.SEMICOLON,
            '*': TokenType.STAR
        }
        if c in singleton_map:
            self.add_token(singleton_map[c])
        elif c == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                while not self.is_at_end() and self.peek() != '\n':
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c in ' \r\t':
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        elif c.isdigit():
            self.number()
        elif Scanner.is_alpha(c):
            self.identifier()
        else:
            Lox.Lox.error(self.line, "Unexpected token.")

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type: TokenType, literal=None):
        self.tokens.append(Token(token_type, self.source[self.start: self.current]
                                 , literal, self.line))

    def match(self, expected) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            Lox.Lox.error(self.line, "Unterminated string.")
            return

        self.advance()

        self.add_token(TokenType.STRING, self.source[self.start+1:self.current-1])

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()

            while self.peek().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self):
        while Scanner.is_alpha(self.peek()):
            self.advance()
        keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }
        lexeme = self.source[self.start:self.current]
        self.add_token(TokenType.IDENTIFIER if lexeme not in keywords else keywords[lexeme])

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        else:
            return self.source[self.current + 1]

    @staticmethod
    def is_alpha(ch: str):
        return ch.isalpha() or str == '_' or ch.isdigit()
