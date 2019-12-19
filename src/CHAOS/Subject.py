
from FunctionsTime import TimeToText

# Status: Print Subject's state
def Status(self, mode="RGB"):
    if   self.TimeIsAllAssigned() == False:
        return "#FFFF60"
    elif len(self.subjectCollidingInstructor):
        return "#FF6060"
    elif len(self.subjectCollidingStudent):
        return "#AAFF60"
    else:
        return "#60FF60"
#TimeIsAllAssigned: return subject is assign(bool)
def TimeIsAllAssigned(self):
    for i in self.timeIsAssigned:
        if i==False:
            return False
    return True

#TimeIsAllFixed: return subject is assign(bool)
def TimeIsAllFixed(self):
    for i in self.timeIsFixed:
        if i==False:
            return False
    return True

# StatusTime: return Subject's stateTime
def StatusTime(self, ind, mode="RGB"):
    if   self.timeIsFixed[ind]:
        return "#606060"
    else:
        if self.timeIsAssigned[ind]:
            return "#60FF60"
        else:
            return "#FFFF60"

def TimeAssignedString(self):
    tt = ""
    for ind ,t in enumerate(self.timeAssignedTime):
        tt+=TimeToText((t[0],t[1],t[2],self.timeAssignedSplit[ind]))
        tt+=", "
    return tt

def TimeType(self):
    if    self.timeAssignedSplit == [90,90]:        return 1
    elif  self.timeAssignedSplit == [180,180]:      return 0
    elif  self.timeAssignedSplit == [120]:          return 2
    elif  self.timeAssignedSplit == [180]:          return 3
    elif  self.timeAssignedSplit == [240]:          return 4
    elif  self.timeAssignedSplit == [60]:          return 5
    elif  self.timeAssignedSplit == [90,90,120] and self.idx in [0, 1, 2, 3]: return 6 # Not done yet
    elif  self.timeAssignedSplit == [90,90,120]:    return 7 # Not done yet
    else:                                           return 0


class Subject:
    def __init__(self, idx, mode = 1):
        self.idx = idx
        self.mode = mode

        self.command = False
        self.commandIdx = list()
        self.commandSubSame = list() # same time
        self.commandSubClose = list() # as close as possible
        self.commandSubDiffHour = list() # other hour
        self.commandSubDiffDay = list() # other day > subdiffDay

        self.infoCode = "" # Class Code ex) SE101
        self.infoCreditTotal = 0
        self.infoCreditClass = 0
        self.infoCreditPractice = 0
        self.infoDivision = 1 # Class division
        self.infoInstructor = list() # Instructor idx ex) [0, 5, 11]
        self.infoLocation = list() # Location idx, same length with infoClassLength ex) [0, 0]
        self.infoMemo = ""
        self.infoName = ""
        self.parent = None
        
        self.studentAttend = list()
        self.studentCapacity = list()

        self.subjectCollidingInstructor = list()
        self.subjectCollidingStudent = list()
        self.subjectExclude = list()

        self.timeIsAssigned = list()
        self.timeIsFixed = list()
        self.timeAssignedSplit = list() # Split of the class by minute ex) [90, 90]
        self.timeAssignedTime = list()
        self.timeAssignedClassroom = list()

        self.examOn = False
        self.examLectureOnExam = False
        self.examLength = 0
        self.examAssignedLectureTime = list()
        self.examAssignedLectureSplit = list()
        self.examAssignedLectureClassroom = list()
        self.examTimePrefer = list()
        self.examDivisionUniteList = list()

        self.timePrefer = list()
        self.timeExclude = list()


    Status = Status
    StatusTime = StatusTime
    TimeAssignedString = TimeAssignedString
    TimeIsAllAssigned = TimeIsAllAssigned
    TimeIsAllFixed = TimeIsAllFixed
    TimeType = TimeType
