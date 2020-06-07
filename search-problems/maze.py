from enum import Enum
from typing import (List, NamedTuple, Callable, Optional)

import random
from math import sqrt


class Cell(str, Enum):
	EMPTY = " "
	BLOCKED = "X"
	START = "S"
	GOAL = "G"
	PATH = "*"


class MazeLocation(NamedTuple):
	row: int
	column: int


class Maze:
	def __init__(
		self,
		rows: int = 20,
		columns: int = 40,
		sparseness: float = 0.2,
		start: MazeLocation = MazeLocation(0, 0),
		goal: MazeLocation = MazeLocation(9, 9)
	) -> None:
		# Initialize basic instance variables
		self._rows: int = rows
		self._columns: int = columns
		self.start: MazeLocation = start
		self.goal: MazeLocation = goal
		
		# Fill the grid with empty cells
		self._grid: List[List[Cell]] = [[
			Cell.EMPTY for column in range(columns)
		] for row in range(rows)]

		# Populate the grid with blocked cells
		self._randomly_fill(rows, columns, sparseness)

		# Fill the start and goal locations in
		self._grid[start.row][start.column] = Cell.START
		self._grid[goal.row][goal.column] = Cell.GOAL

	def _randomly_fill(
		self,
		rows: int,
		columns: int,
		sparseness: float
	) -> None:
		for row in range(rows):
			for column in range(columns):
				if random.uniform(0, 1.0) < sparseness:
					self._grid[row][column] = Cell.BLOCKED

	def successors(self, ml: MazeLocation) -> List[MazeLocation]:
		'''
			successors() simply checks above, below, to the right, and to the left of a MazeLocation in a Maze to see if it can find empty spaces that can be gone to from that location. It also avoids checking locations beyond the edges of the Maze. It puts every possible MazeLocation that it finds into a list that it ultimately returns to the caller.
		'''
		locations: List[MazeLocation] = []
		if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
			locations.append(MazeLocation(ml.row + 1, ml.column))
		if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
			locations.append(MazeLocation(ml.row - 1, ml.column))
		if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
			locations.append(MazeLocation(ml.row, ml.column + 1))
		if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
			locations.append(MazeLocation(ml.row, ml.column - 1))
		return locations

	def __str__(self) -> str:
		'''
			Returns a nicely formatted vesion of the maze for
			printing.
		'''
		output: str = ""
		for row in self._grid:
			output += "".join([
				column.value for column in row
			])
			output += "\n"
		return output

	def goal_test(self, ml: MazeLocation) -> bool:
		return ml == self.goal


if __name__ == "__main__":
	maze: Maze = Maze()
	print(maze)

