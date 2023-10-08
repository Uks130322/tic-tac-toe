"""Play tic-tac-toe with your computer!"""

import random
from time import sleep


MOVES = 9   # amount of moves
field_list = [None] * 9


phrases = {"begin": ("Let's play tic-tac-toe!",
                     "I'm not a very good player but let's try",
                     "Let the game begin!"),
           "computerFirst": ("Let me start",
                             "I'm the first player and you are the second"),
           "humanFirst": ("You are X and i'm O",
                          "Please, begin"),
           "instruction": ("Enter cell name in 'a1' format",),
           "computerTurn": ("My turn now",
                            "It's my move",
                            "I'll move here:",
                            "Okay, let me think..."),
           "humanTurn": ("Your turn now",
                         "Please make your move",
                         "Let's see what you'll do",
                         "Make your choose"),
           "wrongFormat": ("I don't understand, please enter again",
                           "Can't understand, try again",
                           "Repeat, please, i didn't get it"),
           "occupied": ("This cell is occupied",
                        "It's already done, try another one",
                        "It's occupied, make another move"),
           "computerWin": ("Wow, I won!",
                           "Victory is mine!",
                           "I won. Thank you for the game"),
           "humanWin": ("You won! Congrats!",
                        "Oh no, i lost, as always...",
                        "You won. It's not my day, i guess..."),
           "draw": ("It's a draw",
                    "Draw. We both are the best",
                    "A draw. Good game"),
           "playAgain": ("Wanna play again?",
                         "Maybe one more time?"),
           "dontPlayAgain": ("Ok, bye! Hava a nice day",
                             "I'll be waiting for you here!")
           }


class FieldIsOccupied(ValueError):
    pass


def clean_input(some_text, func):
    table = some_text.maketrans(',.?:;!-', "       ")
    some_text = some_text.translate(table)
    some_text = some_text.replace(" ", "")
    some_text = func(some_text)
    return some_text


def start():
    """Decide who move first, zero is computer, one is human"""

    return random.randrange(2)


human_first = start()


def computer_turn():
    """Computer choose random field to move"""

    global MOVES, field_list, human_first
    move = random.randrange(MOVES)
    k = 0

    print(random.choice(phrases["computerTurn"]))
    sleep(1)

    for index in range(len(field_list)):
        if k == move and not field_list[index]:
            field_list[index] = human_first + 1
            break
        elif field_list[index]:
            continue
        else:
            k += 1

    MOVES -= 1


def human_turn():
    """Human move in format 'a1'"""

    global MOVES, field_list, human_first

    print(random.choice(phrases["humanTurn"]))

    move = input()
    move = clean_input(move, str.lower)

    try:
        if move[0] not in ("a", "b", "c") or move[1] not in ("1", "2", "3"):
            raise ValueError
        index = (ord(move[0]) - 97) * 3 + int(move[1]) - 1   # because ord("a") is 97

        if field_list[index]:
            raise FieldIsOccupied

        field_list[index] = human_first or 2
        MOVES -= 1
    except FieldIsOccupied:
        print(random.choice(phrases["occupied"]))
        human_turn()
    except ValueError:
        print(random.choice(phrases["wrongFormat"]))
        human_turn()


def show_field() -> None:
    """Print game field"""

    global field_list
    lst = field_list
    field_dict = {None: " - ", 1: " X ", 2: " O "}
    print(f"    1  2  3 \n"
          f" a {field_dict[lst[0]]}{field_dict[lst[1]]}{field_dict[lst[2]]}\n"
          f" b {field_dict[lst[3]]}{field_dict[lst[4]]}{field_dict[lst[5]]}\n"
          f" c {field_dict[lst[6]]}{field_dict[lst[7]]}{field_dict[lst[8]]}\n")


def cheque_win():
    """
    Check someone's victory or draw
    return 1 in case first player win
    return 2 in case second player win
    return 3 in case draw
    return 0 in case game isn't finished
    """

    global MOVES, field_list

    first = [1, 1, 1]
    second = [2, 2, 2]
    win_first = [field_list[:3] == first or
                 field_list[3:6] == first or
                 field_list[6:] == first or
                 field_list[::3] == first or
                 field_list[1::3] == first or
                 field_list[2::3] == first or
                 field_list[2:7:2] == first or
                 field_list[::4] == first
                 ]
    win_second = [field_list[:3] == second or
                  field_list[3:6] == second or
                  field_list[6:] == second or
                  field_list[::3] == second or
                  field_list[1::3] == second or
                  field_list[2::3] == second or
                  field_list[2:7:2] == second or
                  field_list[::4] == second
                  ]
    if any(win_first):
        return 1
    elif any(win_second):
        return 2
    elif MOVES == 0:
        return 3
    else:
        return 0


def choose_winner():
    """Choose who won"""

    if cheque_win() == 0:
        return 0
    elif cheque_win() == 3:
        return random.choice(phrases["draw"])
    elif cheque_win() == 1:
        if human_first:
            return random.choice(phrases["humanWin"])
        else:
            return random.choice(phrases["computerWin"])
    elif cheque_win() == 2:
        if human_first:
            return random.choice(phrases["computerWin"])
        else:
            return random.choice(phrases["humanWin"])


def play_again():
    """Ask player about repeat and start new game or say goodbye"""

    global MOVES, field_list, human_first

    print(random.choice(phrases["playAgain"]))
    answer = input("YES or NO\n")
    answer = clean_input(answer, str.upper)

    if answer == "NO":
        print(random.choice(phrases["dontPlayAgain"]))
        MOVES = 9
        field_list = [None] * 9
    elif answer == "YES":
        MOVES = 9
        field_list = [None] * 9
        human_first = start()
        all_together()
    else:
        print(random.choice(phrases["wrongFormat"]))
        play_again()


def all_together():
    """The whole game. Functions in needed sequencing"""

    global MOVES, field_list

    print(random.choice(phrases["begin"]), "\n", phrases["instruction"][0])

    if human_first:
        print(random.choice(phrases["humanFirst"]))
        show_field()
        human_turn()
        show_field()
    else:
        print(random.choice(phrases["computerFirst"]))
    while MOVES > 0:
        computer_turn()
        show_field()
        if choose_winner() != 0:
            print(choose_winner())
            break
        human_turn()
        show_field()
        if choose_winner() != 0:
            print(choose_winner())
            break

    play_again()


all_together()
