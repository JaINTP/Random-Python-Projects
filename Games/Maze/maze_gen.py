"""
A module for generating, printing, and writing mazes to files.

This module provides functionality to generate a maze with customizable characters
for walls, paths, start, and end points. It includes capabilities to print the maze
to the console and write it to a specified file.
"""

from dataclasses import dataclass
import argparse
import random

@dataclass
class MazeProperties:
    """
    Stores properties of a maze.

    Attributes:
        size (int): The size of the maze. Must be between 5 and 99. Defaults to 10.
        wall_char (str): Character used to represent walls. Defaults to '#'.
        path_char (str): Character used to represent paths. Defaults to ' '.
        start_char (str): Character used to represent the start point. Defaults to 'S'.
        end_char (str): Character used to represent the end point. Defaults to 'E'.
    """
    size: int = 10
    wall_char: str = '#'
    path_char: str = ' '
    start_char: str = 'S'
    end_char: str = 'E'

class MazeGenerator:
    """
    A class to generate, print, and write mazes to files based on customizable properties.

    Methods:
        generate_maze(): Generates a maze with the specified properties.
        print_maze(): Prints the maze to the console.
        write_to_file(filename): Writes the maze to a specified file.
    """

    def __init__(self, properties: MazeProperties):
        """
        Initializes the MazeGenerator with specific properties.

        Parameters:
            properties (MazeProperties): The properties of the maze.
        """
        self.properties = properties
        self.maze = []
        if self.properties.size not in range(4, 101):
            raise ValueError("Maze size must be in range 5 and 100.")

    def _get_neighbours(self, x: int, y: int, visited: set) -> list[tuple[int, int]]:
        """
        Find unvisited neighbours of a cell in the maze.

        Parameters:
            x, y (int): Coordinates of the current cell.
            visited (set): Set of visited cells.

        Returns:
            list[tuple[int, int]]: Coordinates for unvisited neighbours.
        """
        directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.properties.size
                and 0 <= ny < self.properties.size
                and (nx, ny) not in visited
                and self.maze[nx][ny] == self.properties.wall_char):
                neighbors.append((nx, ny))
        return neighbors

    def generate_maze(self):
        """
        Generate a square maze using the Randomized Prim's algorithm.
        """
        self.properties.size = max(5, min(self.properties.size | 1, 99))
        self.maze = [[self.properties.wall_char for _ in range(self.properties.size)]
                     for _ in range(self.properties.size)]

        stack = []
        visited = set()

        start = (0, 1)
        self.maze[start[0]][start[1]] = self.properties.start_char
        stack.append((start[0]+1, start[1]))
        visited.add((start[0]+1, start[1]))

        while stack:
            current = stack[-1]
            x, y = current
            self.maze[x][y] = self.properties.path_char
            neighbours = self._get_neighbours(x, y, visited)

            if neighbours:
                next_cell = random.choice(neighbours)
                visited.add(next_cell)
                wall_x, wall_y = (x + next_cell[0]) // 2, (y + next_cell[1]) // 2
                self.maze[wall_x][wall_y] = self.properties.path_char
                stack.append(next_cell)
            else:
                stack.pop()

        for x in range(self.properties.size-2, 0, -1):
            if self.maze[self.properties.size-2][x] == self.properties.path_char:
                self.maze[self.properties.size-1][x] = self.properties.end_char
                break

    def print_maze(self):
        """
        Print the maze to the console.
        """
        for row in self.maze:
            print(''.join(row))

    def write_to_file(self, filename:str="maze.txt"):
        """
        Write the maze to a file.

        Parameters:
            filename (str): The name of the file to write the maze to.

        Raises:
            IOError: If the file cannot be opened or written to.
        """
        try:
            with open(filename, "w", encoding="utf-8") as file:
                for row in self.maze:
                    file.write(''.join(row) + "\n")
        except IOError as e:
            print(f"Error writing to file {filename}: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a maze with customizable entrance, exit, path, and wall characters.')
    parser.add_argument('output', type=str,
                        help='Output file to write the maze to.')
    parser.add_argument('--size', type=int, default=10,
                        help='Size of the maze (between 5 and 100, inclusive).')
    parser.add_argument('--wall', default='#',
                        help='Character to represent the walls.')
    parser.add_argument('--path', default=' ',
                        help='Character to represent the paths.')
    parser.add_argument('--start', default='S',
                        help='Character to represent the start point.')
    parser.add_argument('--end', default='E',
                        help='Character to represent the end point.')
    parser.add_argument('--print', action='store_true',
                        help='Print the maze to the console.')

    args = parser.parse_args()
    maze_properties = MazeProperties(size=args.size, wall_char=args.wall,
                                     path_char=args.path, start_char=args.start,
                                     end_char=args.end)
    maze = MazeGenerator(maze_properties)
    maze.generate_maze()

    if args.print:
        maze.print_maze()

    maze.write_to_file(args.output)
