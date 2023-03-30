from datetime import datetime, timedelta, date

class School:
    def __init__(self, name, auditoriums, red_week_schedule, black_week_schedule):
        self.name = name
        self.auditoriums = auditoriums
        self.red_week_schedule = red_week_schedule
        self.black_week_schedule = black_week_schedule
        
        self.classes = []
        self.teachers = []
        self.courses = []
        
        self.start_date = date(2023, 9, 1)  # Start date for the school year
        self.end_date = date(2024, 5, 31)  # End date for the school year
        
        self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.holidays = []  # List of holidays, to be populated later
        
    def get_available_timeslots(self, auditorium, start_time, end_time, day):
        """Returns a list of available timeslots for an auditorium on a given day"""
        if day not in self.weekdays:
            return []  # lectures are only held on weekdays
        
        if day in self.holidays:
            return []  # no lectures on holidays
        
        auditorium_schedule = self.get_auditorium_schedule(auditorium, day)
        available_timeslots = []
        current_time = start_time
        while current_time < end_time:
            if (current_time, current_time + timedelta(hours=2)) not in auditorium_schedule:
                available_timeslots.append((current_time, current_time + timedelta(hours=2)))
            current_time += timedelta(hours=2)
        return available_timeslots
    
    def get_auditorium_schedule(self, auditorium, day):
        """Returns the schedule for an auditorium on a given day"""
        if day in self.red_week_schedule:
            return self.red_week_schedule[day][auditorium]
        elif day in self.black_week_schedule:
            return self.black_week_schedule[day][auditorium]
        else:
            return []
        
    def set_auditorium_specialization(self, auditorium, specialization):
        """Sets the specialization of an auditorium"""
        for course in self.courses:
            if course.specialization == specialization:
                for day in self.weekdays:
                    schedule = self.get_auditorium_schedule(auditorium, day)
                    for timeslot in schedule:
                        if self.is_timeslot_free(auditorium, timeslot, day):
                            return (day, timeslot)
        return None
    
    def is_timeslot_free(self, auditorium, timeslot, day):
        """Checks if an auditorium is free during a given timeslot on a given day"""
        if day in self.red_week_schedule:
            schedule = self.red_week_schedule[day][auditorium]
        else:
            schedule = self.black_week_schedule[day][auditorium]
        return timeslot not in schedule
    
    def is_teacher_free(self, teacher, timeslot, day):
        """Checks if a teacher is free during a given timeslot on a given day"""
        for teacher_course in teacher.courses:
            if teacher_course.end_time >= timeslot[0] and teacher_course.start_time <= timeslot[1]:
                return False
            if teacher_course.day == day and teacher_course.auditorium in self.auditoriums:
                auditorium_schedule = self.get_auditorium_schedule(teacher_course.auditorium, day)
                if timeslot in auditorium_schedule:
                    return False
        return
