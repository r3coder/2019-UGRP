

from Student import Student
from Subject import Subject
from Instructor import Instructor
from Classroom import Classroom

# AddStudent: Add Student to simulation
# Member Function of the Simulation
# Input
#   args(dict) = inputed arguemnts
def AddStudent(self, args):
    s = Student(len(self.students))
    if "infoGeneration" in args:
        s.infoGeneration = args["infoGeneration"]
    if "infoId" in args:
        s.infoId = args["infoId"]
    if "subject1st" in args:
        s.subject1st = args["subject1st"]
    if "subject2nd" in args:
        s.subject2nd = args["subject2nd"]
    if "subjectEnroll" in args:
        s.subjectEnroll = args["subjectEnroll"]
    s.parent = self
    self.students.append(s)

# AddSubject: Add subject to simulation
# Member Function of the Simulation
# Input
#   args(dict) = inputed arguments
def AddSubject(self, args):
    s = Subject(len(self.subjects))
    if "command" in args:
        s.command = args["command"]
    if "commandIdx" in args:
        s.commandIdx = args["commandIdx"]
    if "commandSubSame" in args:
        s.commandSubSame = args["commandSubSame"]
    if "commandSubClose" in args:
        s.commandSubClose = args["commandSubClose"]
    if "commandSubDiffHour" in args:
        s.commandSubDiffHour = args["commandSubDiffHour"]
    if "commandSubDiffDay" in args:
        s.commandSubDiffDay = args["commandSubDiffDay"]
    if "infoCode" in args:
        s.infoCode = args["infoCode"]
    if "infoCreditTotal" in args:
        s.infoCreditTotal = args["infoCreditTotal"]
    if "infoCreditClass" in args:
        s.infoCreditClass = args["infoCreditClass"]
    if "infoCreditPractice" in args:
        s.infoCreditPractice = args["infoCreditPractice"]
    if "infoDivision" in args:
        s.infoDivision = args["infoDivision"]
    if "infoInstructor" in args:
        s.infoInstructor = args["infoInstructor"]
    if "infoLocation" in args:
        s.infoLocation = args["infoLocation"]
    if "infoMemo" in args:
        s.infoMemo = args["infoMemo"]
    if "infoName" in args:
        s.infoName = args["infoName"]
    if "mode" in args:
        s.mode = args["mode"]
    if "studentAttend" in args:
        s.studentAttend = args["studentAttend"]
    if "studentCapacity" in args:
        s.studentCapacity = args["studentCapacity"]
    if "subjectExclude" in args:
        s.subjectExclude = args["subjectExclude"]
    if "timeIsAssigned" in args:
        s.timeIsAssigned = args["timeIsAssigned"]
    if "timeIsFixed" in args:
        s.timeIsFixed = args["timeIsFixed"]
    if "timeAssignedSplit" in args:
        s.timeAssignedSplit = args["timeAssignedSplit"]
    if "timeAssignedTime" in args:
        s.timeAssignedTime = args["timeAssignedTime"]
    if "timeAssignedClassroom" in args:
        s.timeAssignedClassroom = args["timeAssignedClassroom"]
    if "timePrefer" in args:
        s.timePrefer = args["timePrefer"]
    if "timeExclude" in args:
        s.timeExclude = args["timeExclude"]
    if "examOn" in args:
        s.examOn = args["examOn"]
    if "examLectureOnExam" in args:
        s.examLectureOnExam = args["examLectureOnExam"]
    if "examLength" in args:
        s.examLength = args["examLength"]
    if "examIsAssigned" in args:
        s.examIsAssigned = args["examIsAssigned"]
    if "examAssignedLectureTime" in args:
        s.examAssignedLectureTime = args["examAssignedLectureTime"]
    if "examAssignedClassroom" in args:
        s.examAssignedClassroom = args["examAssignedClassroom"]
    if "examTimePrefer" in args:
        s.examTimePrefer = args["examTimePrefer"]
    if "examDivisionUniteList" in args:
        s.examDivisionUniteList = args["examDivisionUniteList"]

    if s.infoCode[2] in ["1", "2"]:
        s.timeExclude.append((1,9,0,60))
        s.timeExclude.append((3,9,0,60))

    s.parent = self
    self.subjects.append(s)

# AddInstructor: Add Instructor to simualtion
# Member Function of the Simulation
# Input
#   args(dict) = inputed arguments
def AddInstructor(self, args):
    s = Instructor()
    s.idx = len(self.instructors)
    if "infoName" in args:
        s.infoName = args["infoName"]
    if "subjectAssign" in args:
        s.subjectAssign = args["subjectAssign"]
    if "subjectEnroll" in args:
        s.subjectEnroll = args["subjectEnroll"]
    if "timeImpossible" in args:
        s.timeImpossible = args["timeImpossible"]
    if "timePrefer1st" in args:
        s.timePrefer1st = args["timePrefer1st"]
    if "timePrefer2nd" in args:
        s.timePrefer2nd = args["timePrefer2nd"]
    if "timePrefer3rd" in args:
        s.timePrefer3rd = args["timePrefer3rd"]
    s.parent = self
    self.instructors.append(s)

# AddClassroom: Add Classroom to simulation
# Input
#   args(dict) = inputed arguments
def AddClassroom(self, args):
    s = Classroom(len(self.instructors))
    if "infoCode" in args:
        s.infoCode = args["infoCode"]
    if "infoName" in args:
        s.infoName = args["infoName"]
    if "infoIsAssignable" in args:
        s.infoIsAssignable = args["infoIsAssignable"]
    if "subjectAssignable" in args:
        s.subjectAssignable = args["subjectAssignable"]
    if "infoIsRecordable" in args:
        s.infoIsRecordable = args["infoIsRecordable"]
    if "infoBoardType" in args:
        s.infoBoardType = args["infoBoardType"]
    if "infoShape" in args:
        s.infoShape = args["infoShape"]
    if "infoCapacity" in args:
        s.infoCapacity = args["infoCapacity"]
    if "infoIsProjector" in args:
        s.infoIsProjector = args["infoIsProjector"]

    s.parent = self
    self.classrooms.append(s)

