import argparse
import tkinter as tk
from tkinter import font as tkFont

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


def get_column_width(user_calender: list[list[str]]) -> int:
    # finding the max length of each string on the calendar
    max_length = 0
    for row in user_calender:
        for cell in row:
            if len(cell.strip()) > max_length:      # strip() takes spaces out
                max_length = len(cell.strip())
    return max_length + 2


def print_calendar(user_calender: list[list[str]]):
    column_width = get_column_width(user_calender)
    line = "-" * ((column_width + 1) * len(user_calender[0]) - 1)

    print(line)
    for i in range(len(user_calender)):
        print("|".join(cell.strip().center(column_width) for cell in user_calender[i]))
        if i == 0:
            print(line)      # divider under the day names
    print(line)


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

root = tk.Tk()
root.title("Calender")
root.geometry("1200x700")
root.grid_rowconfigure((0,1,2), weight=1,  uniform="a")
root.grid_columnconfigure((0,1,2), weight=1,  uniform="a")

time_preference = tk.Label(root)
inputTxt = tk.Text(root)
confirmButton = tk.Button(root)

bigFont = tkFont.Font(family="Ariel", size=20, weight="bold")
prefButton =tk.Button(root, text="Preference Button",font=bigFont, command=lambda :get_user_pref_tk_day(),bd=1)
prefButton.grid(row=1,column=1, sticky='ENSW')
root.mainloop()


print_preferences(user_pref)
newCalendar: list[list[str]] = course_maker(calendar, testCourseList)
print_calendar(newCalendar)
print()
print_course_summary(newCalendar)
#test

parser = argparse.ArgumentParser(prog="name", description="used to get the name of the user")
parser.add_argument("name", help="what name to save for the calender")

args = parser.parse_args()

add_user_cal(args.name, newCalendar)
cal_temp=  read_user_cal(args.name, calendar)


