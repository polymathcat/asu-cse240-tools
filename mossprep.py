#!/usr/bin/env python

"""mossprep.py: Automatically generates the command for running MOSS on every
                source file in the current folder.

                Requires a folder of source files and a base code file (see
                settings below). The language will be inferred from the
                extension of the base file.

                Prints a complete MOSS command for analyzing all files together.
                Example: ./moss -l c -b HW02_Base.c Name1_HW02.c Name2_HW02.c ...
                """

__author__      = "Ruben Acuna"
__copyright__   = "Copyright 2011-2013, Ruben Acuna"

import os

####################################################
##################### SETTINGS #####################
####################################################
base_file = "HW02_Programming.c"


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

for name in [x for x in os.listdir(dir) if  not base_file == x and not ".py" in x]:
    output = output + name + " "

print "The correct MOSS command is:"
print output
