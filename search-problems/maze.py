from typing import List, NamedTuple, Callable, Optional
from enum import Enum
import random
from math import sqrt

from generic_search import Node, dfs, bfs, astar, node_to_path


class Cell(str, Enum):
	EMPTY = ' '
	BLOCKED =  'X'
	START = 'S'
	GOAL = 'G'
	PATH = '*'
	
	
class MazeLocation(NamedTuple):
	row: int
	column: int
	
	
class Maze:
	def __init__(
			self,
			rows: int = 10,
			columns: int = 10,
			sparseness: float = 0.2,
			start: MazeLocation = MazeLocation(0, 0),
			goal: MazeLocation = MazeLocation(9, 9)
		) -> None:
			self._rows: int = rows
			self._columns: int = columns
			self.start: MazeLocation = start
			self.goal: MazeLocation = goal
			self._grid: List[List[Cell]] = [
					[Cell.EMPTY for column in range(columns)]
					for row in range(rows)
				]
				
			self._random_fill(rows, columns, sparseness)
			self._grid[start.row][start.column] = Cell.START
			self._grid[goal.row][goal.column] = Cell.GOAL
	
	def _random_fill(
			self,
			rows: int,
			columns: int,
			sparsiness: float 
		) -> None:
			for row in range(rows):
				for column in range(columns):
					if random.uniform(0, 1.0) < sparsiness:
						self._grid[row][column] = Cell.BLOCKED
						
	def __str__(self) -> str:
		output: str = ''
		for row in self._grid:
			output += '|'.join([column.value for column in row])
			output += '\n'
		return output
		
	def goal_test(self, ml: MazeLocation) -> bool:
		return ml == self.goal
		
	def successors(self, ml: MazeLocation) -> List[MazeLocation]:
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
		
	def mark(self, path: List[MazeLocation]) -> None:
		for ml in path:
			self._grid[ml.row][ml.column] = Cell.PATH
			
		self._grid[self.start.row][self.start.column] = Cell.START
		self._grid[self.goal.row][self.goal.column] = Cell.GOAL
		
	def clear(self, path: List[MazeLocation]) -> None:
		for ml in path:
			self._grid[ml.row][ml.column] = Cell.EMPTY
		
		self._grid[self.start.row][self.start.column] = Cell.START
		self._grid[self.goal.row][self.goal.column] = Cell.GOAL
	
	
def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
	def distance(ml: MazeLocation) -> float:
		x_dist: int = ml.column - goal.column
		y_dist: int = ml.row - goal.row
		return sqrt((x_dist * x_dist) + (y_dist * y_dist))
	return distance	
	
	
def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
	def distance(ml: MazeLocation) -> float:
		x_dist: int = abs(ml.column - goal.column)
		y_dist: int = abs(ml.row - goal.row)
		return x_dist + y_dist
	return distance
	
					
if __name__ == '__main__':
	maze: Maze = Maze()
	print(maze)
	solution1: Optional[Node[MazeLocation]] = dfs(
			maze.start,
			maze.goal_test,
			maze.successors
		)

	if solution1 is None:
		print('No solution found using depth-first search')
	else:
		path1: List[MazeLocation] = node_to_path(solution1)
		maze.mark(path1)
		print(maze)
		maze.clear(path1)
		
	solution2: Optional[Node[MazeLocation]] = bfs(
			maze.start,
			maze.goal_test,
			maze.successors
		)

	if solution2 is None:
		print('No solution found using breadth-first search')
	else:
		path2: List[MazeLocation] = node_to_path(solution2)
		maze.mark(path2)
		print(maze)
		maze.clear(path2)

	solution3: Optional[Node[MazeLocation]] = astar(
			maze.start,
			maze.goal_test,
			maze.successors,
			manhattan_distance(maze.goal),
		)

	if solution3 is None:
		print('No solution found using A-star search')
	else:
		path3: List[MazeLocation] = node_to_path(solution3)
		maze.mark(path3)
		print(maze)
		maze.clear(path3)
