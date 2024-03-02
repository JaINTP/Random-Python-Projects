"""
This module facilitates the creation and interaction with a maze game,
allowing users to navigate through mazes.

Classes:
    Maze: Manages the structural details of a maze, including its layout and player positioning.
    MazeGame: Orchestrates game dynamics such as maze navigation, progress tracking, and win
              condition verification.
"""

import argparse
from dataclasses import dataclass, field
from typing import List
import os
import sys
from maze_gen import MazeGenerator, MazeProperties

@dataclass
class Maze:
    """
    Holds the structure and player information of a maze.

    Attributes:
        layout: A matrix representation of the maze where each cell can be a path, wall,
                start, or exit.
        width: The total number of columns in the maze.
        height: The total number of rows in the maze.
        start_x: The column index where the player starts.
        start_y: The row index where the player starts.
        player_x: The current column index of the player within the maze.
        player_y: The current row index of the player within the maze.
    """
    layout: List[List[str]] = field(default_factory=list)
    width: int = 0
    height: int = 0
    start_x: int = 0
    start_y: int = 0
    player_x: int = 0
    player_y: int = 0

class MazeGame:
    """
    Manages the gameplay logic, including maze loading, player movement, and victory checks.

    Methods:
        load_maze_from_file: Reads a maze layout from a file and initializes the game state.
        display_maze: Outputs the current state of the maze with the player's location.
        move_player: Updates the player's position based on input directions.
        check_win_condition: Determines if the player has reached the maze's exit.
        play: Launches the game, processing user input for navigation until the game concludes.
    """

    def __init__(self, filename: str):
        """
        Prepares the game environment by loading a maze from the given filename.

        Args:
            filename: Path to a file containing the desired maze layout.
        """
        self.maze = Maze()
        self.load_maze_from_file(filename)

    def load_maze_from_file(self, filename: str):
        """
        Populates the game's maze structure from a file, accommodating various file formats.

        Args:
            filename: Path to the maze layout file.
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")

        if os.path.getsize(filename) == 0:
            raise ValueError(f"The file '{filename}' is empty.")

        with open(filename, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()
            try:
                self.maze.height, self.maze.width = map(int, first_line.split())
                layout_lines = file.readlines()
            except ValueError:
                layout_lines = [first_line] + file.readlines()
                self.maze.height = len(layout_lines)
                self.maze.width = len(layout_lines[0].rstrip())

            self.maze.layout = [list(line.strip()) for line in layout_lines]
            for y, line in enumerate(layout_lines):
                if 'S' in line:
                    self.maze.start_x, self.maze.start_y = line.index('S'), y
                    self.maze.player_x, self.maze.player_y = self.maze.start_x, self.maze.start_y

    def display_maze(self):
        """
        Displays the maze with the player's current location marked distinctly.
        """
        for y, row in enumerate(self.maze.layout):
            for x, char in enumerate(row):
                if x == self.maze.player_x and y == self.maze.player_y:
                    print('X', end='')
                else:
                    print(char, end='')
            print()

    def move_player(self, direction: str) -> str:
        """
        Adjusts the player's position based on a specified direction if the move is permissible.

        Args:
            direction: A character indicating the desired direction ('W', 'A', 'S', 'D').

        Returns:
            A message indicating the move's result, or None if successful.
        """
        dx, dy = 0, 0
        if direction.upper() == 'W':
            dy = -1
        elif direction.upper() == 'S':
            dy = 1
        elif direction.upper() == 'A':
            dx = -1
        elif direction.upper() == 'D':
            dx = 1
        else:
            return

        new_x, new_y = self.maze.player_x + dx, self.maze.player_y + dy
        if 0 <= new_x < self.maze.width and 0 <= new_y < self.maze.height:
            if self.maze.layout[new_y][new_x] != '#':
                self.maze.player_x, self.maze.player_y = new_x, new_y
                return None
            return "Invalid move: you can't move through walls."
        return "Invalid move: you can't move out of bounds."

    def check_win_condition(self) -> bool:
        """
        Evaluates if the player has successfully reached the maze's exit.

        Returns:
            True if the player's current position is the exit, False otherwise.
        """
        return self.maze.layout[self.maze.player_y][self.maze.player_x] == 'E'

    def _clear_terminal(self):
        """
        Clears the console screen to refresh the game's visual presentation.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def play(self, refresh: bool = False):
        """
        Initiates and maintains the game loop, accepting and processing player inputs.

        Args:
            refresh: Whether to clear the screen after each move to keep the display uncluttered.
        """
        self._clear_terminal()
        print(f"Welcome to the Maze Game! (W, A, S, D to move." \
              f"{" M for Map" if not refresh else ""})")
        self.display_maze()

        while not self.check_win_condition():
            move = input(f"Next move (W/A/S/D/{'M/' if not refresh else ''}Q): ").strip()

            top_msg = ''

            if move.upper() == 'M' and not refresh:
                self.display_maze()
            elif move.upper() == 'Q':
                print("Quitting game.")
                return
            elif move.upper() not in ('W', 'A', 'S', 'D', 'M', 'Q'):
                top_msg = "Invalid input: please use W, A, S, D, M, or Q."

            if move.upper() in ('W', 'A', 'S', 'D'):
                top_msg = self.move_player(move)

            if refresh:
                self._clear_terminal()
                print(top_msg if top_msg is not None else '')
                self.display_maze()
            else:
                print(top_msg if top_msg is not None else '')

            if self.check_win_condition():
                print("Congratulations! You've found the exit and won the game.")
                break

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Maze Game: Navigate through the maze to find the exit.")
    argparser.add_argument("maze_file",
                           help="File containing the maze layout.")
    argparser.add_argument("--refresh", action="store_true",
                           help="Refresh the display after each move.")
    argparser.add_argument("--generate", action="store_true",
                           help="Generate a new maze and save to the specified file.")
    argparser.add_argument("--version", action="version", version="Maze Game 1.0")

    args = argparser.parse_args()

    if args.generate:
        if os.path.exists(args.maze_file):
            to_overwrite = input(f"The file '{args.maze_file}' " \
                                 "already exists. Overwrite it? [Y/N]: ")
            if to_overwrite.upper() != 'Y':
                print("Exiting without generating a new maze.")
                sys.exit()

        size = input("Enter the dimensions (from 5 to 100) of the maze to generate (e.g. 10): ")
        maze_properties = MazeProperties(size=int(size))
        maze = MazeGenerator(maze_properties)
        maze.generate_maze()
        maze.write_to_file(args.maze_file)

    game = MazeGame(args.maze_file)
    game.play(args.refresh)
