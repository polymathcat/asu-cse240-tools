#!/usr/bin/env python

"""commentgen.py: Automatically generates comments from the CSE240 grading spreadsheet."""

__author__      = "Ruben Acuna"
__copyright__   = "Copyright 2011-2013, Ruben Acuna"

def tag(text, t):
    return "<" + t + ">" + text + "</" + t + ">"

####################################################
##################### SETTINGS #####################
####################################################
hw = 1
parts = [1, 2]
section = "tr"


filename = "CSE240 - 2013 Spring - HW"+str(hw).zfill(2)+" - Sheet1.tsv"
file = open(filename, "r")
text = file.readlines()
text_separator = "\t"

dict_column_indices = {} #str->int
dict_comments = {} #str->int
dict_point_values = {} #int->int
number_of_questions = 0
section_questions = {}

#store mapping of columns to indices
for column_name, i in enumerate(text[0].split(text_separator)):
    i = i.rstrip()
    if not column_name in dict_column_indices:
        dict_column_indices[i] = column_name;
    else:
        print "ERROR: two columns have identical names"

#determine number of questions
for column_name in dict_column_indices.keys():
    if "_final" in column_name:
        id = int(column_name.split("_")[0][1:])
        if id > number_of_questions:
            number_of_questions = id

#store comments from second row
row_comments = [x.strip() for x in text[1].split(text_separator)]
for column_name in dict_column_indices.keys():
    if not column_name in dict_comments:

        dict_comments[column_name] = row_comments[dict_column_indices[column_name]]

#store point values from third row
row_point_value = [x.strip() for x in text[2].split(text_separator)]
for column_name in dict_column_indices.keys():
    if "_final" in column_name and not column_name in dict_point_values:
        id = int(column_name.split("_")[0][1:])
        dict_point_values[id] = int(row_point_value[dict_column_indices[column_name]])

#detect questions associated with different parts
for part in parts:
    x1 = dict_column_indices[str(part).zfill(2)+"_days_late"]

    if str(part+1).zfill(2)+"_days_late" in dict_column_indices:
        x2 = dict_column_indices[str(part+1).zfill(2)+"_days_late"]
    else:
        x2 = len(dict_column_indices.keys())

    for column_name in dict_column_indices.keys():
        if "_final" in column_name:

            if x1 <  dict_column_indices[column_name] < x2:

                id = int(column_name.split("_")[0][1:])

                if part in section_questions:
                    section_questions[part] += [id]
                else:
                    section_questions[part] = [id]

    section_questions[part].sort()

in_correct_section = False

for line in text[3:]:

    line = [x.strip() for x in line.split(text_separator)]

    if line[0] == "#"+section.upper()+" Section":
        in_correct_section = True
    elif line[0][0] == "#" and "Section" in line[0]:
        in_correct_section = False

    if not in_correct_section:
        continue

    if line == "" or line[0][0] == "#":
        continue

    user_name = line[dict_column_indices["Last Name"]] + ", " + line[dict_column_indices["First Name"]]
    feedback = ""

    for part in parts:
        col = dict_column_indices[str(part).zfill(2)+"_days_late"]
        if not line[col].strip() in [str(0), ""]:
            feedback += "<b>Part " + str(part).zfill(2) + " submission worth only " + str(100 - int(line[col]) * 10) + "% graded value due to submission time. </b>"

    feedback += "<ul>"

    #process each question
    for part in parts:
        for id in section_questions[part]:
            prefix = "q"+str(id)+"_"
            colnum_final = dict_column_indices[prefix+"final"]
            colnum_comment = dict_column_indices[prefix+"comment"]

            #process final score column
            feedback += tag("q"+str(id)+": " + line[colnum_final] + "/"+str(dict_point_values[id])+" ", "b")

            feedback += "<ul>"

            #process point loss columns
            columns_point_loss = []

            for column_name in dict_column_indices.keys():

                if prefix == column_name[:len(prefix)]:
                    postfix = column_name[len(prefix):]

                    if postfix in ["final", "compiles", "compiles_comment", "comment"]:
                        continue

                    if line[dict_column_indices[column_name]] != "":
                        feedback += tag("-"+ line[dict_column_indices[column_name]] + ": " + dict_comments[column_name], "li")

            #process comment columns
            for column_name in dict_column_indices.keys():

                if prefix[:-1]+"c_" == column_name[:len(prefix)+1]:
                    postfix = column_name[len(prefix):+1]

                    if not line[dict_column_indices[column_name]] in [str(0), ""]:

                        feedback += tag("Suggestion: " + dict_comments[column_name], "li")

            #check if this is a programming problem
            if "q"+str(id)+"_compiles" in dict_column_indices.keys():
                colnum_compiles = dict_column_indices["q"+str(id)+"_compiles"]
                colnum_compiles_comment = dict_column_indices["q"+str(id)+"_compiles_comment"]

                if line[colnum_compiles] != str(1):
                    feedback += tag(dict_comments["q"+str(id)+"_compiles_comment"]+" -"+str((1-float(line[colnum_compiles]))*100)+"% from base grade. ", "li")

                if line[colnum_compiles_comment] != "":
                    feedback += tag("Compiler/Parser explanation: "+ line[colnum_compiles_comment] + " ", "li")

            #process general comment column
            if line[colnum_comment] != "":
                feedback += tag("Question remark: "+ line[colnum_comment] + " ", "li")

            feedback += "</ul>"

    feedback += "</ul>"

    print "<h3>"+ user_name + "</h3>" + feedback
