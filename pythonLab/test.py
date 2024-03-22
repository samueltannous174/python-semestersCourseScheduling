import random
from itertools import combinations
from os import path
import termcolor
import json
from datetime import time

import pprint

courses_by_year_and_semester = {}
courses_by_grade = {}
current_hours = 0
sem_free_days = {1: 1, 2:1, 3: 0}
maximum_number_of_credits = 18
number_of_semesters = 0
passed_grades = []
hours_by_semester = {1: 14, 2: 15, 3: 3}
max_number_of_semesters = 18
DAYS = ["M"]





def main():
    global passed_grades
    current_year = 2
    current_semester = 1
    making_student_plan()
    passed_grades = getting_passed_courses()
    semesters_and_years = list(courses_by_year_and_semester.keys())
    all_schedules = {}
    while True:
        chosen_number = int(input("please select number: "))
        if chosen_number == 1:
            print_study_plan()
        if chosen_number == 2:
            sudent_records_verify()
        if chosen_number == 3:
            student_study_plan([])
        if chosen_number == 4:
            ask_user_the_preferences()
        if chosen_number == 5:
            ask_user_number_of_semesters()
        if chosen_number == 6:
            count = 0
            str = input(f"want next semester (year={current_year},semester={current_semester})?")
            while not str=="no" and current_year < 6:
                count += 1
                if count > max_number_of_semesters:
                    print(f"you cant create more than {max_number_of_semesters}")
                    break
                current_schedule = schedule_planning(current_year, current_semester)
                all_schedules[(current_year, current_semester)] = current_schedule
                student_study_plan(current_schedule)
                if current_semester == 2:
                    current_semester += 1
                elif current_semester == 3:
                    current_semester = 1
                    current_year += 1
                else:
                    current_semester += 1
                str = input(f"want next semester (year={current_year},semester={current_semester})?")
        if chosen_number== 7:
            inp=input('do you want to save your schedules?(yes/no): ')
            if inp.lower()=='yes':
                save_scedules(all_schedules)
                print("shecdules is saved")
            else:
                inp=input('do you want to continue or exit ?')
                if inp.lower() == 'exit':
                    exit()
                else:
                    continue


                exit()



def save_scedules(all_schedules):
    all_lines = []
    for key, schedule in all_schedules.items():
        year, semester = key
        all_lines.append(f"-----------------------------------------year = {year}, semester = {semester} --------------------------------------------")
        all_lines.append("\n")
        all_lines.append(pprint.pformat(schedule, indent=2))
        all_lines.append("\n")
    with open("saved_schedule.txt", "w") as f:
        f.writelines(all_lines)



def print_study_plan():
    print("Year Semester    Courses")
    for key, courses in courses_by_year_and_semester.items():  # reading key and value from this dic , value whcih is array of  dic as i mention before
        courses_str = []
        year, semester = key
        for c in courses:
            courses_str.append(c["code"])
        print(f"{year}\t\t{semester}\t\t{','.join(courses_str)}")


def making_student_plan():
    with open("CEStudyPlan.txt", "r") as f:
        lines = f.readlines()[1:]
        for line in lines:
            line = line.strip().split(",")
            if not line or line == "\n":
                continue
            year = int(line[0])
            semester = int(line[1])
            key = (year, semester)
            if key in courses_by_year_and_semester:  # dic is declared before main function
                courses_by_year_and_semester[key].append({"code": line[2], "prerequisists": line[
                                                                                            3:] or []})  # adding specfic year and semster to make student plan in each (year,semster) value =array of dic[{"code": value,"prequists"},{},{},{}.....]
            else:
                courses_by_year_and_semester[key] = []  # if the key does not exists before add it to the main dic
                courses_by_year_and_semester[key].append({"code": line[2], "prerequisists": line[3:] or []})

        # pprint.pprint(courses_by_year_and_semester, indent=2)  # print this if you didnt understand


def sudent_records_verify():
    sudent_records_name = input("please enter Sudent Records file name ")
    sudent_records_location = input("please enter Sudent Records file location ")
    path.exists(sudent_records_name)
    name_exists = path.exists(f'{sudent_records_name}')
    location_exists = path.exists(f'{sudent_records_location}')

    if name_exists and location_exists:
        print("student record read succesfully!")
    else:
        print("file not found please retype the file name and location !!!!!!!")
        sudent_records_verify()


def student_study_plan(current_schedule):
    courses_by_year_and_semester = {}
    courses_by_grade = {}

    with open("CEStudyPlan.txt", "r") as f:
        lines = f.readlines()[1:]
        for line in lines:
            line = line.strip().split(",")
            if not line or line == "\n":
                continue
            year = int(line[0])
            semester = int(line[1])
            key = (year, semester)
            if key in courses_by_year_and_semester:  # dic is declared before main function
                courses_by_year_and_semester[key].append({"code": line[2], "prerequisists": line[
                                                                                            3:] or []})  # adding specfic year and semster to make student plan in each (year,semster) value =array of dic[{"code": value,"prequists"},{},{},{}.....]
            else:
                courses_by_year_and_semester[key] = []  # if the key does not exists before add it to the main dic
                courses_by_year_and_semester[key].append({"code": line[2], "prerequisists": line[3:] or []})
        ###################pprint.pprint(courses_by_year_and_semester, indent=2)
        print("Year Semester    Courses")
        current_schedule_courses = {course["course_code"] for course in (current_schedule or [])}
        for key, courses in courses_by_year_and_semester.items():  # reading key and value from this dic , value whcih is array of  dic as i mention before
            courses_str = []
            year, semester = key
            for c in courses:
                if c["code"] in current_schedule_courses:
                    courses_str.append(termcolor.colored(c['code'], "red"))
                elif c["code"] in passed_grades:
                    courses_str.append(termcolor.colored(c['code'], "green"))
                else:
                    courses_str.append(c["code"])
            print(f"{year}\t\t{semester}\t\t{','.join(courses_str)}")


def getting_passed_courses():
    with open("student_records.txt", "r") as f:  # reading courses student take
        lines = f.readlines()[1:]  # to avoide header
        for line in lines:
            courses_with_grade = line.strip().split(",")[2:]  # to avoid year and semester values
            for course_with_grade in courses_with_grade:
                course, grade = course_with_grade.strip().split(":")
                courses_by_grade[course] = int(grade)
    passed_grades = []
    for course in courses_by_grade:  # check which grade have taken he passed in it and add it to array
        if courses_by_grade[course] > 60:
            passed_grades.append(course)
    return passed_grades


def ask_user_the_preferences():
    global sem_free_days
    maximum_number_of_credits = int(input("please enter maximum number of credits:"))


    hours_by_semester[1] = int(input("please enter number of hours for semester 1:"))
    if hours_by_semester[1] > maximum_number_of_credits:
        print(f"Error, you cant have more than {maximum_number_of_credits} hours")
        return

    hours_by_semester[2] = int(input("please enter number of hours for semester 2:"))
    if hours_by_semester[2] > maximum_number_of_credits:
        print(f"Error, you cant have more than {maximum_number_of_credits} hours")
        return
    hours_by_semester[3] = int(input("please enter number of hours for semester 3:"))
    if hours_by_semester[3] > maximum_number_of_credits:
        print(f"Error, you cant have more than {maximum_number_of_credits} hours")
        return
    sem_free_days[1] = int(input("Please enter free days of semester1: "))

    sem_free_days[2] = int(input("Please enter free days of semester2: "))

    sem_free_days[3] = int(input("Please enter free days of summer semester: "))


def ask_user_number_of_semesters():
    global max_number_of_semesters
    max_number_of_semesters = int(input("please enter number of semesters to create:"))




def schedule_planning(year, semester):
    semester_one = {}
    semester_two = {}
    semester_summer = {}
    with open('CourseBrowser_1.json') as json_file:
        data = json.load(json_file)

    for key in data:
        if key not in semester_one:
            semester_one[key] = data[key]  # save json to dictionary

    with open('CourseBrowser_2.json') as json_file:
        data = json.load(json_file)

    for key in data:
        if key not in semester_two:
            semester_two[key] = data[key]  # save json to dictionary

    with open('CourseBrowser_3.json') as json_file:
        data = json.load(json_file)

    for key in data:
        if key not in semester_summer:
            semester_summer[key] = data[key]  # save json to dictionary

    # making_student_plan()
    making_semester = []
    current = (year, semester)


    current_hours = 0
    if semester == 1:
        my_semester = semester_one
    elif semester == 2:
        my_semester = semester_two
    else:
        my_semester = semester_summer

    for key, courses in courses_by_year_and_semester.items():
        current_year, current_semester = key
        if current_year <= year and (current_semester <= semester or (current_semester<=semester+1 and current_year!=year)):
            for course in courses:  # add courses before current semester
                if course["code"] not in passed_grades:
                    if (len(course["prerequisists"]) == 0 or check_if_prequisits_passed(
                            course["prerequisists"], passed_grades)) and if_exists_in_semester(semester_one, course["code"]):  # check if it passed prequisits and in that semester
                        making_semester.append(course)
                        new = course["code"][5]  # second number in code course is couse hours
                        current_hours = current_hours + int(new)

        else:
            break

    if current not in courses_by_year_and_semester:
        current = (year, semester - 1)
    courses = courses_by_year_and_semester.get(current)
    return priority(courses, current_hours, passed_grades, courses_by_year_and_semester,my_semester, making_semester, semester)



def priority(courses, current_hours, passed_grades, courses_by_year_and_semester, my_semester, making_semester, semester_number, free=None):

    current_semster = []
    semseter_hours = 0



    for course in making_semester:
        course["number_in_prequisists"] = int(check_number_the_course_is_in_prerequisists(course, courses_by_year_and_semester))  # depending in second priority want to see which unlocks more courses

    sorted_dictionaries = sorted(making_semester, key=lambda x: x['number_in_prequisists'],
                                 reverse=True)  # sort the courses from which have more number in preequisits

    priority_three_courses = []  # which have same number in preequisits (0)
    pprint.pprint(sorted_dictionaries)

    for course in sorted_dictionaries:  # add the  highest priority first which unlocks courses
        if course["number_in_prequisists"] != 0:
            current_semster.append(course)
            new = course["code"][5]
            semseter_hours = semseter_hours + int(new)
        else:
            priority_three_courses.append(course)

    already_added_courses_time = get_courses_times(my_semester, current_semster)
    priority_three_courses_time = get_courses_times(my_semester, priority_three_courses)

    if free is None:
        free = random.sample(DAYS,  sem_free_days[semester_number])

    # create high priortiy schedule
    current_schedule = make_schedule(free, already_added_courses_time)
    for added_course in current_schedule:
        passed_grades.append(added_course["course_code"])
    total_hours = 0
    # find total hours
    for course_in_schedule in current_schedule:
        total_hours += int(course_in_schedule["course_code"][5])
    remaining_hours = 0
    # check the remaing hours and courses to use from  lower priority
    remaining_courses = {}
    if total_hours < hours_by_semester[semester_number]:
        # find remaing hours
        remaining_hours =hours_by_semester[semester_number] - total_hours
        # sort by highest duration
        sorted_priority_three_courses_time = sorted(priority_three_courses_time, key=lambda k: int(k[5]),
                                                    reverse=True)
        for course_code in sorted_priority_three_courses_time:
            lecture_times = priority_three_courses_time[course_code]
            hours = int(course_code[5])
            added=0
            # find non opverlapping courses that fills all the scedule
            if hours <= remaining_hours:
                for lecture_time in lecture_times:
                    if free not in list(lecture_time.keys()) and all(
                            not check_overlap_times(already_added_course["time"], lecture_time) for
                            already_added_course in current_schedule):
                        remaining_courses[course_code] = lecture_times
                        remaining_hours -= hours
                        added+=hours
                        break
        # create second scheule
        low_priority_schedule = make_schedule(free, remaining_courses)
        for lower_course in low_priority_schedule:
            passed_grades.append(lower_course["course_code"])
        # append schedules togather
        current_schedule += low_priority_schedule

    courses_total_time = 0
    for schedule_course in current_schedule:
        courses_total_time += int(schedule_course["course_code"][5])

    print("--------------------------- Suggested Schedule --------------------------------------")

    if courses_total_time < hours_by_semester[semester_number]:
        print(termcolor.colored(f"here is a suggested schedule", "red"))
        priority(courses, current_hours, passed_grades, courses_by_year_and_semester, my_semester, making_semester, semester_number, [])
    else:
        print(termcolor.colored(f"schedule total hours={courses_total_time}", "blue"))
        print(termcolor.colored(f"free days for semester are: {free}", "blue"))
        pprint.pprint(current_schedule)
    print("-------------------------------------------------------------------------------------")

    return current_schedule


def make_schedule(free_day: str, courses: dict):
    schedule = []
    total_hours = 0
    time_found = False
    for course_code, lecture_times in courses.items():  # schedule maker
        for lecture_time in lecture_times:
            days = list(lecture_time.keys())  # [T, R]
            if len(days) == 0:
                continue
            if not set(free_day).intersection(set(days)):
                if len(schedule) == 0:
                    schedule.append({"time": lecture_time, "course_code": course_code})
                    break
                else:
                    if all(not check_overlap_times(already_added_course["time"], lecture_time) for already_added_course
                           in schedule):
                        schedule.append({"time": lecture_time, "course_code": course_code})
                        time_found = True
                        break
                if time_found:
                    break
    return schedule


def check_number_the_course_is_in_prerequisists(course_checking, courses_by_year_and_semester):
    number_of_times = 0
    for courses in courses_by_year_and_semester.values():
        for course in courses:
            if course_checking["code"] in course["prerequisists"]:
                number_of_times = number_of_times + 1

    return number_of_times


def check_if_prequisits_passed(prequisits, passed_grades):
    for i in prequisits:
        if i not in passed_grades:
            return False
    return True


def if_exists_in_semester(semester, code):
    for lecture in semester:
        if code in lecture:
            return True

    return False


def check_overlap_times(timeA, timeB):  # {"M": "10:00 - 11:00"}    #checking if it doesn't have  the same values
    daysA = set(timeA.keys())
    daysB = set(timeB.keys())
    if not len(daysA.intersection(daysB)):
        return False
    times_by_day = {}
    for day_name in daysA.union(daysB):
        times = times_by_day.get(day_name, [])
        if day_name in timeA:
            times.append(timeA[day_name])
        if day_name in timeB:
            times.append(timeB[day_name])
        times_by_day[day_name] = times
    for times in times_by_day.values():
        if len(times) == 1:
            continue
        timeA = times[0]
        timeB = times[1]
        startA, endA = timeA.split(" - ")
        startB, endB = timeB.split(" - ")
        startA_h, startA_m = startA.split(":")
        endA_h, endA_m = endA.split(":")
        startB_h, startB_m = startB.split(":")
        endB_h, endB_m = endB.split(":")
        start_time_A = time(hour=int(startA_h), minute=int(startA_m))
        end_time_A = time(hour=int(endA_h), minute=int(endA_m))
        start_time_B = time(hour=int(startB_h), minute=int(startB_m))
        end_time_B = time(hour=int(endB_h), minute=int(endB_m))
        latest_start = max(start_time_A, start_time_B)
        earliest_end = min(end_time_A, end_time_B)
        if latest_start < earliest_end:
            return True
    return False


def get_courses_times(semester, courses):
    times_by_lecture = {}
    for course in courses:
        for lecture in semester:
            if course["code"] in lecture:
                times_for_lecture = times_by_lecture.get(course["code"], [])
                times = dict(list(semester[lecture].items())[1:])
                times_for_lecture.append(times)
                times_by_lecture[course["code"]] = times_for_lecture
    return times_by_lecture

# def save():

main()

