import sys
import lox.Scanner as Scanner


class Lox:
    had_error = False

    def __init__(self):
        pass

    @staticmethod
    def main(argv):
        if len(argv) > 1:
            print('Usage: pylox [script]')
            sys.exit(64)
        elif len(argv) == 1:
            pass
            # Lox.run_file(argv[0])
        else:
            Lox.run_prompt()

    @staticmethod
    def run_prompt():
        while True:
            Lox.run(input('> '))
            Lox.had_error = False

    @staticmethod
    def run(source):
        scanner = Scanner.Scanner(source)
        tokens = scanner.scan_tokens()
        for t in tokens:
            print(t)

    @staticmethod
    def error(line, message):
        Lox.report(line, "", message)

    @staticmethod
    def report(line, where, message):
        print("[line {}] Error {}: {}".format(line, where, message))
        Lox.had_error = True
