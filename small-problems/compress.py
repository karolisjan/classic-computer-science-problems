from sys import argv, getsizeof
from typing import Sequence


class CompressedGene:
	def __init__(self, gene: str) -> None:
		self.__compress(gene)
		
	def __compress(self, gene: str) -> None:
		self.__bit_string: int = 1 # sentinel

		for nucleotide in gene.upper():
			self.__bit_string <<= 2
			self.__bit_string |= self.nucleotide_to_bits(nucleotide)
			
	def decompress(self) -> str:
		gene: Sequence[str] = []
		n = self.__bit_string.bit_length() - 1 # exclude sentinel

		for i in range(0, n, 2):
			bits: int = self.__bit_string >> i & 0b11
			gene.append(self.bits_to_nucleotide(bits))
			
		return ''.join(gene)[::-1]
			
	@staticmethod
	def nucleotide_to_bits(nucleotide: str) -> int:
		bits = {
			'A': 0b00,
			'C': 0b01,
			'G': 0b10,
			'T': 0b11
		}.get(nucleotide, None)
		
		if bits is None:
			raise ValueError(f'Invalid nucleotide: {nucleotide}')
		return bits
		
	@staticmethod
	def bits_to_nucleotide(bits: int) -> str:
		nucleotide = {
			0b00: 'A',
			0b01: 'C',
			0b10: 'G',
			0b11: 'T'
		}.get(bits, None)
		
		if nucleotide is None:
			raise ValueError(f'Invalid bits: {bits}')
		return nucleotide
		
	def __str__(self) -> str:
		return self.decompress()
		
	@property
	def size(self):
		return getsizeof(self.__bit_string)


if __name__ == '__main__':
	uncompressed_gene = argv[1]
	compressed_gene = CompressedGene(uncompressed_gene)

	print(f'Size before compression: {getsizeof(uncompressed_gene)} b')
	print(f'Size after compression: {compressed_gene.size} b')
	print(f'Original and decompressed are the same: {uncompressed_gene == compressed_gene.decompress()}')
