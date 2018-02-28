#!/usr/bin/env python3

""" Hangman in Python (2.7.x upwards) with ncurses """

from curses import wrapper
import random
import re


#TODO Streamline ASCII imgs
def display_stage(stage, stdscr):
    """ Display ASCII hangman """
    with open('hangmans/{}.txt'.format(stage), 'r') as hangman_stage:
        for line in hangman_stage:
            stdscr.addstr(line)

def get_secret():
    """ Get secret word """
    with open('/usr/share/dict/words') as dictionary:
        word_list = dictionary.read().splitlines()
        secret = ''
        while len(secret) < 3 and secret[-2::] != 'ed':
            # Get random word from dictionary, remove "'s" pattern if present
            secret = word_list[random.randint(0, len(word_list)-1)].replace("'s", "")
        return secret

def unveil_secret(unveiled_secret, secret, guess):
    """ Unveil secret word as user guesses correctly """
    for idx, _ in enumerate(secret):
        if secret[idx] == guess:
            unveiled_secret[idx] = guess

    return unveiled_secret

def main(stdscr):
    """ Main loop """
    turn = 0
    max_chances = 6
    chances_left = max_chances
    secret = get_secret()
    consumed_secret = secret
    unveiled_secret = ['#' for _ in range(len(secret))]
    used_guesses = []

    while chances_left:
        stdscr.clear()
        announcement = 'Turn: {}. Chances left: {}. Guesses: {}\n'.format(
            turn + 1,
            chances_left,
            used_guesses
        )
        stdscr.addstr(announcement)
        unveiled_secret_str = ''.join(elem for elem in unveiled_secret)
        stdscr.addstr("Secret word: {}\n".format(unveiled_secret_str))

        guess = stdscr.getkey().lower()
        while len(guess) != 1:
            stdscr.addstr('Insert a char here...\n')
            guess = stdscr.getkey().lower()
            stdscr.addstr('Tip: Insert 1 (ONE) character. \n')
            stdscr.refresh()

        if guess in used_guesses:
            used_guesses_str = ', '.join(character for character in used_guesses)
            stdscr.addstr('You already tried that letter!\n')
            stdscr.addstr('Tip: Already used guesses are: {}\n'.format(used_guesses_str))
            stdscr.refresh()
        else:
            used_guesses += [guess]
            if guess in consumed_secret:
                pattern = r'[{}{}]'.format(guess.lower(), guess.upper())
                consumed_secret = re.sub(pattern, '', consumed_secret)
                unveiled_secret = unveil_secret(unveiled_secret, secret, guess)
            else:
                chances_left -= 1
        turn += 1

        stdscr.refresh()

        if not consumed_secret:
            stdscr.addstr('Congrats! You won!\n')
            break
    stdscr.addstr('The answer was {}. Press any key to exit.\n'.format(secret))
    stdscr.refresh()
    stdscr.getch()

wrapper(main)
