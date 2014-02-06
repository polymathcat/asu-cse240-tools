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
__copyright__   = "Copyright 2011-2014, Ruben Acuna"

import os

####################################################
##################### SETTINGS #####################
####################################################
base_file = "HW02_02_Base.c"

####################################################
####################### MAIN #######################
####################################################
if base_file[-2:] == ".c":
    type = "c"
elif base_file[-4:] == ".cpp":
    type = "cc"
elif base_file[-4:] == ".rkt":
    type = "scheme"

output = "./mossnet -l "+type

if base_file:
    output += " -b "+base_file+" "

dir = os.getcwd()

exclude = ["mossnet", "mossprep.py", base_file]

for name in [x for x in os.listdir(dir) if not x in exclude]:
    os.rename(name, name.replace(" ", "_"))
    name = name.replace(" ", "_")
    os.rename(name, name.replace("(", "_"))
    name = name.replace("(", "_")
    os.rename(name, name.replace(")", "_"))
    name = name.replace(")", "_")
    
    output = output + name + " "

print "The correct MOSS command is:"
print output
