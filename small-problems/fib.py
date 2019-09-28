import sys
from typing import Dict, Callable


def memoize(func: Callable[[int], int]) -> Callable[[int], int]:
	memo: Dict[int, int] = {}
	
	def wrapper(n: int) -> int:
		if n not in memo:
			memo[n] = func(n)
		return memo[n]
	return wrapper


class Memoize:
	def __init__(self, func: Callable[[int], int]) -> None:
		self.func: Callable[[int], int] = func
		self.memo: Dict[int, int] = {0: 0, 1: 1}
		
	def __call__(self, n: int) -> int:
		if n not in self.memo:
			self.memo[n] = self.func(n)
		return self.memo[n]


@memoize
def fib(n: int) -> int:
	if n < 2:
		return n
	return fib(n - 1) + fib(n - 2)


@Memoize
def fib2(n: int) -> int:
	if n < 2: 
		return n
	return fib(n - 1) + fib(n - 2)	


if __name__ == '__main__':
	n = int(sys.argv[1])
	print(fib(n))
	print(fib2(n))
