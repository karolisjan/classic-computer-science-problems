from __future__ import annotations
from typing import (
		Generic,
		List,
		T,
		Optional,
		Callable,
		Set,
		Deque,
		Dict
	)

from heapq import heappush, heappop

	
class Queue(Generic[T]):
	def __init__(self) -> None:
		self._queue: Deque[t] = Deque()
		
	@property
	def empty(self) -> bool:
		return not self._queue
		
	def push(self, item: T) -> None:
		self._queue.append(item)
		
	def pop(self) -> T:
		return self._queue.popleft()  # FIFO
		
	def __repr__(self) -> str:
		return repr(self._queue)


class Stack(Generic[T]):
	def __init__(self) -> None:
		self._stack: List[T] = []
		
	@property
	def empty(self) -> bool:
		return not self._stack
		
	def push(self, item: T) -> None:
		self._stack.append(item)
		
	def pop(self) -> T:
		return self._stack.pop()  # LIFO
		
	def __repr__(self) -> str:
		return repr(self._stack)


class PriorityQueue(Generic[T]):
	def __init__(self) -> None:
		self._container: List[T] = []
		
	@property
	def empty(self) -> bool:
		return not self._container
		
	def push(self, item: T) -> None:
		heappush(self._container, item)  # in by priority
		
	def pop(self) -> T:
		return heappop(self._container)  # out by priority
		
	def __repr__(self) -> str:
		return repr(self._container)
		

class Node(Generic[T]):
	def __init__(
			self, 
			state: T, 
			parent: Optional[Node], 
			cost: float = 0.0,
			heuristic: float = 0.0
		) -> None:
			self.state: T = state
			self.parent: Optional[Node] = parent
			self.cost = cost
			self.heuristic = heuristic
			
	def __lt__(self, other: Node) -> bool:
		return (self.cost + self.heuristic) < (other.cost + other.heuristic)
		

def dfs(
			initial: T,
			goal_test: Callable[[T], bool],
			successors: Callable[[T], List[T]]
		) -> Optional[Node[T]]:
			# frontier is where we've yet to go
			frontier: Stack[Node[T]] = Stack()
			frontier.push(Node(initial, None))
			
			# explored is where we've been
			explored: Set[T] = {initial}
			
			# keep going while there is more to explore
			while not frontier.empty:
				current_node: Node[T] = frontier.pop()
				current_state: T = current_node.state
				
				# if we found the goal, we're done
				if goal_test(current_state):
					return current_node
					
				# check where we can go next and haven't explored
				for child in successors(current_state):
					if child in explored:  # skip children we already explored
						continue
						
					explored.add(child)
					frontier.push(Node(child, current_node))
					
			return None  # went through everything and never found goal
			

def bfs(
		initial: T,
		goal_test: Callable[[T], bool],
		successors: Callable[[T], List[T]]
	) -> Optional[Node[T]]:
		# frontier is where we've yet to go
		frontier: Queue[Node[T]] = Queue()
		frontier.push(Node(initial, None))
		
		# explored is where we've been
		explored: Set[T] = {initial}
		
		# keep going while there is more to explore
		while not frontier.empty:
			current_node: Node[T] = frontier.pop()
			current_state: T = current_node.state
			
			# if we found goal, we're done
			if goal_test(current_state):
				return current_node
				
			# check where we can go next and haven't explored
			for child in successors(current_state):
				if child in explored:  # skip children we already explored
					continue
					
				explored.add(child)
				frontier.push(Node(child, current_node))
				
		return None  # went through everything and never found goal
			
			
def astar(
		initial: T,
		goal_test: Callable[[T], bool],
		successors: Callable[[T], List[T]],
		heuristic: Callable[[T], float]
	) -> Optional[Node[T]]:
		# frontier is where we've yet to go
		frontier: PriorityQueue = PriorityQueue()
		frontier.push(Node(initial, None, 0.0, heuristic(initial)))
		
		# explored is where we've been
		explored: Dict[T, float] = {initial: 0.0}
		
		while not frontier.empty:
			current_node: Node[T] = frontier.pop()
			current_state: T = current_node.state
			
			# if we found the goal, we're done
			if goal_test(current_state):
				return current_node
				
			# check where we can go next and haven't explored
			for child in successors(current_state):
				# 1 assumes a grid, need a cost function for
				# more sophisticated apps
				new_cost: float = current_node.cost + 1
				
				if child not in explored or explored[child] > new_cost:
					explored[child] = new_cost
					frontier.push(Node(
								child,
								current_node,
								new_cost,
								heuristic(child)
							)
						)

		return None  # went through everything and never found goal
			

def node_to_path(node: Node[T]) -> List[T]:
	path: List[T] = [node.state]
	
	# work backwards from end to front
	while node.parent is not None:
		node = node.parent
		path.append(node.state)
		
	path.reverse()
	return path

