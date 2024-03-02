# Maze Game README

## Overview
The Maze Game is a Python-based application that allows users to navigate through mazes. This game involves reading a maze layout from a file, displaying it, and allowing the user to move through the maze with the goal of finding the exit.

## Installation

No specific installation is required other than having Python installed on your system. Clone or download the repository to your local machine to get started.

## Requirements

- Python 3.x
- An environment where Python's standard libraries are available

## Classes

- `Maze`: Manages the structural details of a maze, including its layout and player positioning.
- `MazeGame`: Orchestrates game dynamics such as maze navigation, progress tracking, and win condition verification.

## Usage

### Running the Game

To start the game, navigate to the directory containing the game files and run:

```BASH
python maze_game.py <maze_file> [--refresh] [--generate] [--version]
```

Arguments:
- `<maze_file>`: Mandatory. The path to the file containing the maze layout.
- `--refresh`: Optional. If set, the display will refresh after each move to keep the display uncluttered.
- `--generate`: Optional. Generates a new maze and saves it to the specified file before starting the game.
- `--version`: Optional. Displays the version of the Maze Game.

### Controls

- Move using `W` (up), `A` (left), `S` (down), `D` (right).
- Press `M` to display the map (if `--refresh` is not used).
- Press `Q` to quit the game.

### Generating a Maze

If you use the `--generate` flag, you will be prompted to overwrite the file if it exists and to enter the dimensions for the new maze. The game will then generate a new maze based on your input and save it to the specified file.

## Customization

You can create custom mazes by editing the maze file directly. Ensure the maze layout follows the format expected by the game:
- `#` represents walls.
- ` ` (space) represents paths.
- `S` represents the start position.
- `E` represents the exit.

Make sure the maze is properly enclosed with walls and has a single start and exit point.

***

# Maze Generator README

## Overview
The Maze Generator is a Python module designed to create customizable mazes. It provides functionality for generating a maze with customizable characters for walls, paths, start, and end points. The module also includes capabilities to print the generated maze to the console and write it to a specified file, making it a versatile tool for creating mazes for games, simulations, or any application that requires maze generation.

## Installation

This module does not require installation beyond having Python installed on your system. Simply download or clone the repository containing the Maze Generator module to get started.

## Requirements

- Python 3.x
- No external libraries are required; the module uses standard Python libraries.

## Features

- Customizable maze size, ranging from 5x5 to 99x99.
- Customizable characters for maze walls, paths, start point, and end point.
- Maze generation using the Randomized Prim's algorithm.
- Ability to print the maze to the console.
- Ability to write the maze to a file.

## Usage

### Generating a Maze

Run the module from the command line, specifying the output file and any desired options:

```BASH
python maze_generator.py <output file> [options]
```

Options:
- `--size`: Specify the size of the maze (defaults to 10x10). Valid values are from 5 to 100.
- `--wall`: Character to represent the walls (defaults to '#').
- `--path`: Character to represent the paths (defaults to ' ').
- `--start`: Character to represent the start point (defaults to 'S').
- `--end`: Character to represent the end point (defaults to 'E').
- `--print`: Print the generated maze to the console.

### Example Command

To generate a 20x20 maze with custom characters and print it to the console:
```BASH
python maze_generator.py my_maze.txt --size 20 --wall 'W' --path '.' --start 'A' --end 'B' --print
```

This command generates a maze with the specified characteristics, prints it to the console, and writes it to `my_maze.txt`.

## Customization

The maze properties can be customized through the command line arguments as shown above. This allows for a wide range of maze appearances and structures, suitable for different applications and preferences.

***

## Contributing

Contributions to the Maze Game are welcome. Please ensure that any pull requests or issues are clearly described, replicable, and tested when applicable.

## License

This project is open-source and available under the MIT License. See the LICENSE file for more details.
