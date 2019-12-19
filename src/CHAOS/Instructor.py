
from FunctionsUtil import *

# Status: Print Instructor's state
def Status(self, mode="RGB"):
    if   len(self.subjectColliding)>0:
        return "#FF6060"
    elif len(self.GetLeftSubjects())>0:
        return "#FFFF60"
    else:
        return "#60FF60"

# GetLeftSubjects: return list that instructor's class is not yet assigned
# Member Function of the Instructor
# Return
#   NoAssignEssential(list): Essential subject that student doesn't Assign
def GetLeftSubjects(self):
    NoAssignEssential=[]
    for i in self.subjectEnroll:
        NoAssignEssential.append(i)
    for stu_Ess in self.subjectEnroll:
        for stu_E in self.subjectAssign:
            if CheckSameSubjectbyName(self.parent.subjects[stu_Ess],self.parent.subjects[stu_E]):
                NoAssignEssential.remove(stu_Ess)
                break
    return NoAssignEssential

class Instructor:
    def __init__(self, idx=-1):
        self.idx = idx
        self.infoName = ""
        
        self.parent = None

        self.subjectAssign = list()
        self.subjectEnroll = list()
        self.subjectColliding = list()
        
        self.timeImpossible = list()
        self.timePrefer1st = list()
        self.timePrefer2nd = list()
        self.timePrefer3rd = list()

    GetLeftSubjects = GetLeftSubjects
    Status = Status
