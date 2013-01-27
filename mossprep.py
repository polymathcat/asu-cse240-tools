#!/usr/bin/env python

"""mossprep.py: Automatically generates the command for running MOSS on every file in the folder."""

__author__      = "Ruben Acuna"
__copyright__   = "Copyright 2011-2013, Ruben Acuna"

import os

####################################################
##################### SETTINGS #####################
####################################################
base_file = "Base_HW05_Q01.cpp"


if base_file[-2:] == ".c":
    type = "c"
elif base_file[-2:] == ".cpp":
    type = "cc"
elif base_file[-2:] == ".rkt":
    type = "scheme"

output = "./moss -l "+type

if base_file:
    output += " -b "+base_file+" "

dir = os.getcwd()

for name in [x for x in os.listdir(dir) if "."+os.path.splitext(base_file)[1] in x and not base_file == x]:
    output = output + name + " "

print output