import logging
import sys

from calq.lexer import Lexer, INTEGER, PLUS, MINUS, MULT, DIV, EOF, OP_LIST

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(consoleHandler)


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def errors(self):
        raise Exception(f"Error interpreting input: {self.current_token}")

    def eat(self, token_type):
        logger.debug("EAT - %s - %s", self.current_token, token_type)
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.errors()

    def term(self):
        result = self.factor()

        while self.current_token.type in (MULT, DIV):
            op = self.current_token
            self.eat(op.type)
            rfactor = self.factor()

            if op.type == MULT:
                result = result * rfactor
            elif op.type == DIV:
                result = result // factor

        return result

    def factor(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        self.current_token = self.lexer.get_next_token()

        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            op = self.current_token
            self.eat(op.type)

            term = self.term()

            if op.type == PLUS:
                result = result + term
            elif op.type == MINUS:
                result = result - term

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


if __name__ == "__main__":
    main()
