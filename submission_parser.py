#!/usr/bin/env python

"""submission_parser.py: Automatically generates HTML files that lists submissions per question and with prompt. Also
                         attempts to generate spreadsheet framework (incomplete).

                         Requires student_information_<section>.xls to be in local folder, a copy of BlackBoard student
                         information spreadsheet which has been converted to ASCII. <section> is set in settings.

                         Parses Homework <hw>.01.download.xls, a copy of default BlackBoard submission spreadsheet which
                         has been converted to ASCII. <hw> is set in settings.

                         Produces hw<hw>_f_submissions_q<i>.html where <hw> is taken from the settings and <i> ranges
                         over the questions. Only tested with short answer and multiple choice.

                         """

__author__      = "Ruben Acuna"
__copyright__   = "Copyright 2011-2013, Ruben Acuna"

import sys

####################################################
##################### SETTINGS #####################
####################################################
hw_number = 2
section = "f"

text_separator = "\t"

#from stack overflow because of lazyness
def rchop(thestring, ending):
    if thestring.endswith(ending):
        return thestring[:-len(ending)]
    return thestring

class blackboard_tsv(object):
    def __init__(self, filename, student_information):

        self._students = [None] * len(student_information)
        self.columns = []
        column_indices = dict()

        file = open(filename, "r")
        lines = file.readlines()

        for key, i in enumerate(lines[0].split(text_separator)):
            i = i.strip("\"").strip().strip("\"").strip() #whatever man
            if not key in column_indices:
                column_indices[i] = key
                self.columns.append(i)
            else:
                print "ERROR: spreadsheet has duplicate column"
                exit()

        for line in lines[1:]:
            line_chunks = [chunk.strip("\"").strip().strip("\"").strip() for chunk in line.split(text_separator)]

            student = dict()

            for column_title in column_indices.keys():

                if not column_title in student:
                    student[column_title] = line_chunks[column_indices[column_title]]
                else:
                    print "ERROR: student has duplicate column"
                    exit()

            for j, sorted_student in enumerate(student_information):
                if student["Username"] == sorted_student["Username"]:
                    self._students[j]  = student
                    break

        file.close()

    def __iter__(self):
        return iter(self._students)

    def get_columns(self):
        return self.columns

    #sort_by_name

    def __getitem__(self, key):
        return self._students.__getitem__(key)

class QuestionShortAnswer(object):
    def __init__(self, id, prompt, possible_points):
        self._id = id
        self._prompt = prompt
        self._possible_points = possible_points

        self._column_letter = "?"

        self._comments = []
        self._deductions = ["incomplete"]

    def add_comment_column(self, comment):
        self._comments.append(comment)

    def add_deduction_column(self, deduction):
        self._deductions.append(deduction)

    def get_columns_needed(self):
        return 2 + len(self._comments) + len(self._deductions)

    def print_student_row(self, row_index, no_submission):
        #print "MEOW",
        sys.stdout.write("\t")
        sys.stdout.write("=" + self._possible_points)

        initial_column_id = ord(self._column_letter) + 1

        for deduction in self._deductions:
            sys.stdout.write("-" + chr(initial_column_id) + str(row_index))
            initial_column_id += 1

        for comment in self._comments:
            sys.stdout.write("\t")

        if not no_submission:
            for deduction in self._deductions:
                sys.stdout.write("\t")
        else:
            sys.stdout.write("\t")
            sys.stdout.write(str(self._possible_points))
            for deduction in self._deductions[1:]:
                sys.stdout.write("\t")

        sys.stdout.write("\t") #for comment column

    def print_columns(self):
        sys.stdout.write("\t")
        title = "q" + str(self._id)
        sys.stdout.write(title + "_final")

        for deduction in self._deductions:
            sys.stdout.write("\t")
            sys.stdout.write(title + "_" + deduction)

        for comment in self._comments:
            sys.stdout.write("\t")
            sys.stdout.write(title + "c_" + comment)

        sys.stdout.write("\t")
        sys.stdout.write(title + "_comment")

def results_extract_short_answer_questions(sheet, columns):
    questions = []

    #ex: 'Question ID 1', 'Question 1', 'Answer 1', 'Possible Points 1', 'Auto Score 1', 'Manual Score 1'
    while len(columns) > 0:

        id = int(columns[0].split(" ")[-1])
        prompt = sheet[1]["Question " + str(id)]
        value = sheet[1]["Possible Points " + str(id)]

        if columns[0] != "Question ID " + str(id) or \
           columns[1] != "Question " + str(id) or \
           columns[2] != "Answer " + str(id) or \
           columns[3] != "Possible Points " + str(id) or \
           columns[4] != "Auto Score " + str(id) or \
           columns[5] != "Manual Score " + str(id):
            print "ERROR: failed to parse short answer."
            exit()

        question = QuestionShortAnswer(id, prompt, value)
        questions.append(question)

        columns = columns[6:]

    return questions

def load_student_information():

    students = []
    column_indices = dict()

    file = open("student_information_"+section+".xls", "r")
    lines = file.readlines()

    for key, i in enumerate(lines[0].split(text_separator)):
        i = i.strip("\"").strip().strip("\"").strip() #whatever man
        if not key in column_indices:
            column_indices[i] = key

        else:
            print "ERROR: spreadsheet has duplicate column"
            exit()

    for line in lines[1:]:
        line_chunks = [chunk.strip("\"").strip().strip("\"").strip() for chunk in line.split(text_separator)]

        student = dict()

        for column_title in column_indices.keys():

            if not column_title in student:
                student[column_title] = line_chunks[column_indices[column_title]]
            else:
                print "ERROR: student has duplicate column"
                exit()

        students.append(student)

    file.close()

    return students

def print_grading_spreadsheet(questions_short_answer, student_information, submissions_short_answers):

    #print columns
    column_titles = ["Last Name", "First Name", "final_grade", "days_late"]
    sys.stdout.write(column_titles[0])
    for title in column_titles[1:]:
        sys.stdout.write("\t")
        sys.stdout.write(title)

    #PRINT QUESTIONS
    for question in questions_short_answer:
        question.print_columns()
    print

    #print student rows
    for i, student in enumerate(student_information): #HACK

        row_index = i + 2

        #fill out last name
        sys.stdout.write(student["Last Name"])

        #fill out first name
        sys.stdout.write("\t")
        sys.stdout.write(student["First Name"])

        #fill out formula for final_grade - sum of all questions
        sys.stdout.write("\t")
        sys.stdout.write("=(")

        sys.stdout.write(questions_short_answer[0]._column_letter + str(row_index))
        for question in questions_short_answer[1:]:
            sys.stdout.write("+" + question._column_letter + str(row_index))

        sys.stdout.write(")*(1-.1*D" + str(row_index) + ")")

        #?
        #for part 01
        student = submissions_short_answers[i]

        #fill out nothing for days_late
        sys.stdout.write("\t")
        sys.stdout.write("?")

        #fill out the formulas and default values for questions
        for question in questions_short_answer:
            #print "MEOW\t",
            if not student:
                question.print_student_row(row_index, True)
            else:
                question.print_student_row(row_index, False)

        #finish off the row with a newline
        print

def dump_short_answer_questions(bb_short_answers, hw_number, questions_short_answer, student_information):
    for question in questions_short_answer:
        answer_column = "Answer " + str(question._id)

        filename = "hw" + str(hw_number) +"_"+ section +"_submissions_q" + str(question._id) + ".html"
        file = open(filename, "w")

        file.write("<b><font size=\"6\">")
        file.write("Question #" + str(question._id) + ":")
        file.write("</font></b><br>\n")
        file.write(question._prompt + "<br>\n")

        for i, student in enumerate(bb_short_answers):

            #file.write("=======================================\n")
            file.write("<b><font size=\"5\">")
            file.write(student_information[i]["Last Name"] + ", " + student_information[i]["First Name"])
            file.write("</font></b><br>\n")

            if student:
                answer = student[answer_column].strip()

                if answer == "<Unanswered>":
                    answer = "Question opened, saved with blank answer, <i>and</i> not submitted." #sometimes doesn't work

                answer += "<br><br>\n";
                file.write(answer);

            else:
                file.write("HW not submitted.<br><br>\n")

            file.write("\n")

        file.close()

def process_homework(hw_number, question_deductions, question_comments, student_information):
    #goal: build inital online spread sheet from inputs as well as gradeable text
    bb_short_answers = blackboard_tsv("Homework " + str(hw_number) + ".01.download.xls", student_information)

    #PREPARE QUESTIONS
    #get short answer questions
    questions = results_extract_short_answer_questions(bb_short_answers, bb_short_answers.get_columns()[3:])

    #merge deductions with parsed short answer questions
    for question_id in question_deductions:
        for question in questions:
            if question._id == question_id:
                for deduction in question_deductions[question_id]:
                    question.add_deduction_column(deduction)

    #merge comments with parsed short answer questions
    for question_id in question_comments:
        for question in questions:
            if question._id == question_id:
                for comment in question_comments[question_id]:
                    question.add_comment_column(comment)

    #update column labels
    columns_consumed = 4 #from default 4 that will be printed

    for question in questions:
        letter = chr(columns_consumed + 1 + 64)

        question._column_letter = letter

        columns_consumed += question.get_columns_needed()

    #use at own risk - pending integration with commentgen.py so it doesn't have to manually detect columns.
    #print_grading_spreadsheet(questions, student_information, bb_short_answers)

    dump_short_answer_questions(bb_short_answers, hw_number, questions, student_information)

#class specific
student_information = load_student_information()

question_comments = dict()
question_comments[1] = ["shortdescript"]

question_deductions = dict()
question_deductions[2] = ["noname"]

process_homework(hw_number, question_deductions, question_comments, student_information)

