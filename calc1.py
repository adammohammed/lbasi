import logging
import sys
INTEGER, PLUS, MINUS, MULT, DIV, EOF = "INTEGER", "PLUS", "MINUS", "MULT", "DIV", "EOF"
OP_LIST = [PLUS, MINUS, MULT, DIV]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(consoleHandler)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({}, {})".format(
            self.type,
            self.value
        )

    def __repr__(self):
        self.__str__()

class Interpreter:
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

    def eat(self, token_type):
        logger.debug("EAT - %s - %s", self.current_token, token_type)
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.errors()

    def expr(self):
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(INTEGER)

        result = left.value

        while self.current_token.type != EOF:
            op = self.current_token
            if op.type in OP_LIST:
                self.eat(op.type)

            right = self.current_token
            self.eat(INTEGER)

            if op.type == PLUS:
                result = result + right.value
            elif op.type == MINUS:
                result = result - right.value
            elif op.type == MULT:
                result = result * right.value
            elif op.type == DIV:
                result = result / right.value

        return result

def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
