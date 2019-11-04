'''
	A one-time pad.
	
	Encrypts a piece of data by combining it
	with random dummy data in such a way that 
	the original cannot be reconstituted without
	access to both the product and the dummy
	data.
'''
from typing import Tuple
from secrets import token_bytes


def random_key(length: int) -> int:
	tb: bytes = token_bytes(length)
	# 'big' refers to the endianness of
	# bytes: byte-ordering - does the
	# most significant byte come first or
	# does the least significant byte
	# come first?
	return int.from_bytes(tb, 'big')
	

def encrypt(original: str) -> Tuple[int, int]:
	'''
		A ^ B = C
		C ^ A = B
		C ^ B = A
	'''
	original_bytes: bytes = original.encode()
	dummy: int = random_key(len(original_bytes))
	original_key: int = int.from_bytes(original_bytes, 'big')
	encrypted: int = original_key ^ dummy # XOR
	return dummy, encrypted


def decrypt(key1: int, key2: int) -> str:
	decrypted: int = key1 ^ key2 
	# Add 7 to the length of the decrypted data
	# before using integer division to divide by
	# 8 to ensure we 'round up', to avoid an 
	# off-by-one error.
	temp: bytes = decrypted.to_bytes(
		(decrypted.bit_length() + 7) // 8,
		'big'
	)
	return temp.decode()


if __name__ == '__main__':
	key1, key2 = encrypt('One Time Pad')
	result: str = decrypt(ke1, key2)
	print(key1, key2)
	print(result)
