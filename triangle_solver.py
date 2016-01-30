# coding: utf-8

from math import * 

try:
	hypo = raw_input('Do you know your hypotenuse? ')

	if hypo == 'yes':
		c = input('Enter your hypotenuse')
		q = input('Enter your other side')
		print (sqrt( (c*c) - (q*q) ))

	else:
		a = input('Enter your first number') 
		b = input('Enter your second number')
		print (sqrt( (a * a) + (b * b) ))
	
except ValueError:
	print "Math domain error"
