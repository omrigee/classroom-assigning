import sqlite3
import os
import atexit

DBExist = os.path.isfile('schedule.db')
dbcon = sqlite3.connect('schedule.db')
cursor = dbcon.cursor()


def print_table_as_a_table(table):
    cursor.execute('SELECT * FROM ' + table);
    list = cursor.fetchall()
    print(table)
    for item in list:
     print(item)


def close_db():
    dbcon.commit()
    dbcon.close()


atexit.register(close_db)


def main():
    # Checks if there is any courses in the courses table, if courses table is empty, wont enter the 'while' loop:
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    courseListLength = len(courses)
    iteration = 0
    enteredLoop = False

    while courseListLength > 0 and DBExist:
        enteredLoop = True
        cursor.execute("SELECT * FROM classrooms")
        classrooms = cursor.fetchall()

        for item in classrooms:
            # CLASSROOMS WITH 1 HOUR LEFT IN COURSE:
            if item[3] == 1:
                cursor.execute("SELECT * FROM courses WHERE id={}".format(item[2]))
                course = cursor.fetchone()
                print("({}) {}: {} is done".format(iteration, item[1], course[1]))
                cursor.execute("UPDATE classrooms  SET current_course_time_left={} WHERE id={} ".format(0, item[0]))
                cursor.execute("UPDATE classrooms SET current_course_id={} WHERE id={}".format(0, item[0]))
                cursor.execute("DELETE FROM courses WHERE id={}".format(item[2]))
                item = list(item)
                item[3] = 0
                courseListLength = courseListLength-1
            # OCCUPIED CLASSROOMS (time left in course > 1):
            if item[3] > 1:
                cursor.execute("SELECT * FROM courses WHERE id={}".format(item[2]))
                course = cursor.fetchone()
                print("({}) {}: occupied by {}".format(iteration, item[1], course[1]))
                cursor.execute("UPDATE classrooms  SET current_course_time_left={} WHERE id={} ".format(item[3] - 1, item[0]))


            # AVAILABLE CLASSROOMS (time left in course = 0):
            if item[3] == 0:
                # means this classroom(item) is available, need to assign a course
                cursor.execute("SELECT * FROM courses WHERE class_id=({})".format(item[0]))
                courseOfAvailableRoom = cursor.fetchone()
                if not courseOfAvailableRoom is None:
                    print("({}) {}: {} is schedule to start".format(iteration, item[1], courseOfAvailableRoom[1]))
                    courseToBeginID = courseOfAvailableRoom[0]
                    courseToBeginLength = courseOfAvailableRoom[5]
                    cursor.execute(
                        "UPDATE classrooms SET current_course_id={} WHERE id={}  ".format(courseToBeginID, item[0]))
                    cursor.execute(
                        "UPDATE classrooms  SET current_course_time_left={} WHERE id={} ".format(courseToBeginLength,
                                                                                                 item[0]))
                    courseToBeginStudentType = courseOfAvailableRoom[2]
                    courseToBeginAmountOfStudents = courseOfAvailableRoom[3]

                    cursor.execute("SELECT * FROM students WHERE grade='{}'".format(courseToBeginStudentType))
                    students = cursor.fetchone()
                    currentStudentNumber = students[1]
                    cursor.execute("UPDATE students SET count=({}) WHERE grade=('{}') ".format(
                        currentStudentNumber - courseToBeginAmountOfStudents, courseToBeginStudentType))


        # end of the loop, needs to print tables:
        print_table_as_a_table("courses")
        print_table_as_a_table("classrooms")
        print_table_as_a_table("students")


        iteration = iteration + 1


    if not enteredLoop:
       print_table_as_a_table("courses")
       print_table_as_a_table("classrooms")
       print_table_as_a_table("students")

if __name__ == "__main__":
    main()
