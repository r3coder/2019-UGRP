# Student.py
# Holding student class implementation

import Util

class Student:
    # PrintExamTimetable: prints timetable
    # - Input argument
    #   s(list(Subject)): subject classes
    def PrintExamTimetable(self, s, mode = 2):
        print(str(self.id)+"'s Exam table")
        if mode==1 or mode == 0:
            for i in self.subjectEnrolled:
                if s[i].isExam == True:
                    stt = "(FIXED)" if s[i].isFixed else ""
                    print("    {:3d} {:s} {:s}:{:s}".format(s[i].codeIndex, stt, s[i].name, Util.TimeTupleListToHumanStr(s[i].timeExam)))
        if mode==2 or mode == 0:
            # Only works on int mode
            res=list()
            for i in range(5):
                res.append([0]*48)
            myind = 1
            for i in self.subjectEnrolled:
                if s[i].isExam == True:
                    for k in s[i].timeExam:
                        res[k[0]][k[1]] = myind
                    myind+=1
            for i in range(24):
                print("{:2d}".format(i),end="")
            print()
            for i in res:
                for val in i:
                    if val==0: print("-",end="")
                    else: print("{:1d}".format(val),end="")
                print()
        print()

    # EnrollClass: enroll class to student
    # - Input argument
    #   s(Subject): subject class to enroll
    # Student.EnrollSubject(Subject) is same as Subject.EnrollStudent(Student)
    def EnrollSubject(self, s):
        assert s.codeSurvey in self.subjectSurvey
        self.subjectSurvey.remove(s.codeSurvey)
        self.subjectEnrolled.append(s.codeSubject)
        if self.id not in s.studentAttend:
            s.studentAttend.append(self.id)
    
    # DismissClass: dismiss student from class
    # - Input argument
    #   s(Subject): subject class to dismiss
    # Student.DismissSubject(Subject) is same as Subject.DismissStudent(Student)
    def DismissSubject(self, s):
        assert s.codeSubject in self.subjectEnrolled
        self.subjectSurvey.append(s.codeSurvey)
        self.subjectEnrolled.remove(s.codeSubject)
        if self.id in s.studentAttend:
            s.studentAttend.remove(self.id)
    
    # Initialize Student Class with survey code and timetable weight
    def __init__(self, i, g, survey=[], weight=[]):
        self.id = i # Student ID
        self.grade = g # Student Grade
        self.subjectSurvey = survey # Subject code from survey
        self.subjectEnrolled = [] # Subject already enrolled
        self.timetableWeight = weight # Timetable weight
        self.enrolledCredit = 0 # Enrolled Credit
    
