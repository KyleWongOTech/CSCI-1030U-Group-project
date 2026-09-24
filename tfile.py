#section class that keeps track of what day and times the classes happen in
class section:
    def __init__(self, day: str, time_start: str, time_end: str):
        self.day=day
        self.time_start=time_start
        self.time_end=time_end

#courses to keep track of the name and the sections that the classes happen in
class course:
    def __init__(self, name: str, slot1: section, slot2: section):
        self.name=name
        self.slot1=slot1
        self.slot2=slot2

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
                                for l in range (i,j+1):
                                    courses[l][k] = courseList[x].name

        available= any(courseList[x].name in Slots for Slots in courses)


        #slot 2 for lectures
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
calender: list[list[str]] = [["  Time    ", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                            ["  8:00    ","","","","","",""],
                            ["  8:10    ","","","","","",""],
                            ["  8:30    ","","","","","",""],
                            ["  8:40    ","","","","","",""],
                            ["  9:00    ","","","","","",""],
                            ["  9:10    ","","","","","",""],
                            ["  9:30    ","","","","","",""],
                            ["  9:40    ","","","","","",""],
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

#prints out the empty course schedule
for i in range(len(calender)):

    print(calender[i])



CSCI1061UA=section("Tuesday", "15:40", "17:00")
CSCI1061UB=section("Thursday", "15:40", "17:00")
CSCI1061UC=section("Thursday", "14:10", "15:30")
CSCI1061UD=section("Monday", "14:10", "15:30")

CSCI1061ULABA=section("Tuesday", "17:10", "20:00")
CSCI1061ULABB=section("Friday", "14:10", "17:00")
CSCI1061ULABC=section("Thursday", "17:10", "20:00")
CSCI1061ULABD=section("Tuesday", "8:10", "11:00")
CSCI1061ULABE=section("Friday", "8:10", "11:00")


#CSCI 1050U arch

CSCI1050UA=section("Thursday", "12:40", "14:00")
CSCI1050UB=section("Wednesday", "12:40", "14:00")
CSCI1050UC=section("Thursday", "12:40", "14:00")
CSCI1050UD=section("Wednesday", "12:40", "14:00")

CSCI1050ULABA=section("Thursday", "8:10", "11:00")
CSCI1050ULABB=section("Tuesday", "14:10", "17:00")
CSCI1050ULABC=section("Tuesday", "11:10", "14:00")
CSCI1050ULABD=section("Tuesday", "17:10", "20:00")


#MATH 1020U  calc II

MATH1020UA=section("Wednesday", "8:10", "9:30")
MATH1020UB=section("Monday", "12:10", "13:30")
MATH1020UC=section("Friday", "17:10", "18:30")

MATH1020UTUTA=section("Thursday", "8:10", "9:30")
MATH1020UTUTB=section("Tuesday", "8:10", "9:30")
MATH1020UTUTC=section("Wednesday", "8:10", "9:30")

#PHY 1020U Physcis II

PHY1020UA=section("Wednesday", "12:40", "14:00")
PHY1020UB=section("Thursday", "12:40", "14:00")

PHY = course("PHY 101", PHY1020UA, PHY1020UB)


testCourseList: list[course]=[PHY]

newCalender:list[list[course]]=course_maker(calender,testCourseList)


for i in range(len(newCalender)):
    print(newCalender[i])