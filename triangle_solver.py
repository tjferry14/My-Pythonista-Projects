#/usr/bin/env python
# coding: utf-8

from math import sqrt

try:
    raw_input          # Python2
except NameError:
    raw_input = input  # Python3

try:
    hypo = raw_input('Do you know your hypotenuse? ').strip().lower()
    if hypo == 'yes':
        c = float(raw_input('Enter your hypotenuse: ').strip())
        q = float(raw_input('Enter your other side: ').strip())
        print (sqrt((c * c) - (q * q)))
    else:
        a = int(input('Enter your first number '))
        b = int(input('Enter your second number '))
        print (sqrt((a * a) + (b * b)))
except ValueError:
    print("Math domain error")
