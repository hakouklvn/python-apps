from colorama import Fore

state = [
    ['X', ' ', 'O'],
    ['O', 'X', ' '],
    [' ', 'O', ' ']
]
player = True


def reset_board():
    global player
    player = True

    for i in range(3):
        for j in range(3):
            state[i][j] = ' '


def draw_board():
    print(f'{Fore.CYAN}---------')
    for row in state:
        print(f'{Fore.CYAN}| ', end="")
        for s in row:
            if s == 'X':
                print(f'{Fore.GREEN}{s} ', end=f'{Fore.RESET}')
            if s == 'O':
                print(f'{Fore.YELLOW}{s} ', end=f'{Fore.RESET}')
            if s == ' ':
                print('  ', end='')
        print(f'{Fore.CYAN}|')
    print(f'---------{Fore.RESET}')


def check_winner():
    for idx, row in enumerate(state):
        for symbol in ('X', 'O'):
            counter = 0
            for jdx, _ in enumerate(row):
                if state[jdx][idx] == symbol:
                    counter += 1
            # Vertical OR Horizontal
            if counter == 3 or row.count(symbol) == 3:
                return symbol

    # First diagonal OR Second Diagonal
    for symbol in ('X', 'O'):
        first = [True if state[i][i] == symbol else False for i in range(3)]
        second = [True if state[i][2-i] == symbol else False for i in range(3)]
        if all(first) or all(second):
            return symbol

    # Game not finished
    empty = sum([row.count(' ') for row in state])
    if empty == 0:
        return 'Draw'

    return None


def handle_cmd_err(cmd):
    paramaters = ['user', 'easy', 'medium', 'hard']
    cmd = cmd.split()
    assert len(cmd) == 3, 'Bad parameters!'
    assert cmd[0] == 'start', 'Bad parameters!'
    assert cmd[1] in paramaters and cmd[2] in paramaters, 'Bad parameters!'


def ai_easy(symbol):
    import random
    global player

    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)

        if state[row][col] == ' ':
            print('Making move level "easy"')
            state[row][col] = symbol
            player = not player

            break


def ai_medium(symbol):
    import random
    global player
    player = not player

    # Rule 1
    for idx, row in enumerate(state):
        if row.count(symbol) == 2 and row.count(' ') == 1:
            for jdx, col in enumerate(row):
                if state[idx][jdx] == ' ':
                    state[idx][jdx] = symbol
                    return

    # Rule 2
    other_symbol = 'X' if player else 'O'
    # Horizontal
    for idx, row in enumerate(state):
        if (row.count(other_symbol) == 2) and (row.count(' ') == 1):
            jdx = row.index(' ')
            state[idx][jdx] = symbol
            return

    # Vertical
    for i in range(3):
        counter = space = 0
        space_x = space_y = 0
        for j in range(3):
            if state[j][i] == other_symbol:
                counter += 1
            elif state[j][i] == ' ':
                space += 1
                space_x, space_y = j, i
        # Vertical
        if counter == 2 and space == 1:
            state[space_x][space_y] = symbol
            return

    # Diagonal
    counter = space = index = 0
    for i in range(3):
        if state[i][i] == other_symbol:
            counter += 1
        elif state[i][i] == ' ':
            space += 1
            index = i
    if counter == 2 and space == 1:
        state[index][index] = symbol
        return

    # Second Diagonal
    counter = space = index = 0
    for i in range(3):
        if state[i][2-i] == other_symbol:
            counter += 1
        elif state[i][2-i] == ' ':
            space += 1
            index = i

    if counter == 2 and space == 1:
        state[index][2-index] = symbol
        return

    #######
    # Rule 3
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)

        if state[row][col] == ' ':
            print('Making move level "medium"')
            state[row][col] = symbol
            break


def maximize(symbol, scores, alpha, beta):
    new_symbol = 'O' if player else 'X'
    max_val = float('-inf')
    px = py = None

    winner = check_winner()
    if winner in scores:
        return (scores[winner], 0, 0)

    for i in range(0, 3):
        for j in range(0, 3):
            if state[i][j] == ' ':
                state[i][j] = symbol
                (m, _, _) = minimize(new_symbol, scores, alpha, beta)
                if m > max_val:
                    max_val = m
                    px = i
                    py = j
                # Setting back the field to empty
                state[i][j] = ' '
                if max_val >= beta:
                    return (max_val, px, py)

                if max_val > alpha:
                    alpha = max_val

    return (max_val, px, py)


def minimize(symbol, scores, alpha, beta):
    new_symbol = 'X' if player else 'O'

    min_val = float('inf')
    px = py = None

    winner = check_winner()
    if winner in scores:
        return (scores[winner], 0, 0)

    for i in range(0, 3):
        for j in range(0, 3):
            if state[i][j] == ' ':
                state[i][j] = symbol
                (m, _, _) = maximize(new_symbol, scores, alpha, beta)
                if m < min_val:
                    min_val = m
                    px = i
                    py = j
                # Setting back the field to empty
                state[i][j] = ' '
                if min_val <= alpha:
                    return (min_val, px, py)

                if min_val < beta:
                    beta = min_val
    return (min_val, px, py)


def user_play(symbol):
    global player
    try:
        row, col = map(int, input("Enter the coordinates: ").strip().split())
    except (ValueError, TypeError):
        print("You should enter numbers!")
    else:
        row, col = int(row)-1, int(col)-1
        assert 0 <= row < 3 and 0 <= col < 3, 'Coordinates should be from 1 to 3!'
        assert state[row][col] == ' ', 'This cell is occupied! Choose another one!'

        state[row][col] = symbol
        player = not player


def play_game(cmd):
    global player

    while True:
        # symbol = f'{Fore.GREEN}X{Fore.RESET}' if player else f'{Fore.BLUE}O{Fore.RESET}'
        symbol = 'X' if player else 'O'
        index = 0 if player else 1
        scores = {'X': 1, 'O': -1,
                  'Draw': 0}if player else {'X': -1, 'O': 1, 'Draw': 0}
        game = {'user': user_play, 'easy': ai_easy, 'medium': ai_medium}

        try:
            draw_board()
            winner = check_winner()
            if winner is not None:
                draw = f'{Fore.MAGENTA}Draw{Fore.RESET}'
                msg = f'{Fore.GREEN} X wins' if winner == 'X' else f'{Fore.YELLOW} O wins'
                print(draw if winner == 'Draw' else f'{msg}{Fore.RESET}')
                break

            if cmd[index] == 'hard':
                print('Making move level "hard"')
                (m, px, py) = maximize(symbol, scores, float('-inf'), float('inf'))
                state[px][py] = symbol
                player = not player
                continue

            game.get(cmd[index])(symbol)

        except AssertionError as err:
            print(err)


def main():
    global player

    while True:
        try:
            reset_board()
            cmd = input('Input command: ')
            if cmd == 'exit':
                break
            handle_cmd_err(cmd)
            play_game(cmd.split()[1:])

        except AssertionError as err:
            print(f'{Fore.RED}{err}{Fore.RESET}')


if __name__ == '__main__':
    main()
