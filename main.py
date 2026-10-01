#section class that keeps track of what day and times the classes happen in

def get_user_pref() -> list[list[str]]:
    days = ["Monday ", "Tuesday ", "Wednesday ", "Thursday ", "Friday "]
    pref = []

    print ("Time of day preferences:")
    print("1. Morning (08:00 - 12:00)")
    print("2. Afternoon (12:00 - 16:00)")
    print("3. Evening (16:00 - 20:00)")
    print("4. No preference\n")


    for i in range(len(days)):
        while True:
            choose = input(f"Please choose from 1-4 for {days[i]}")

            if choose == "1":
                pref.append([days[i], "Morning"])
                break

            elif choose == "2":
                pref.append([days[i], "Afternoon"])
                break

            elif choose == "3":
                pref.append([days[i], "Evening"])
                break

            elif choose == "4":
                pref.append([days[i], "Any"])
                break

            else:
                print("Not a valid choice.")


    return pref
            






class section:
    def __init__(self, day: str, time_start: str, time_end: str):
        self.day=day
        self.time_start=time_start
        self.time_end=time_end

#courses to keep track of the name and the sections that the classes happen in
class course:
    def __init__(self, name: str, slot1: section, slot2: section = None):
        self.name=name
        self.slot1=slot1
        self.slot2=slot2

# turns the time into minutes so that its easier to check for breaks  
def minutes(time):
    time=time.split(":")
    return int(time[0])*60+int(time[1])

def course_maker(courses : list[list[course]], courseList:list[course]):


    #goes through the list of course objects
    for x in range (len(courseList)):
        #used later
        available = True

        #goes through the list in the list of courses
        for i in range (1, len(courses)):
            #checks to see if it's the start time of the first slot, *replace() lets us format the calendar
            if courseList[x].slot1.time_start==courses[i][0].replace(" ", ""):

                #goes through the list of list again
                for j in range (0, len(courses)):
                    #checks to see if it's the end time of the first slot
                    if courseList[x].slot1.time_end==courses[j][0].replace(" ", ""):

                        #goes through the first list of the 2d array
                        for k in range (len(courses[0])):

                            #
                            if courseList[x].slot1.day==courses[0][k].replace(" ", "") and courses[i][k]== "":

                                #gets the start and end time for each class
                                start=minutes(courseList[x].slot1.time_start)
                                end=minutes(courseList[x].slot1.time_end)

                                # goes through all the times on specific days
                                for row in range (1, len(courses)):
                                    row_time=minutes(courses[row][0].replace(" ", ""))

                                    #chceks 30 mins before and after the class 
                                    if row_time>start-30 and row_time<end+30:

                                        #if another class is there, it will not add the break to the schedule
                                        if courses[row][k]!="":
                                            available=False
                    

                                if available:
                                    for l in range (i,j+1):
                                        courses[l][k] = courseList[x].name

        available= any(courseList[x].name in Slots for Slots in courses)


        #slot 2 for lectures
        if courseList[x].slot2 is not None:
            for i in range (1, len(courses)):
                if(not available):
                    break
                if courseList[x].slot2.time_start==courses[i][0].replace(" ", ""):
                    for j in range (i, len(courses)):
                        if courseList[x].slot2.time_end==courses[j][0].replace(" ", ""):
                            for k in range (len(courses[0])):
                                if courseList[x].slot2.day==courses[0][k].replace(" ", "") and courses[i][k]== "":
                                    for l in range (i,j+1):
                                        courses[l][k] = courseList[x].name
                                elif courseList[x].slot2.day==courses[0][k].replace(" ", "") and courses[i][k]!= "":
                                    available=False
                                    print("f")

        if not available:
            for i in range (len(courses)):
                for j in range(len(courses[i])):

                    if courses[i][j]==courseList[x].name:

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



CSCI1061UA=section("Tuesday", "15:40", "17:00")
CSCI1061UB=section("Thursday", "15:40", "17:00")
CSCI1061UC=section("Thursday", "14:10", "15:30")
CSCI1061UD=section("Monday", "14:10", "15:30")

CSCI1061ULABA=section("Tuesday", "17:10", "20:00")
CSCI1061ULABB=section("Friday", "14:10", "17:00")
CSCI1061ULABC=section("Thursday", "17:10", "20:00")
CSCI1061ULABD=section("Tuesday", "08:10", "11:00")
CSCI1061ULABE=section("Friday", "08:10", "11:00")


#CSCI 1050U arch

CSCI1050UA=section("Thursday", "12:40", "14:00")
CSCI1050UB=section("Wednesday", "12:40", "14:00")
CSCI1050UC=section("Thursday", "12:40", "14:00")
CSCI1050UD=section("Wednesday", "12:40", "14:00")

CSCI1050ULABA=section("Thursday", "08:10", "11:00")
CSCI1050ULABB=section("Tuesday", "14:10", "17:00")
CSCI1050ULABC=section("Tuesday", "11:10", "14:00")
CSCI1050ULABD=section("Tuesday", "17:10", "20:00")


#MATH 1020U  calc II

MATH1020UA=section("Wednesday", "08:10", "09:30")
MATH1020UB=section("Monday", "12:10", "13:30")
MATH1020UC=section("Friday", "17:10", "18:30")

MATH1020UTUTA=section("Thursday", "08:10", "09:30")
MATH1020UTUTB=section("Tuesday", "08:10", "09:30")
MATH1020UTUTC=section("Wednesday", "08:10", "09:30")

#PHY 1020U Physcis II

PHY1020UA=section("Wednesday", "12:40", "14:00")
PHY1020UB=section("Thursday", "12:40", "14:00")



csci1061_lecs = [CSCI1061UA, CSCI1061UB, CSCI1061UC, CSCI1061UD]
csci1061_labs = [CSCI1061ULABA, CSCI1061ULABB, CSCI1061ULABC, CSCI1061ULABD, CSCI1061ULABE]

csci1050_lecs = [CSCI1050UA, CSCI1050UB, CSCI1050UC, CSCI1050UD]
csci1050_labs = [CSCI1050ULABA, CSCI1050ULABB, CSCI1050ULABC, CSCI1050ULABD]

math1020_lecs = [MATH1020UA, MATH1020UB, MATH1020UC]
math1020_tuts = [MATH1020UTUTA, MATH1020UTUTB, MATH1020UTUTC]

phy1020_lecs = [PHY1020UA, PHY1020UB]






PHY = course("PHY 101", PHY1020UA, PHY1020UB,)

CALC = course("CALC 102", MATH1020UA, MATH1020UTUTA,)


testCourseList: list[course] = [CALC, PHY]

newCalendar: list[list[course]] = course_maker(calendar, testCourseList)


user_pref = get_user_pref()
print("\nYour schedule with preferred times of day:\n")
for pref in user_pref:
    print(pref[0].center(10) + ": " + pref[1].center(10))

print("")

# finding the max length of each string on the calendar
max_length = 0
for row in newCalendar:
    for cell in row:
        if len(cell.strip()) > max_length:      #strip() takes spaces out of
            max_length = len(cell.strip()) 

column_width = max_length + 2


for row in newCalendar:
    print("|".join(cell.strip().center(column_width) for cell in row))