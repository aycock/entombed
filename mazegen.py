#!/usr/bin/env python

# Python < 3
# see LICENSE file for licensing information

import random

def getrandombit():	return random.randint(0, 1)
def leftrandombit():	return getrandombit()
def rightrandombit():	return getrandombit()
def midrandombit():	return getrandombit()
def generated(x):	pass

def prrow(seed):
	PF12 = ''
	for i in range(8):
		if seed & 1:
			PF12 = 'XX' + PF12
		else:
			PF12 = '__' + PF12
		seed >>= 1
	PF012 = 'XXXX' + PF12

	print PF012, PF012[::-1]

# the mystery table from Entombed

MAGIC = {
	(0b00, 0b000):	1,
	(0b00, 0b001):	1,
	(0b00, 0b010):	1,
	(0b00, 0b011):	None,		# None == random bit
	(0b00, 0b100):	0,
	(0b00, 0b101):	0,
	(0b00, 0b110):	None,
	(0b00, 0b111):	None,

	(0b01, 0b000):	1,
	(0b01, 0b001):	1,
	(0b01, 0b010):	1,
	(0b01, 0b011):	1,
	(0b01, 0b100):	None,
	(0b01, 0b101):	0,
	(0b01, 0b110):	0,
	(0b01, 0b111):	0,

	(0b10, 0b000):	1,
	(0b10, 0b001):	1,
	(0b10, 0b010):	1,
	(0b10, 0b011):	None,
	(0b10, 0b100):	0,
	(0b10, 0b101):	0,
	(0b10, 0b110):	0,
	(0b10, 0b111):	0,

	(0b11, 0b000):	None,
	(0b11, 0b001):	0,
	(0b11, 0b010):	1,
	(0b11, 0b011):	None,
	(0b11, 0b100):	None,
	(0b11, 0b101):	0,
	(0b11, 0b110):	0,
	(0b11, 0b111):	0,
}

def rowgen(lastrows):
	# prepend and append random bits to last row
	lastrowpadded = leftrandombit()
	lastrowpadded <<= 8
	lastrowpadded |= lastrows[-1]
	lastrowpadded <<= 1
	lastrowpadded |= rightrandombit()

	# last two bits generated in current row, initial value = 10
	lasttwo = 0b10

	newrow = 0

	# iterate from 7...0, inclusive
	for i in range(7, -1, -1):
		threeabove = (lastrowpadded >> i) & 0b111

		newbit = MAGIC[lasttwo, threeabove]
		if newbit is None:
			newbit = midrandombit()
		newrow = (newrow << 1) | newbit

		lasttwo = ( (lasttwo << 1) | newbit ) & 0b11

	# hook for verification
	generated(newrow)

	# now do postprocessing
	lastrows.append(newrow)
	lastrows = lastrows[-11:]

	# condition 1
	history = [ b & 0xf0 for b in lastrows ]
	if 0 not in history:
		if sum( [ b & 0x80 for b in history ] ) == 0:
			#print 'pp 1'
			lastrows[-1] = 0

	# condition 2
	history = [ b & 0xf for b in lastrows[-7:] ]
	if 0 not in history:
		comparator = 0
		if len(lastrows) >= 9:
			comparator = lastrows[-9]
		if sum( [ b & 1 for b in history ] ) == (comparator & 1)*7:
			#print 'pp 2'
			lastrows[-1] &= 0xf0

	prrow(lastrows[-1])
	return lastrows
	
def mazegen():
	lastrows = [ 0 ]
	while True:
		lastrows = rowgen(lastrows)

if __name__ == '__main__':
	#random.seed(12345)
	mazegen()
