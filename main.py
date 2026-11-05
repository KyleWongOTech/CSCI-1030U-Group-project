import argparse
import tkinter as tk
from tkinter import font as tkFont
import json
import csv

#section class that keeps track of what day and times the classes happen in
class Section:
    def __init__(self, day: str, time_start: str, time_end: str, type_class:str):
        self.day=day
        self.time_start=time_start
        self.time_end=time_end
        self.type_class=type_class

#courses to keep track of the name and the sections that the classes happen in
class Course:
    #used for all classes
    def __init__(self, name: str, slot1: Section, slot2: Section, lab: list[Section], tutorial:list[Section] ):
        self.name=name
        self.slot1=slot1
        self.slot2=slot2
        self.lab=lab
        self.tutorial=tutorial

#stores the students schedule preferences 
class SchedulePreferences:
    def __init__(self, min_break=30, days_off=None, priority="balanced"):
        self.min_break = int(min_break)
        #priority can be "balanced", "breaks", or "days_off"
        self.priority = priority
        if days_off is None:
            self.days_off = []
        else:
            self.days_off = days_off
    #converts preferencs into a dictionary
    def to_dict(self):
        return {
            "min_break": self.min_break,
            "days_off": self.days_off,
            "priority": self.priority
        }
    #saves preferences to a json file
    def save_to_json(self, filename):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=4)
    #loads previous preferences from a json file
    def load_from_json(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
            self.min_break = data["min_break"]
            self.days_off = data["days_off"]
            self.priority = data["priority"]



def add_user_cal(user:str, Calender:list[list[str]]):
    with open("User_Calender.txt", "a") as f:
        f.write(f"{user}\n")
        for i in range(len(Calender)):
            f.write(f"{Calender[i]}\n")
        f.write("------------------\n\n")

def read_user_cal(user:str, cal:list[list[str]]) -> list[list[str]]|None:

    found:bool=False
    col: int = 0
    row: int = 0
    with open("User_Calender.txt") as f:
        for line in f:
            if line.lower()==user.lower():
                found=True
            if found:
                for char in line:
                    if char==',':
                        row+=1
                    elif char!=" " or char!="'":
                        cal[col][row]= cal[col][row]+char
            col+=1
            if col==len(cal)-1:
                break
    if not found:
        return None
    return cal




def print_preferences(pref: list[str]):
    print("\nYour schedule with preferred times of day:")
    for i in range(len(pref)):
        print(f"{pref[i]}")



#Mirah Milestone #2: class that shows the calendar (terminal, csv file, and tkinter window)
class CalendarView:
    def __init__(self, user_calender: list[list[str]]):
        self.calendar = user_calender   # the 2D calendar to show
        self.colours = {}               # course name -> colour for the window

    #recursion: finds the longest cell starting at row_index and going down
    def widest_cell(self, row_index: int = 0) -> int:
        #base case- no rows left
        if row_index == len(self.calendar):
            return 0
        widest_here = 0
        for cell in self.calendar[row_index]:
            if len(cell.strip()) > widest_here:      # strip() takes spaces out
                widest_here = len(cell.strip())
        #recursive case- compare this row with the widest of the rest
        return max(widest_here, self.widest_cell(row_index + 1))

    def column_width(self) -> int:
        return self.widest_cell() + 2

    def print_grid(self):
        column_width = self.column_width()
        line = "-" * ((column_width + 1) * len(self.calendar[0]) - 1)

        print(line)
        for i in range(len(self.calendar)):
            print("|".join(cell.strip().center(column_width) for cell in self.calendar[i]))
            if i == 0:
                print(line)      # divider under the day names
        print(line)

    def courses_by_day(self) -> dict[str, list[str]]:
        courses = {}
        # column 0 is the time, so days start at column 1
        for col in range(1, len(self.calendar[0])):
            day = self.calendar[0][col].strip()
            courses[day] = []
            for row in self.calendar[1:]:
                name = row[col].strip()
                if name != "" and name not in courses[day]:
                    courses[day].append(name)
        return courses

    def print_summary(self):
        courses = self.courses_by_day()
        print("Courses per day:\n")
        for day in courses:
            if len(courses[day]) == 0:
                print(f"{day:<10}: Free")
            else:
                print(f"{day:<10}: " + ", ".join(courses[day]))

    #file i/o: writes the calendar to a csv file (opens in excel)
    def export_csv(self, filename: str):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            for row in self.calendar:
                writer.writerow([cell.strip() for cell in row])
        print(f"Calendar exported to {filename}")

    #gives every course its own colour in the window
    def colour_for(self, cell: str) -> str:
        palette = ["#afb4b6", "#ffcfdf", "#fefdca", "#c3f0ca", "#e0c3fc", "#ffd8a8"]
        if cell == "":
            return "white"
        course_name = cell.split(" - ")[0]
        if course_name not in self.colours:
            self.colours[course_name] = palette[len(self.colours) % len(palette)]
        return self.colours[course_name]

    #interface: shows the calendar as a grid of coloured labels in a tkinter window
    def show_window(self, parent: tk.Tk):
        window = tk.Toplevel(parent)
        window.title("Your Schedule")
        small_font = ("Arial", 8)
        for r in range(len(self.calendar)):
            for c in range(len(self.calendar[r])):
                cell = self.calendar[r][c].strip()
                if r == 0 or c == 0:
                    colour = "lightgrey"    # headers (days and times)
                else:
                    colour = self.colour_for(cell)
                label = tk.Label(window, text=cell, bg=colour, font=small_font,
                                 width=18, relief="ridge", bd=1)
                label.grid(row=r, column=c, sticky="NSEW")
        tk.Button(window, text="Close", command=window.destroy).grid(
            row=len(self.calendar), column=0, columnspan=len(self.calendar[0]), sticky="EW")
        parent.wait_window(window)   # waits until the window is closed


#old function names still work so the rest of the code doesn't break
def print_calendar(user_calender: list[list[str]]):
    CalendarView(user_calender).print_grid()


def print_course_summary(user_calender: list[list[str]]):
    CalendarView(user_calender).print_summary()

def print_course_summary(user_calender: list[list[str]]):
    courses_by_day = {}

    # column 0 is the time, so days start at column 1
    for col in range(1, len(user_calender[0])):
        day = user_calender[0][col].strip()
        courses_by_day[day] = []
        for row in user_calender[1:]:
            name = row[col].strip()
            if name != "" and name not in courses_by_day[day]:
                courses_by_day[day].append(name)

    print("Courses per day:\n")
    for day in courses_by_day:
        if len(courses_by_day[day]) == 0:
            print(f"{day:<10}: Free")
        else:
            print(f"{day:<10}: " + ", ".join(courses_by_day[day]))


def place_lecture(available: bool, class_name: str, class_sec:Section, temp_cal=list[list[str]]) -> tuple[
    type[list[list[str]]], bool]:
    if class_sec is not None:

        for i in range (1, len(temp_cal)):
            if not available:
                break
            if class_sec.time_start==temp_cal[i][0].replace(" ", ""):
                for j in range (i, len(temp_cal)):
                    if class_sec.time_end==temp_cal[j][0].replace(" ", ""):
                        for k in range (len(temp_cal[0])):
                            if class_sec.day==temp_cal[0][k].replace(" ", "") and "" == temp_cal[i][k]:
                                temp_cal=recursion(k,i,j,class_name, class_sec.type_class, temp_cal)

                                break
                            elif class_sec.day==temp_cal[0][k].replace(" ", "") and "" != temp_cal[i][k]:
                                available=False

                                break

    return temp_cal, available

def recursion(row: int, col:int, last_col:int, class_name:str, class_type: str, temp_cal)-> type[list[list[str]]]:
    if last_col == col:
        return temp_cal

    temp_cal[col][row] = class_name + " - " + class_type
    col+=1

    return recursion(row, col, last_col, class_name, class_type, temp_cal)

def place_lab_tutorial(available: bool, className: str, mylist: list[Section], temp_cal=type[list[list[str]]]) :
    alreadyIn:bool
    if mylist is not None:
        for q in range (len(mylist)):
            alreadyIn = False
            for r in range(len(temp_cal)):
                if (className +" - " + mylist[q].type_class) in temp_cal[r]:
                    alreadyIn=True
            if not available:
                break
            if not alreadyIn:
                temp_cal, available = place_lecture(available, className, mylist[q] ,temp_cal)
                if available == False and q<len(mylist):
                    available=True
    return temp_cal, available

def check_day() -> None:
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    userInput:str= inputTxt.get("1.0", "end-1c")
    print(userInput)
    if userInput in days:
        inputTxt.delete("1.0","end-1c")
        get_user_pref_tk_pref(userInput)
    elif userInput == "done":
        time_preference.grid_forget()
        inputTxt.grid_forget()
        confirmButton.grid_forget()
        prefButton.grid(row=1,column=1, sticky='ENSW')

def check_pref(day) ->None:
    userInput:str = inputTxt.get("1.0", "end-1c")
    if userInput in ["1","2","3","4"]:
        inputTxt.delete("1.0","end-1c")
        get_user_pref(day, userInput)
    elif userInput == "done":
        time_preference.grid_forget()
        inputTxt.grid_forget()
        confirmButton.grid_forget()
        prefButton.grid(row=1,column=1, sticky='ENSW')

def get_user_pref_tk_day() ->None:
    prefButton.grid_forget()

    time_preference.config(text="\nChoose a day of the week \n from Monday to Saturday", font=bigFont)
    time_preference.grid(row=0,column=1, sticky='ENSW')
    inputTxt.config(height = 15, width=20, font=bigFont)
    inputTxt.grid(row=1, column=1, sticky='ENW')
    confirmButton.config(text="Confirm Choice", height=5, command=lambda : check_day())
    confirmButton.grid(row=1, column=1, sticky='ESW')

def get_user_pref_tk_pref(day:str) ->None:

    time_preference.config(text="\nTime of day preferences:\n1. Morning (08:00 - 12:00)"
                                +"\n2. Afternoon (12:00 - 16:00)\n3. Evening (16:00 - 20:00)"
                                +"\n4. No preference\n", font=bigFont)
    time_preference.grid(row=0,column=1, sticky='ENSW')
    inputTxt.config(height = 15, width=20, font=bigFont)
    inputTxt.grid(row=1, column=1, sticky='ENW')
    confirmButton.config(text="Confirm Choice", height=5, command=lambda : check_pref(day))
    confirmButton.grid(row=1, column=1, sticky='ESW')


def get_user_pref(day:str, choose:str) -> None:
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    global user_pref

    index = days.index(day)
    if choose == "1":
        user_pref[index]=f"{day.lower()}: Morning(08:00 - 12:00)"

    elif choose == "2":
        user_pref[index]=f"{day.lower()}: Afternoon(12:00 - 16:00)"

    elif choose == "3":
        user_pref[index]=f"{day.lower()}: Evening(16:00 - 20:00)"

    elif choose == "4":
        user_pref[index]=f"{day.lower()}: Any(08:00 - 20:00)"

    else:
        print("Not a valid choice.")



# turns the time into minutes so that it's easier to check for breaks
def minutes(time):
    time=time.split(":")
    return int(time[0])*60+int(time[1])

#checks if the break between two classes is enough
def enough_break (section1, section2, break_time):
    if section1.day != section2.day:
        return True
    start1=minutes(section1.time_start)
    end1=minutes(section1.time_end)
    start2=minutes(section2.time_start)
    end2=minutes(section2.time_end)

    # Check if there's an overlap
    if end1 + break_time <= start2:
        return True
    if end2 + break_time <= start1:
        return True
    return False

#checks if 2 classes overlap
def overlap(section1, section2):
    #classes on different days don't overlap
    if section1.day != section2.day:
        return False
    #convert times to minutes for easier comparison
    start1 = minutes(section1.time_start)
    end1 = minutes(section1.time_end)
    start2 = minutes(section2.time_start)
    end2 = minutes(section2.time_end)

    #check for overlap
    if start1 < end2 and start2 < end1:
        return True
    return False

#check if a class is on a day the student wants off
def allowed_day(section, days_off):
    if section.day in days_off:
        return False
    return True

#checks if a class follows all the studens preferences
def can_add(section, selected, preferences):
    #checks if the students wants this day off
    day_okay =allowed_day(section, preferences.days_off)
    #checks whetehr the class has eneough break time]
    break_okay = True

    for old_section, old_name in selected:
        #no overlap between classes
        if overlap(section, old_section):
            return False
        if not enough_break(section, old_section, preferences.min_break):
            break_okay = False
            break
    #both preferences are satisfied
    if day_okay and break_okay:
        return True
    #the student prioritizes days off
    if preferences.priority == "days_off":
        return day_okay
    #the student prioritizes breaks
    if preferences.priority == "breaks":
        return break_okay
    #balanced priority, both must be satisfied
    return False


   

def course_maker(courses : list[list[str]], courselist:list[Course]) -> list[list[str]]:


    #goes through the list of course objects
    for x in range (len(courselist)):
        #used later
        available = True
        skip = False

        #lecture 1
        courses, available=place_lecture(available, courselist[x].name, courselist[x].slot1, courses)

        #lecture 2
        courses, available=place_lecture(available, courselist[x].name, courselist[x].slot2, courses)

        #tutorial
        courses, available = place_lab_tutorial(available, courselist[x].name, courselist[x].tutorial, courses)

        #lab
        courses, available = place_lab_tutorial(available, courselist[x].name, courselist[x].lab, courses)

        if not available:
            for i in range (len(courses)):
                for j in range(len(courses[i])):

                    if courselist[x].name in courses[i][j]:

                        courses[i][j]=""



    return courses

#create possible combinations of courses 
def course_options(course):
    required=[]
    #add the required sections to the list
    if course.slot1 is not None:
        required.append(course.slot1)
    if course.slot2 is not None:
        required.append(course.slot2)

    #get the available labs and tutorials
    labs=course.lab if course.lab else [None]
    tutorials=course.tutorial if course.tutorial else [None]

    choices=[]

    #try all combinations of labs and tutorials
    for lab in labs:
        for tutorial in tutorials:
           sections=required[:]
           if lab is not None:
               sections.append(lab) 
           if tutorial is not None:
               sections.append(tutorial)
           choices.append(sections)
    return choices

#creates a copy of the preferences with a different priority
def change_priority(preferences, new_priority):
    return SchedulePreferences(preferences.min_break, preferences.days_off, new_priority)

#generates schedules using recursion
def generate_schedule(courses, preferences):
    #recursive helper that tried different combinations
    def find_schedules(current_preferences):
        results = []

        def try_courses(index, selected):
            #base case- all courses have been considered
            if index == len(courses):
                results.append(selected[:])
                return

            # get the current course
            course = courses[index]

            #try each possible section combination
            for option in course_options(course):
                new_selected = selected[:]
                valid = True

                #check each section in this combination
                for section in option:
                    if not can_add(section, new_selected, current_preferences):
                        valid = False
                        break
                    new_selected.append((section, course.name))

                #recursion- if valid, move to the next course
                if valid:
                    try_courses(index + 1, new_selected)

        #start checking from the first course
        try_courses(0, [])
        return results

    #first try to satisfy both preferences
    balanced_preferences = change_priority(preferences, "balanced")
    schedule = find_schedules(balanced_preferences)

    if len(schedule) > 0:
        return schedule

    #if both cant be satified, use the main priority
    if preferences.priority == "days_off":
        return find_schedules(change_priority(preferences, "days_off"))
    if preferences.priority == "breaks":
        return find_schedules(change_priority(preferences, "breaks"))

    #balanced means neither preference can be relaxed
    return []

#creates a calendar using the selected class sections
def make_calendar(selected, original_calendar):

    #make a copy of the original calendar
    new_calendar=[]
    for row in original_calendar:
        new_calendar.append(row[:])

    #go through each seleceted class
    for section, name in selected:
        #fina the correct day column
        if section.day not in new_calendar[0]:
            continue    
        column = new_calendar[0].index(section.day)

        #convert class time into minutes
        start = minutes(section.time_start)
        end = minutes(section.time_end)

        #go through each time row
        for row in range (1, len(new_calendar)):
            time=minutes(new_calendar[row][0].strip())
            #check if this time is during the class time
            if start <= time and time< end:
                new_calendar[row][column] = name + " - " + section.type_class
    return new_calendar


#initializes the course schedule

calendar: list[list[str]] = [["  Time    ", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                            ["  08:00    ","","","","","",""],
                            ["  08:10    ","","","","","",""],
                            ["  08:30    ","","","","","",""],
                            ["  08:40    ","","","","","",""],
                            ["  09:00    ","","","","","",""],
                            ["  09:10    ","","","","","",""],
                            ["  09:30    ","","","","","",""],
                            ["  09:40    ","","","","","",""],
                            ["  10:00    ","","","","","",""],
                            ["  10:10    ","","","","","",""],
                            ["  10:30    ","","","","","",""],
                            ["  10:40    ","","","","","",""],
                            ["  11:00    ","","","","","",""],
                            ["  11:10    ","","","","","",""],
                            ["  11:30    ","","","","","",""],
                            ["  11:40    ","","","","","",""],
                            ["  12:00    ","","","","","",""],
                            ["  12:10    ","","","","","",""],
                            ["  12:30    ","","","","","",""],
                            ["  12:40    ","","","","","",""],
                            ["  13:00    ","","","","","",""],
                            ["  13:10    ","","","","","",""],
                            ["  13:30    ","","","","","",""],
                            ["  13:40    ","","","","","",""],
                            ["  14:00    ","","","","","",""],
                            ["  14:10    ","","","","","",""],
                            ["  14:30    ","","","","","",""],
                            ["  14:40    ","","","","","",""],
                            ["  15:00    ","","","","","",""],
                            ["  15:10    ","","","","","",""],
                            ["  15:30    ","","","","","",""],
                            ["  15:40    ","","","","","",""],
                            ["  16:00    ","","","","","",""],
                            ["  16:10    ","","","","","",""],
                            ["  16:30    ","","","","","",""],
                            ["  16:40    ","","","","","",""],
                            ["  17:00    ","","","","","",""],
                            ["  17:10    ","","","","","",""],
                            ["  17:30    ","","","","","",""],
                            ["  17:40    ","","","","","",""],
                            ["  18:00    ","","","","","",""],
                            ["  18:10    ","","","","","",""],
                            ["  18:30    ","","","","","",""],
                            ["  18:40    ","","","","","",""],
                            ["  19:00    ","","","","","",""],
                            ["  19:10    ","","","","","",""],
                            ["  19:30    ","","","","","",""],
                            ["  19:40    ","","","","","",""],
                            ["  20:00    ","","","","","",""],]



CSCI1061UA=Section("Tuesday", "15:40", "17:00", "lecture")
CSCI1061UB=Section("Thursday", "15:40", "17:00", "lecture")
CSCI1061UC=Section("Thursday", "14:10", "15:30", "lecture")
CSCI1061UD=Section("Monday", "14:10", "15:30", "lecture")

CSCI1061ULABA=Section("Tuesday", "17:10", "20:00", "lab")
CSCI1061ULABB=Section("Friday", "14:10", "17:00", "lab")
CSCI1061ULABC=Section("Thursday", "17:10", "20:00", "lab")
CSCI1061ULABD=Section("Tuesday", "08:10", "11:00", "lab")
CSCI1061ULABE=Section("Friday", "08:10", "11:00","lab")


#CSCI 1050U arch

CSCI1050UA=Section("Thursday", "12:40", "14:00", "lecture")
CSCI1050UB=Section("Wednesday", "12:40", "14:00", "lecture")
CSCI1050UC=Section("Thursday", "12:40", "14:00", "lecture")
CSCI1050UD=Section("Wednesday", "12:40", "14:00", "lecture")

CSCI1050ULABA=Section("Thursday", "08:10", "11:00", "lab")
CSCI1050ULABB=Section("Tuesday", "14:10", "17:00", "lab")
CSCI1050ULABC=Section("Tuesday", "11:10", "14:00", "lab")
CSCI1050ULABD=Section("Tuesday", "17:10", "20:00", "lab")


#MATH 1020U  calc II

MATH1020UA=Section("Wednesday", "08:10", "09:30", "lecture")
MATH1020UB=Section("Monday", "12:10", "13:30", "lecture")
MATH1020UC=Section("Friday", "17:10", "18:30", "lecture")

MATH1020UTUTA=Section("Thursday", "08:10", "09:30", "tutorial")
MATH1020UTUTB=Section("Tuesday", "08:10", "09:30", "tutorial")
MATH1020UTUTC=Section("Wednesday", "08:10", "09:30", "tutorial")

#PHY 1020U Physcis II

PHY1020UA=Section("Wednesday", "12:40", "14:00", "lecture")
PHY1020UB=Section("Thursday", "12:40", "14:00", "lecture")
PHYLAB1 = Section("Tuesday", "08:10", "09:30", "Lab")
PHYLAB2 = Section("Friday", "17:10", "20:10", "Lab")
PHYTUT1 = Section("Monday", "08:10", "10:30", "Tutorial")
PHYTUT2 = Section("Friday", "17:10", "20:00", "Tutorial")



csci1061_lecs = [CSCI1061UA, CSCI1061UB, CSCI1061UC, CSCI1061UD]
csci1061_labs = [CSCI1061ULABA, CSCI1061ULABB, CSCI1061ULABC, CSCI1061ULABD, CSCI1061ULABE]

csci1050_lecs = [CSCI1050UA, CSCI1050UB, CSCI1050UC, CSCI1050UD]
csci1050_labs = [CSCI1050ULABA, CSCI1050ULABB, CSCI1050ULABC, CSCI1050ULABD]

CSCI1061 = Course("CSCI 1061", csci1061_lecs[0], csci1061_labs[0], None, None)
CSCI1050 = Course("CSCI 1050", csci1050_lecs[0], csci1050_labs[0], None, None)
# Creates CSCI courses with their required lab sections

math1020_lecs = [MATH1020UA, MATH1020UB, MATH1020UC]
math1020_tuts = [MATH1020UTUTA, MATH1020UTUTB, MATH1020UTUTC]

phy1020_lecs = [PHY1020UA, PHY1020UB]
phy1020_labs = [PHYLAB1, PHYLAB2]
phy1020_tuts = [PHYTUT1, PHYTUT2]






PHY = Course("PHY 101", PHY1020UA, PHY1020UB, phy1020_labs, phy1020_tuts)

CALC = Course("CALC 102", MATH1020UA, MATH1020UB, None, math1020_tuts)


testCourseList: list[Course] = [CALC, PHY]
 

# Lets the user choose which courses to add
#print("\nAvailable courses:")
#print("1. CALC 102")
#print("2. PHY 101")
#print("3. CSCI 1061")
#print("4. CSCI 1050")

#while True:
#    choice = input("Choose a course (0 to finish): ")

#    if choice == "0":
#        break
#    elif choice == "1":
#        testCourseList.append(CALC)
#    elif choice == "2":
#        testCourseList.append(PHY)#added 3 and 4
#    elif choice == "3":
#        testCourseList.append(CSCI1061)
#    elif choice == "4":
#        testCourseList.append(CSCI1050)
#    else:
#        print("Invalid choice.")


# which hours each preference choice covers
PERIOD_HOURS = {
    "Morning": "08:00 - 12:00",
    "Afternoon": "12:00 - 16:00",
    "Evening": "16:00 - 20:00",
    "Any": "no preference",
}

user_pref:list[str] = ["monday: Any(08:00 - 20:00)","tuesday: Any(08:00 - 20:00)",
                       "wednesday: Any(08:00 - 20:00)","thursday: Any(08:00 - 20:00)",
                       "friday: Any(08:00 - 20:00)","saturday: Any(08:00 - 20:00)"]


def main():


    parser = argparse.ArgumentParser(description="used to get the name of the user")
    parser.add_argument("name", help="what name to save for the calender")
    #hafsa's command line option for min break
    parser.add_argument("--min_break", type=int, default=None, help="minimum break between classes in minutes")
    #command line options for exporting to csv
    parser.add_argument("--export", default=None, help="save the calendar to a csv file, example: schedule.csv")
    args = parser.parse_args()

    view = CalendarView(newCalendar)
    if args.export is not None:
        view.export_csv(args.export)
    view.show_window(root)

    #read the min break from the command line
    print(f"Minimum break between classes: {args.min_break} minutes")

    add_user_cal(args.name, newCalendar)
    cal_temp=  read_user_cal(args.name, calendar)

    if args.min_break is not None:
        min_break = args.min_break



root = tk.Tk()
root.title("Calender")
root.geometry("1200x700")
root.grid_rowconfigure((0,1,2,3,4,5), weight=1,  uniform="a")
root.grid_columnconfigure((0,1,2), weight=1,  uniform="a")

#hafsa's minimum break preference
break_label = tk.Label(root, text="Minimum break between classes (in minutes):")
break_label.grid(row=2, column=0)
break_entry = tk.Entry(root)
break_entry.grid(row=2, column=1)
break_entry.insert(0, "30")  # Default value
#hafsa's days off preference
days_label = tk.Label(root, text="Days off (comma-separated, e.g., Monday,Friday):")
days_label.grid(row=3, column=0)
days_entry = tk.Entry(root)
days_entry.grid(row=3, column=1)
days_entry.insert(0, "Friday")  # Default value
#hafsa's priority preference
priority_label = tk.Label(root, text="Priority (balanced, breaks, days_off):")
priority_label.grid(row=4, column=0)
priority_entry = tk.Entry(root)
priority_entry.grid(row=4, column=1)
priority_entry.insert(0, "balanced")  # Default value

time_preference = tk.Label(root)
inputTxt = tk.Text(root)
confirmButton = tk.Button(root)

bigFont = tkFont.Font(family="Ariel", size=12, weight="bold")
prefButton =tk.Button(root, text="Preference Button",font=bigFont, command=lambda :get_user_pref_tk_day(),bd=1)
prefButton.grid(row=1,column=1, sticky='ENSW')

#button to confirm the preferences and generate the schedule
done_button = tk.Button(root, text="Generate Schedule", font=bigFont, command=root.quit)#https://coderslegacy.com/python/tkinter-close-window/
done_button.grid(row=5, column=1)
root.mainloop()


print_preferences(user_pref)
#get the minimum break from the entry
min_break = int(break_entry.get())
#use the command line argument for min break if provided

#Hafsa's scheduling preferences
#get the prefereed days off from the entry and split them into a list
days_off=[]
for day in days_entry.get().split(","):
    days_off.append(day.strip())
#get the priority from the entry
priority = priority_entry.get().strip()
my_preferences = SchedulePreferences(min_break=min_break, days_off=days_off, priority=priority)
#save hafsa's preferences to a json file
my_preferences.save_to_json("preferences.json")
print("Preferences saved to preferences.json")
#load the preferences from the json file
my_preferences.load_from_json("preferences.json")
print("Preferences loaded from preferences.json")
#show the loaded preferences
print(my_preferences.to_dict())
print("Minimum break:", my_preferences.min_break)
#generate a schedule based on the preferences
my_schedule = generate_schedule(testCourseList, my_preferences)
#check how many scjedules were found
print("valid schedules found:", len(my_schedule))
if len(my_schedule)>0:
    print("Success! the scheduler found a valid schedule that meets your preferences.")
else:
    print("No valid schedules found that meet your preferences.")
#show the classes in the first valid schedule
if len(my_schedule)>0:
    print("Classes in the first valid schedule:")
    for section, name in my_schedule[0]:
        print(name, section.day, section.time_start, "-", section.time_end)
#display hafsa's selected schedule in the calendar 
if len(my_schedule)>0:
    hafsa_calendar = make_calendar(my_schedule[0], calendar)
    print("calendar using your preferences:")
    print_calendar(hafsa_calendar)

newCalendar: list[list[str]] = course_maker(calendar, testCourseList)
print_calendar(newCalendar)
print()
print_course_summary(newCalendar)
#test


if __name__=="__main__":
    main()




