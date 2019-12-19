# Subject.py
# Holding subject class implementation

import Util

class Subject:

    # GetTime: get assigned time for this class
    def GetTime(self):
        if self.isTimeAssigned: return self.time
        else: return []

    # EnrollStudent : enroll student to class
    # - Input argument
    #   s(Student): student Class to enroll
    # Student.EnrollSubject(Subject) is same as Subject.EnrollStudent(Student)
    def EnrollStudent(self, s):
        s.EnrollSubject(self)
    
    # DismissClass: dismiss student from class
    # - Input argument
    #   s(Student): student class to dismiss
    # Student.DismissSubject(Subject) is same as Subject.DismissStudent(Student)
    def DismissStudent(self, s):
        s.DismissSubject(self)
    
    # GetLectureStr: get lecture string
    def GetLectureStr(self, index = 0):
        fix = ""
        if self.isExamOnLecture: fix = "FIX"
        res = str(self.codeIndex) + " " + fix + self.name + " (" + self.codeSchool +"-"+str(self.division)+ ")"
        # if type(self.locationStr) == list:
            # if len(self.locationStr) == 0: res += ""
            # else: res += self.locationStr[index]
        # else: res += str(self.locationStr)
        # if type(self.instructorStr) == list: res += ") " + Util.ListToStr(self.instructorStr," ")
        # else: res += ") " + self.instructorStr
        return res

    def SetLectureData(self, data):
        # Basic information
        self.name = data["Name"] # Subject Name
        self.codeSchool = data["CodeSchool"] # Subject code by school (ex) SE101-01
        self.codeSurvey = data["CodeSurvey"] # Code from survey
        self.codeSubject = data["Id"] # Code from subject list
        self.credit = data["Credit"]
        self.timeLecture = data["TimeLecture"]
        self.timeRecital = data["TimeRecital"]
        self.targetGrade = data["TargetYear"]
        self.attendLimit = data["StudentLimit"] # Limit of Student
        self.instructorStr = data["Professor"] # instructor information. If you want to use as int, you have to call Util.ConvertInstructorStrToId in your script
        self.instructor = list()
        
        # Survey
        self.timeSplit = data["Split"]
        self.isDayAvailable = data["IsDay"]
        self.isNightAvailable = data["IsNight"]
        self.isTimeFixed = False
        self.timeFixed = data["TimeFixed"]
        
        # Timetable
        self.time = list() # Time assigned, could be list(int) or list(tuple). Use as you want
        self.locationStr = []
        self.location = []
        
        # Assign
        self.availableClassroom = data["ClassRoom"]
        self.studentAttend = [] # Attended student id
    

    def AddTimeLectures(self, l):
        for i in l:
            self.timeLecture.append(i)
            self.time.append(i)
    
    def AddStudent(self, i):
        self.studentAttend.append(i)
    
    def PrintExamInfo(self):
        for item in vars(self).items():
            print(item)
        print("timeExam Convenient")
        for i in range(24): print("{:2d}".format(i),end="")
        print()
        for i in range(5):
            for j in range(48):
                if (i,j) in self.timeExam: print("@",end="")
                else: print("-",end="")
            print()
        print() 

    def __init__(self, index, mode):
        self.name = ""
        self.codeSchool = ""
        self.codeIndex = index
        self.instructorStr = list()
        self.instructor = list()
        self.locationStr = list()
        self.location = list()
        self.time = list()
        self.studentAttend = list()
        self.memo = ""
        self.isTimeSet = False

        if mode=="Exam":
            self.timeLecture = list()
            self.timeExam = list()
            
            # self.timeUnavail = list()
            # self.timeDesired = list()

            self.isExam = False
            self.examLength = 0
            self.isExamOnLecture = False
            self.divisionUnite = list()
            self.divisionClassroom = list()
            self.isLectureOnExam = False
            self.lectureOnExamIndex = list()
            
            self.isFixed = False
            self.fixedTime = list()
            self.desiredTime = list()

