# CSCI-1030U-Group-project
Group project 

The point of the program is to help students with course selection. The program which already contains the list of courses will take inputs from users on what classes they need and what times they would not like to have classes and then create the best schedule possible with the set conditions given.


course_maker function: it takes in a 2D list of the course class and a 1D list of the course class as parameters. It will then check the first column of the 2D array, and if the start time for the course in the x element of the 1D list, it will move on. Then it will see where the end time is for the class it then sorts through the first list in the 2D list which contains all the days and checks to see which day aligns with the class days and if the time slot desired in that day is empty. If both conditions are true it will then add the class name to the 2D list starting from the start time to the end time which was tracked in the for loops earlier. At the end, it checks to see if it added any courses; if it did not, it turns the ‘available’ variable to false, and the second loop breaks early. The second loop is the same as the first, but it’s made for the second class of the week, and its method of detecting if the class time doesn't work is a little bit different. If the second check does not work, it removes all occurrences of the name of the class.

