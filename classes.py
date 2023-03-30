import itertools
from datetime import date, timedelta

class Course:
    def __init__(self, name, hours, teacher, clas):
        self.name = name
        self.hours = hours
        self.teacher = teacher
        self.clas = clas
        
class Clas:
    def __init__(self, name, group_one, group_two=None):
        self.name = name
        self.group_one = group_one
        self.group_two = group_two
        self.schedule = [[[] for _ in range(5)] for _ in range(4)]
        self.group_one_courses = []
        self.group_two_courses = []
        
    def add_course(self, course):
        if course.clas == self.name:
            if course.teacher in self.group_one.teachers:
                self.group_one_courses.append(course)
            elif self.group_two and course.teacher in self.group_two.teachers:
                self.group_two_courses.append(course)
                
    def __str__(self):
        return self.name
    
class Teacher:
    def __init__(self, name, courses, clas):
        self.name = name
        self.courses = courses
        self.clas = clas
        self.lectures_per_week = 20
        self.max_lectures_per_day = 5
        self.max_consecutive_lectures = 4
        self.max_lectures_in_row = 2
        
    def __str__(self):
        return self.name
    
class Auditorium:
    def __init__(self, number, specialization='general'):
        self.number = number
        self.specialization = specialization
        self.schedule = [[[] for _ in range(5)] for _ in range(4)]
        
    def is_available(self, day, lecture):
        return not bool(self.schedule[lecture][day])
    
    def __str__(self):
        return str(self.number)
    
class School:
    def __init__(self, aud_numbers, aud_specializations):
        self.classes = []
        self.teachers = []
        self.courses = []
        self.auditoriums = [Auditorium(number, specialization) for number, specialization in zip(aud_numbers, aud_specializations)]
        
    def add_clas(self, clas):
        self.classes.append(clas)
        
    def add_teacher(self, teacher):
        self.teachers.append(teacher)
        
    def add_course(self, course):
        self.courses.append(course)
        
    def get_teacher_schedule(self, teacher):
        teacher_schedule = [[[] for _ in range(5)] for _ in range(4)]
        for clas in self.classes:
            if clas.group_one.has_teacher(teacher):
                teacher_courses = [course for course in clas.group_one_courses if course.teacher == teacher]
            elif clas.group_two and clas.group_two.has_teacher(teacher):
                teacher_courses = [course for course in clas.group_two_courses if course.teacher == teacher]
            else:
                continue
            for course in teacher_courses:
                for lecture_num, day_num in itertools.product(range(course.hours//2 + course.hours%2), range(5)):
                    if not clas.schedule[lecture_num][day_num]:
                        teacher_schedule[lecture_num][day_num].append((clas, course))
                        break
        return teacher_schedule
    
    def get_auditorium_schedule(self, auditorium):
        auditorium_schedule = [[[] for _ in range(5)] for _ in range(4)]
        for clas in self.classes:
            for course in clas.group_one_courses:
                for lecture_num, day_num in itertools.product(range(course.hours//2 + course
