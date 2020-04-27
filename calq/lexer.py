""" Lexer - tokenizes input for an interpreter """
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def errors(self):
        raise Exception(f"Error parsing input: pos - {self.pos} - {self.text} - {self.current_token}")

    def advance(self):

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):

        num = ''
        while self.current_char is not None and self.current_char.isdigit():
            num += self.current_char
            self.advance()

        return int(num)

    def get_next_token(self):
        text = self.text

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char is '+':
                self.advance()
                return Token(PLUS, None)

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, None)

            if self.current_char == "*":
                self.advance()
                return Token(MULT, None)

            if self.current_char == "/":
                self.advance()
                return Token(DIV, None)

        return Token(EOF, None)
