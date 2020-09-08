
import sqlite3
import atexit
import os
import sys

# checks if DB is already exists.

DBExist = os.path.isfile('schedule.db')

dbcon = sqlite3.connect('schedule.db')
cursor = dbcon.cursor()


def close_db():
    dbcon.commit()
    dbcon.close()


atexit.register(close_db)


def create_tables():

    cursor.execute(""" CREATE TABLE courses(id INTEGER PRIMARY KEY,
                                          course_name TEXT NOT NULL,
                                          student TEXT NOT NULL,
                                          number_of_students INTEGER NOT NULL,
                                          class_id INTEGER REFERENCES classrooms(id),
                                          course_length INTEGER NOT NULL)
                    """)

    cursor.execute(""" CREATE TABLE students(grade TEXT PRIMARY KEY,
                                            count INTEGER NOT NULL)
                   """)

    cursor.execute(""" CREATE TABLE classrooms(id INTEGER PRIMARY KEY,
                                               location TEXT NOT NULL, 
                                               current_course_id INTEGER NOT NULL,
                                               current_course_time_left INTEGER NOT NULL)
                   """)


def insert_data(argv):
    inputfilename = argv[1]


    # opening the config file:
    with open(inputfilename) as inputfile:

    # iterating the config file line by line, adding the matching records:
        for line in inputfile:
            # split the record arguments
            line = line.strip('\n')
            splittedLine = line.split(',')
            for word in splittedLine:
                word = word.strip(' ')
            recordType = splittedLine[0]
            if recordType is 'C':
                insert_course(splittedLine)

            elif recordType is 'S':
                insert_student(splittedLine)

            elif recordType is 'R':
                insert_classroom(splittedLine)




def insert_course(line):
    courseID = line[1].strip(" ")
    courseName = line[2].strip(" ")
    studentType = line[3].strip(" ")
    numOfStudents = line[4].strip(" ")
    classID = line[5].strip(" ")
    courseLength = line[6].strip(" ")
    cursor.execute("INSERT INTO courses VALUES (?, ?, ?, ?, ?, ?)", [courseID,courseName,studentType,numOfStudents,classID,courseLength])


def insert_student(line):
    grade = line[1].strip(" ")
    count = line[2].strip(" ")
    cursor.execute("INSERT INTO students VALUES (?, ?)", [grade,count])

def insert_classroom(line):
    id = line[1].strip(" ")
    location = line[2].strip(" ")
    current_course_id = 0
    current_course_time_left = 0
    cursor.execute("INSERT INTO classrooms VALUES (?, ?, ?, ?)", [id, location, current_course_id, current_course_time_left])





def print_table_as_a_table(table):
    cursor.execute('SELECT * FROM ' + table);
    list = cursor.fetchall()
    print(table)
    for item in list:
     print(item)


def main(argv):

    if not DBExist:
        create_tables()
        insert_data(argv)

    print_table_as_a_table("courses")
    print_table_as_a_table("classrooms")
    print_table_as_a_table("students")


if __name__ == '__main__':
    main(sys.argv)
