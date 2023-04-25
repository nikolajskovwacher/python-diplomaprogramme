######## Minor programme class

class MinorProgramme:
    all_courses = {} # key is program_id, values are courseID's from courses in the program
    grad_students = {} # key is program_id, values are student ID's for those who are eligible for graduating
    grad_w_distinction_students = {} # same, but onlystudents who are  graduation with distinction

    def __init__(self, name, id):
        self.name = name # name of minor programme
        self.id = id # name of minor programme
        self.all_courses[id] = [] # save minor to list
        self.grad_students[id] = []
        self.grad_w_distinction_students[id] = []

    def add_courses(self,courseID):
        tmp_ls = [] #temporary list 
        #check whether a course is in the system or not
        for c in courseID:
            if not c in Courses.courses_in_system:
                print("Error: "+ str(c) +" as courseID does not exist.")
            else:
                tmp_ls.append(c)
        self.all_courses[self.id] += tmp_ls
            
    def remove_courses(self,courseID):
        try:
            for c in courseID:
                self.all_courses[self.id].remove(c)
        except Exception as e:
            # prints the exception name, as well as the error that occured
            print(f"[{e.__class__.__name__}]: Course ID does not match up with courses in programe")


######## Courses class

class Courses:
    #a list of all courses in the system (ID)
    courses_in_system = []
    def __init__(self, name, id):
        self.name = name # name of course
        self.id = id # course id (eg.101)
        #update list containing all courses in system
        self.courses_in_system.append(id)

class Student(object):
    dic_all = {} #list of all student id's
    def __init__(self,firstname,lastname, birthday, nationality):
        # store personal infos about student
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.nationality = nationality
        # auto generated information
        self.email = str(firstname) + "." + str(lastname) + "@datascience.com" #assign a email to student
        self.student_id = gen_unique_id(firstname,lastname,birthday)
        # store courses & assignments of enrolled classes
        self.course_dic = {} # every student has their own course_dic. It's an summary of their achievements. Keys --> courses, Values: List containing assignment progress 
        self.dic_all[self.student_id] =  str(firstname) + " " + str(lastname) #save student in dic_all

    def updateinfo(self,firstname,lastname,birthday,nationality):
        # update personal infos about student
        self.student_id = gen_unique_id(firstname,lastname,birthday)
        self.firstname = firstname
        self.lastname = lastname
        self.birthday = birthday
        self.nationality = nationality

    def enroll_inprogram(self,programID):
        # this function enrolls the student automatically to all courses by program'id
        ls_courses = MinorProgramme.all_courses[programID]
        try:
            for c in ls_courses: # iterate through list, call enroll function
                self.enroll(c)
        except Exception as e:
            print(f"[{e.__class__.__name__}]: ProgramID does not match with any Programs")

    def enroll(self,courseid):
        try: # check first if there is a course with matching id
            self.course_dic[courseid] = [False,False,False,False,False] # a course has always 5 assignments
        except Exception as e:
            # prints the exception name, as well as the error that occured
            print(f"[{e.__class__.__name__}]: Course ID does not match with any courses")

    def deroll(self,course):
        try:
            # if course in self.course_dic
            del self.course_dic[course]
        except Exception as e:
            # prints the exception name, as well as the error that occured
            print(f"[{e.__class__.__name__}]: Course ID does not match up with enrolled courses")

    def check_if_passed(self, courseid):
        # this function checks whether a course is passed
        count= 0
        for i in self.course_dic[courseid]:
            if i == True:
                count += 1
        if count >= 3:
            return True
        else: return False

    def check_if_grad(self):
        # check if every course in program is passed
        count, total_assignments_passed = 0,0
        ls_courses = ds_minor.all_courses["ds22"]
        nofcip = len(ls_courses) #number_of_courses_in_programme

        for c in ls_courses: # list containing all course id's of program
            if self.check_if_passed(c) == True: count +=1
        if count == nofcip: # all courses passed, ready for graduation
            if not self.student_id in MinorProgramme.grad_students["ds22"]: #check if student is already in dictionary list
                MinorProgramme.grad_students["ds22"].append(self.student_id)

        # count total passed assignemnts, if equal or greater that 17: pass with distinction
        for c in ls_courses: # loop through all courses ahich are part of the program
            for i in self.course_dic[c]: # self.course_dic[c] is a list containing assignment progress
                if i == True: total_assignments_passed += 1
        if total_assignments_passed >= 17: # ready for graduation with distinction
            if not self.student_id in MinorProgramme.grad_w_distinction_students["ds22"]: #check if student is already in dictionary list
                MinorProgramme.grad_w_distinction_students["ds22"].append(self.student_id)

    def passfail_assignmemt(self,courseID,assignment_nr,True_ifpassed):
        # update grading on mandatory assignment
        tmp_ls = list(self.course_dic[courseID])
        tmp_ls[assignment_nr-1] = True_ifpassed
        self.course_dic.update({courseID: tmp_ls})
        self.check_if_grad() # call fucntion to check if student is passing with this grading

    def show_allinfos(self):
        print("Name:        " + self.firstname + " " + self.lastname)
        print("Student ID:  " + str(self.student_id))
        print("Birthday:    " + self.birthday)
        print("Nationality: " + self.nationality)
        print("E-mail :     " + self.email)


######## Create a unique ID for each student

def gen_unique_id(firstname,lastname,birthday):
    # this function generates a six-digit integer id based on input values
    id_int_bd = int("3"+ birthday[0:2]+birthday[-2:]) # save the year and day to a integer digit
    id_l, id_f = 0,0
    for char in lastname: id_l += ord(char) # sum up integer value of character of lastname 
    for char in firstname: id_f += ord(char) # same sum with firstname
    unique_id = str(round((id_l/id_f)*id_int_bd,6))
    uni_id = int(unique_id[-6:])
    return uni_id

# For printing dictionaries prettier
def dic_print(dictionary,with_value = None):
    for key, value in dictionary.items() :
        if not with_value == True: value = "" # whether to print whole dictionary or just its keys
        print(key, value)


###########
# Testing #
###########

# add a minor programm (with name and unique id)
ds_minor = MinorProgramme("Data Science","ds22")

# add all courses to system
c1 = Courses("Python Programming Course", 101)
c2 = Courses("Data Mining and Machine Learning Course", 201)
c3 = Courses("Visual Analytics Course", 301)
c4 = Courses("Text Analytics Course", 401)
c34 = Courses("C++", 102)
c75 = Courses("Java", 404)

# establish a Curriculum by adding courses to the minor program
ds_minor.add_courses([101,201,301,401,404])
ds_minor.remove_courses([404]) # remove unwanted course(s) from minor program

# add students to system
s1 = Student("daniel","german","28-04-1998","german")
s2 = Student("jacob","herringesen","08-01-1970","united states")
s3 = Student("nikolaj","wacher","28-04-2000","united states")
s4 = Student("daviid","petersen","28-04-1980","french")

# enroll students in minor program, therfore enroll them to all courses which are part of the program
s1.enroll_inprogram("ds22")
s2.enroll_inprogram("ds22")
s3.enroll_inprogram("ds22")

# passing students assignments
# True = passing; False = failing (by default)
s1.passfail_assignmemt(101,1,True)
s1.passfail_assignmemt(101,2,True)
s1.passfail_assignmemt(101,3,True)
s1.passfail_assignmemt(101,4,True)
s1.passfail_assignmemt(101,5,True)

s2.passfail_assignmemt(101,1,True)
s2.passfail_assignmemt(101,2,True)
s2.passfail_assignmemt(101,3,True)
s2.passfail_assignmemt(101,4,True)

# lets say student 3 is a fast learner and he passed all assignments
for courseid in ds_minor.all_courses["ds22"]:
    for x in range(5):
        s3.passfail_assignmemt(courseid,x+1,True)


######## Test cases

# Printing all course IDs in the diploma programme
dic_print(ds_minor.all_courses, True)

# Print a list of all students in the system
dic_print(Student.dic_all,True) # a list of all students in the system with name & id

# Print information on an individual student
s1.show_allinfos() #shows main information on single student

# Print an individual student's (s3) completed mandatory assignments by course ID
dic_print(s3.course_dic, True)

# Print whether a single course has been passed for an individual student (s1)
print(s1.check_if_passed(101))

# Print the diploma programme's graduating students IDs
dic_print(MinorProgramme.grad_students,True)

# Print the diploma programme's graduating with distinction students IDs
dic_print(MinorProgramme.grad_w_distinction_students,True)

# Enrolling students in other courses than the programs
s1.enroll(102)
dic_print(s1.course_dic) #Print list of courses student is enrolled in