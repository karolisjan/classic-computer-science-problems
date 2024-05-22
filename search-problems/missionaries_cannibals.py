from __future__ import annotations
from typing import List, Optional
from enum import Enum

from generic_search import Node, bfs, node_to_path


class RiverBank(Enum):
	WEST = True
	EAST = False


class ProblemState:
	def __init__(
			self,
			missionaries: int,
			cannibals: int,
			boat: bool,
			max_num: int = 3
		) -> None:
			self.wm: int = missionaries  # west bank missionaries
			self.wc: int = cannibals  # west bank cannibals
			self.boat: bool = boat  # west if True else ease
			self.em: int = max_num - missionaries  # east bank missionaries
			self.ec: int = max_num - cannibals  # east bank cannibals
			self.max_num: int = max_num  # maximum number of the bank
			
	@property
	def is_legal(self) -> bool:
		if self.wm < self.wc and self.wm > 0:
			return False
			
		if self.em < self.ec and self.em > 0:
			return False
			
		return True
			
	def goal_test(self) -> bool:
		return self.is_legal and self.em == self.max_num and self.ec == self.max_num
		
	def successors(self) -> List[ProblemState]:
		successors: List[ProblemState] = []
		
		if self.boat == RiverBank.WEST:
			if self.wm > 1:
				successors.append(ProblemState(self.wm - 2, self.wc, RiverBank.EAST))
			if self.wm > 0:
				successors.append(ProblemState(self.wm - 1, self.wc, RiverBank.EAST))
			if self.wc > 1:
				successors.append(ProblemState(self.wm, self.wc - 2, RiverBank.EAST))
			if self.wc > 0:
				successors.append(ProblemState(self.wm, self.wc - 1, RiverBank.EAST))
			if self.wm > 0 and self.wc > 0:
				successors.append(ProblemState(self.wm - 1, self.wc - 1, RiverBank.EAST))

		if self.boat == RiverBank.EAST:
			if self.em > 1:
				successors.append(ProblemState(self.wm + 2, self.wc, RiverBank.WEST))
			if self.em > 0:
				successors.append(ProblemState(self.wm + 1, self.wc, RiverBank.WEST))
			if self.ec > 1:
				successors.append(ProblemState(self.wm, self.wc + 2, RiverBank.WEST))
			if self.ec > 0:
				successors.append(ProblemState(self.wm, self.wc + 1, RiverBank.WEST))
			if self.em > 0 and self.ec > 0:
				successors.append(ProblemState(self.wm + 1, self.wc + 1, RiverBank.WEST))
				
		return [x for x in successors if x.is_legal]
			
	def __str__(self) -> str:
		return '\n'.join([
				f'On the west bank there are {self.wm} missionaries and {self.wc} cannibals.',
				f'On the east bank there are {self.em} missionaries and {self.ec} cannibals.',
				f'The boat is on the {"west" if self.boat == RiverBank.WEST else "east"} bank.'
			])
			
			
def display_solution(path: List[ProblemState]) -> None:
	if len(path) == 0:
		return
		
	old_state: ProblemState = path[0]
	print(old_state)
	
	for state in path[1:]:
		if state.boat == RiverBank.WEST:
			print(f'{old_state.em - state.em} missionaries and {old_state.ec - state.ec} cannibals moved from the east to the west bank.\n')
		else:
			print(f'{old_state.wm - state.wm} missionaries and {old_state.wc - state.wc} cannibals moved from the west to the east bank.\n')
		print(state)
		old_state = state	
			
			
if __name__ == '__main__':
	start: ProblemState = ProblemState(3, 3, RiverBank.WEST)
	solution: Optional[Node[ProblemState]] = bfs(start, ProblemState.goal_test, ProblemState.successors)
	
	if solution is None:
		print('No solution found!')
	else:
		path: List[ProblemState] = node_to_path(solution)
		display_solution(path)
	
