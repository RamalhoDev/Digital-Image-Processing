from PIL import Image
from enum import IntEnum, auto, unique
from typing import Tuple, TypedDict, List, Union, Optional, Callable

@unique
class ezImageType(IntEnum):
	RGB = 0
	YIQ = auto()
	RGBA = auto()

class ezRGBType(TypedDict):
	r: int
	g: int
	b: int

class ezYIQType(TypedDict):
	y: int
	i: int
	q: int
	
class ezImage():
	size: Tuple[int, int]
	channels_qnt: int
	channels_size:	int
	L: int
	ezType: ezImageType
	bands: List[List[Union[ezRGBType, ezYIQType]]]

	def __init__(self, size: Tuple[int, int] = (0,0), channels_size: int = 8, channels_qnt: int = 3,  ezType: ezImageType = ezImageType.RGB):
		self.size = size
		self.channels_qnt = channels_qnt
		self.channels_size = channels_size
		self.L = 2 ** self.channels_size
		self.ezType = ezType
		
		y_line = []
		for i in range(size[0]):
			x_line= []
			for j in range(size[1]):
				x_line.append({ 'r': 0, 'g': 0, 'b':0 })
			y_line.append(x_line)
		self.bands = y_line
	
	# TODO: Redo this function. I think a better way to aproach this is by iterating in
	# the bands and givinhg just some the pixels accordingly to the kernel size.
	def apply(self, f: Callable, kernel_size: Tuple[Optional[int]] = tuple()):
		if kernel_size != tuple():
			return f(self, kernel_size)
		else:
			return f(self)

	@staticmethod
	def from_pil_image(image: Image.Image):
		if image.mode == "RGB":
			size = image.size
			iBands = image.getdata()
			iBands = list(map(lambda t: dict(r=t[0],g=t[1],b=t[2]), list(iBands)))
			bands = []
			for x in range(size[0]):
				y_line= []
				for y in range(size[1]):
					y_line.append(iBands[y*size[0] + x])
				bands.append(y_line)
			
			c = ezImage(size=size)
			c.bands = bands;
			return c
		assert False, "Error: Other PIL image mode is not implemented yet."

	def __str__(self):
		return f"ezImage(size:{self.size}, L:{self.L}({2}^{self.channels_size}), type: {self.ezType.name})"
	
	def extend_with_zero(self):
		assert False, "Error: Extending with zero is not implemented yet."