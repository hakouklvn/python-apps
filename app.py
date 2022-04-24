import re
from colorama import Fore


OPTS = ('-', '+', '*', '/', '^')
variables = {}


class Calculator:
    def __init__(self):
        self.go = True

    def start(self) -> None:
        while self.go:
            command = input(f'{Fore.BLUE}❯ {Fore.RESET}').replace(' ', '')
            if not command:
                continue

            if command.startswith("/"):
                self.parser_command(command)
                continue

            if '=' in command:
                self.assignment(command.split('='))
                continue

            pattern = r'[\+\-\*\/\^]'
            patterns = re.findall(pattern, command)

            if patterns:
                command = self.rm_duplicate_operators(command)
                solve = Solve()
                val = solve.calculate(command)
                self.print_var(val)
                continue

            self.print_var(command)

    def parser_command(self, command: str) -> None:
        if command == "/exit":
            print(f"{Fore.MAGENTA}Bye!")
            self.go = False
            return

        if command == "/help":
            print(f"{Fore.CYAN}This is a smart calculator")
            return

        print(f'{Fore.RED}Unknown command')

    def assignment(self, command: list) -> None:
        try:
            assert len(command) == 2, "Invalid assignment"
            [key, value] = command
            assert key.isalpha(), "Invalid identifier"

            pattern = r'[\+\-\*\/\^]'
            patterns = re.findall(pattern, value)

            if patterns:
                cmd = self.rm_duplicate_operators(value)
                solve = Solve()
                value = solve.calculate(cmd)

            if value.isdigit():
                variables[key] = value
                return

            assert value.isalpha(), "Invalid assignment"
            assert variables.get(value) is not None, "Unknown variable"

        except AssertionError as err:
            print(err)
            return

        else:
            variables[key] = variables.get(value)
            return

    def print_var(self, command: str) -> None:
        if command.isdigit():
            print(f'{Fore.GREEN}{command}')
            return

        if not command.isalpha():
            print(f"{Fore.RED}Invalid identifier")
            return

        if variables.get(command) is not None:
            print(f'{Fore.GREEN}{variables.get(command)}')
        else:
            print(f'{Fore.RED}Unknown variable')

    def rm_duplicate_operators(self, command):
        pattern = r'[\+\-\*\/\^\(\)]'
        patterns = re.findall(pattern, command)

        for p in patterns:
            # USE PYTHON 3.10
            # if '-' in p:
            #     new_pattern = ' + ' if len(p) % 2 == 0 else ' - '
            # match p:
            #     case '+': command = re.sub('\++', ' + ', command)
            #     case '-': command = re.sub('\-+', new_pattern, command)
            #     case '*': command = re.sub('\*+', ' * ', command)
            #     case '/': command = re.sub('\/+', ' / ', command)
            #     case '^': command = re.sub('\^+', ' ^ ', command)
            #     case '(': command = re.sub('\(', ' ( ', command)
            #     case ')': command = re.sub('\)', ' ) ', command)
            if '-' in p:
                new_pattern = ' + ' if len(p) % 2 == 0 else ' - '
                command = re.sub('\-+', new_pattern, command)
                continue
            if '+' in p:
                command = re.sub('\++', ' + ', command)
                continue
            if '*' == p:
                command = re.sub('\*+', ' * ', command)
                continue
            if '/' == p:
                command = re.sub('\/+', ' / ', command)
                continue
            if '^' == p:
                command = re.sub('\^+', ' ^ ', command)
                continue
            if '(' in p:
                command = re.sub('\(', '( ', command)
                continue
            if ')' in p:
                command = re.sub('\)', ' )', command)
                continue

        return command


class Solve:
    def calculate(self, command: str) -> None:
        try:
            inputs = command.split()

            for i, val in enumerate(inputs):
                if variables.get(val) is not None:
                    inputs[i] = variables.get(val)

            result = self.to_infix(inputs)
            stack = []
            for i in result:
                if i == ' ':
                    continue
                if i.isdigit():
                    stack.append(i)
                    continue
                if i in OPTS:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(self.calc(a, b, i))
                    continue
                raise
            return str(stack[0])
        except:
            print('Invalid expression')
            return

    def to_infix(self, cmd):
        ops = {'^': 3, '*': 2, '/': 2, '+': 1, '-': 1}

        def high(a, b):
            return True if ops[a] < ops[b] else False

        postfix = ''
        stack = []

        for i in cmd:
            if i == ' ':
                continue
            if i in ops:
                if not len(stack) or stack[-1] == '(' or high(stack[-1], i):
                    stack.append(i)
                    continue
                else:
                    while len(stack) and stack[-1] != '(' and not high(stack[-1], i):
                        postfix += f'{stack.pop()} '
                    stack.append(i)
                    continue

            if i == '(':
                stack.append('(')
                continue

            if i == ')':
                while not stack[-1].startswith('('):
                    postfix += f'{stack.pop()} '
                stack.pop()
                continue

            postfix += f'{i} '

        while len(stack) != 0:
            postfix += f'{stack.pop()} '

        return postfix.split()

    def calc(self, a, b, op):
        solution = {
            '+': int(a)+int(b),
            '-': int(a)-int(b),
            '*': int(a)*int(b),
            '/': int(a)/int(b),
            '^': int(a)**int(b),
        }
        return solution.get(op)


def main():
    calculator = Calculator()
    calculator.start()


if __name__ == '__main__':
    main()
