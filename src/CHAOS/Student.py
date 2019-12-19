
from FunctionsUtil import *

# Status: Print Student's state
def Status(self, mode="RGB"):
    if   len(self.subjectColliding) > 0:
        return "#FF0000"
    elif len(self.GetLeftSubjects1st()) > 0:
        return "#FFFF60"
    elif len(self.GetLeftSubjects2nd()) > 0:
        return "#FFFF60"
    else:
        return "#60FF60"

# GetStudentLeftSubjects1st: return subject that not assigned
# Member Function of the Student
# Return
#   NoAssignEssential(list): Essential subject that student doesn't enroll
def GetLeftSubjects1st(self):
    NoAssignEssential=[]
    for i in self.subject1st:
        NoAssignEssential.append(i)
    for stu_Ess in self.subject1st:
        for stu_E in self.subjectAssign:
            if CheckSameSubjectbyName(self.parent.subjects[stu_Ess],self.parent.subjects[stu_E]):
                NoAssignEssential.remove(stu_Ess)
                break
    return NoAssignEssential

# GetStudentLeftSubjects: return subject that not assigned
# Member Function of the Student
# Return
#   NoAssignEssential(list): Non-Essential subject that student doesn't Assign
def GetLeftSubjects2nd(self):
    NoAssignEssential=[]
    for i in self.subject2nd:
        NoAssignEssential.append(i)

    for stu_Ess in self.subject2nd:
        for stu_E in self.subjectAssign:
            if CheckSameSubjectbyName(self.parent.subjects[stu_Ess],self.parent.subjects[stu_E]):
                NoAssignEssential.remove(stu_Ess)
                break
    return NoAssignEssential


class Student:
    def __init__(self, idx):
        self.idx = idx # Student ID
        self.infoGeneration = 0
        self.infoId = 0
        self.infoName = str(idx) # Temp
        self.parent = None
        self.subject1st = list()
        self.subject2nd = list()
        self.subjectColliding = list()
        self.subjectAssign = list() # Subject already enrolled

    Status = Status
    GetLeftSubjects1st = GetLeftSubjects1st
    GetLeftSubjects2nd = GetLeftSubjects2nd
