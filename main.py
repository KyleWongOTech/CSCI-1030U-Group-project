
#initializes the course schedule
courses: list[list[str]] = [["  Time    ", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                            ["  8:00    ","","","a","","",""],
                            ["  9:00    ","","","","","",""],
                            ["  10:00   ","","","","","",""],
                            ["  11:00   ","","","","","",""],
                            ["  12:00   ","","","","","",""],
                            ["  13:00   ","","","","","",""],
                            ["  14:00   ","","","","","",""],
                            ["  15:00   ","","","","","",""],
                            ["  16:00   ","","","","","",""],
                            ["  17:00   ","","","","","",""],
                            ["  18:00   ","","","","","",""],
                            ["  19:00   ","","","","","",""],
                            ["  20:00   ","","","","","",""],]

#prints out the empty course schedule
for i in range(len(courses)):
    print(courses[i])

#section class that keeps track of what day and times the classes happen in
class section:
    def __init__(self, day: str, time_start: str, time_end: str)-> None:
        self.day=day
        self.time_start=time_start
        self.time_end=time_end

#courses to keep track of the name and the sections that the classes happen in
class course:
    def __init__(self, name: str, slot1: section, slot2: section)-> None:
        self.name=name
        self.slot1=slot1
        self.slot2=slot2

#creating section objects
testSection1=section("Monday", "8:00", "12:00")
testSection2=section("Wednesday", "8:00", "9:00")

testSection3=section("Monday", "13:00", "15:00")
testSection4=section("Thursday", "11:00", "15:00")

#creating course objects
testCourse1=course("Math 101", testSection3, testSection4)
testCourse2=course("Physic 101", testSection1, testSection2)

#creating a list of the course object
testCourseList: list[course]=[testCourse2, testCourse1]

#goes through the list of course objects
for x in range (len(testCourseList)):
    #used later
    available = True;

    #goes through the list in the list of courses
    for i in range (1, len(courses)):
        #checks to see if its the start time of the first slot, *replace() lets us format the calender
        if(testCourseList[x].slot1.time_start==courses[i][0].replace(" ","")):

            #goes through the list of list again
            for j in range (0, len(courses)):
                #checks to see if its the end time of the first slot
                if ( testCourseList[x].slot1.time_end==courses[j][0].replace(" ","")):

                    #goes through the first list of the 2d array
                    for k in range (len(courses[0])):

                        #
                        if (testCourseList[x].slot1.day==courses[0][k].replace(" ","") and courses[i][k]==""):
                            for l in range (i,j+1):
                                courses[l][k] = testCourseList[x].name

    available= any(testCourseList[x].name in Slots for Slots in courses)


    #slot 2 for lectures
    for i in range (1, len(courses)):
        if(not available):
            break;
        if(testCourseList[x].slot2.time_start==courses[i][0].replace(" ","")):
            for j in range (i, len(courses)):
                if ( testCourseList[x].slot2.time_end==courses[j][0].replace(" ","")):
                    for k in range (len(courses[0])):
                        if (testCourseList[x].slot2.day==courses[0][k].replace(" ","") and courses[i][k]==""):
                            for l in range (i,j+1):
                                courses[l][k] = testCourseList[x].name
                        elif(testCourseList[x].slot2.day==courses[0][k].replace(" ","") and courses[i][k]!=""):
                            available=False;
                            print("f");

    if (not available):
        for i in range (len(courses)):
            for j in range(len(courses[i])):

                if (courses[i][j]==testCourseList[x].name):

                    courses[i][j]=""


for i in range(len(courses)):
    print(courses[i])