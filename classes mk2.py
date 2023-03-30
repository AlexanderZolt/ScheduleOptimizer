import datetime

class Clas:
    def __init__(self, group_one, group_two, schedule_one=None, schedule_two=None):
        self.group_one = group_one
        self.group_two = group_two
        self.schedule_one = schedule_one if schedule_one else {}
        self.schedule_two = schedule_two if schedule_two else {}

class Course:
    def __init__(self, name, hours, teacher):
        self.name = name
        self.hours = hours
        self.teacher = teacher

class Teacher:
    def __init__(self, name, courses=None, classes=None):
        self.name = name
        self.courses = courses if courses else []
        self.classes = classes if classes else []
        self.total_lectures = 0
        self.daily_lectures = 0

    def add_course(self, course):
        self.courses.append(course)

    def add_class(self, clas):
        self.classes.append(clas)

class Auditorium:
    def __init__(self, number, specialization=None):
        self.number = number
        self.specialization = specialization if specialization else 'general'
        self.schedule = {}

class School:
    def __init__(self, auditoriums):
        self.auditoriums = auditoriums

    def find_available_timeslots(self, auditorium, date):
        timeslots = []
        for i in range(1, 6):
            start_time = datetime.datetime(date.year, date.month, date.day, i+7)
            end_time = start_time + datetime.timedelta(hours=2)
            slot = {'start_time': start_time, 'end_time': end_time}
            if slot not in auditorium.schedule.values():
                timeslots.append(slot)
        return timeslots

    def optimize_specialization(self):
        for auditorium in self.auditoriums:
            courses_taught = set()
            for slot in auditorium.schedule.values():
                course = slot['course']
                courses_taught.add(course)
            if len(courses_taught) == 1:
                course = courses_taught.pop()
                auditorium.specialization = course.name

    def optimize_auditorium_usage(self):
        for auditorium in self.auditoriums:
            for slot in auditorium.schedule.values():
                teacher = slot['teacher']
                date = slot['start_time'].date()
                teacher.total_lectures += 1
                teacher.daily_lectures += 1
                if teacher.total_lectures > 20:
                    print(f"{teacher.name} has exceeded the weekly lecture limit!")
                if teacher.daily_lectures > 5:
                    print(f"{teacher.name} has exceeded the daily lecture limit!")
                for other_auditorium in self.auditoriums:
                    if other_auditorium.number != auditorium.number:
                        if date in other_auditorium.schedule:
                            if other_auditorium.schedule[date] == slot:
                                print(f"Auditorium {other_auditorium.number} is already booked by {slot['teacher'].name} at {slot['start_time']}!")
                if slot['end_time'].hour == 18:
                    print(f"{teacher.name} is teaching a lecture that ends at 6 pm!")
                if slot['course'].hours % 2 != 0:
                    print(f"{slot['course'].name} has an odd number of hours!")

    def assign_lecture(self, clas, course, teacher, date):
        timeslots = self.find_available_timeslots(self.auditoriums[0], date)
       
