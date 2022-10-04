"""
This is the DRIVER file of the UTTT referee implementation for the WPI course 'CS 4341:
Introduction to Artificial Intelligence' running A term of the 2022-2023 academic year. Adapted from the Othello
referee code written by Dyllan Cole <dcole@wpi.edu>

File:   external_players.py
Author: William Babincsak <wbabincsak@wpi.edu>
Date:   3 September 2022
"""

import argparse
import os
import re
import sys
import random
from os import listdir
from os.path import isfile, join

from external_players import get_competitors
from game import Game

def clean():
    """
    Delete files maintained by Referee
    :return: None
    """
    print('cleaning...')
    patterns = [
        re.compile("move_file"),
        re.compile("(:?.*).go"),
        re.compile("end_game"),
        re.compile("first_four_moves")
    ]
    loc = os.path.abspath('referee.py')[0:-len('referee.py')]
    files = [f for f in listdir(loc) if isfile(join(loc, f))]
    for file in files:
        for pattern in patterns:
            if pattern.match(file):
                os.remove(file)



def main():
    """
    Main Referee function
    """


    # Read in arguments from command line
    parser = argparse.ArgumentParser(description="Referee a game of Othello between two programs")
    parser.add_argument("player_one", type=str, help="Group name of player one")
    parser.add_argument("player_two", type=str, help="Group name of player two")
    parser.add_argument("--time_limit", type=int, help="Time limit (default 10 seconds)", required=False)
    args = parser.parse_args(sys.argv[1:])


    # Select order randomly
    p1 = args.player_one
    p2 = args.player_two
    if random.choice([True, False]):
        # Swap p1 and p2
        p3 = p1
        p1 = p2
        p2 = p3

    # Clean any pre-existing files
    clean()

    # Create empty move_file
    open("move_file", "w").close()

    # Get the competitor functions
    # I recommend increasing the time limit for testing so that you have time to write moves into move_file yourself
    # use the --time_limit optional parameter in the command line to set the time limit
    time_limit = 10 if args.time_limit is None else args.time_limit
    f_p1, f_p2 = get_competitors(p1, p2, time_limit)

    # Run game
    game = Game(f_p1, f_p2, p1_name=p1, p2_name=p2, rand_start=True)
    game.run()


if __name__ == "__main__":
    try:
        main()
    except:
        print('________________')
    clean()
