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
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def eat(self, token_type):
        logger.debug("EAT - %s - %s", self.current_token, token_type)
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.errors()

    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        self.current_token = self.lexer.get_next_token()

        result = self.term()

        while self.current_token.type in (PLUS, MINUS, MULT, DIV):
            op = self.current_token
            if op.type in OP_LIST:
                self.eat(op.type)

            term = self.term()

            if op.type == PLUS:
                result = result + term
            elif op.type == MINUS:
                result = result - term
            elif op.type == MULT:
                result = result * term
            elif op.type == DIV:
                result = result // term

        return result




def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
