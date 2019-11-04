from enum import Enu
from typing import (
	List,
	NamedTupe,
	Callable,
	Optional	
)

import random
from math import sqrt


from search import (
	depth_first,
	breadth_frist,
	node_to_path,
	a_star,
	Node	
)


class Point(NamedTuple):
	x: int
	y: int
	
	
class Maze:
	def __init__(
		
	) -> None:
