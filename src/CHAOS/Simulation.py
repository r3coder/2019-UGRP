
import logging

from Student import Student
from Subject import Subject
from Instructor import Instructor
from Classroom import Classroom
from FunctionsTime import TimeValue
from FunctionsTime import TimeToText
from SimulationExecute import Execute
from SimulationEdit import *
from FunctionsUtil import *
from Data import *

# AssignSubjectToTime: Search All Subjects by code
# Member Function of the Simulation
# Input
#   code: code of the subject
# Return
#   idx(list(int)): index of the subjects, empty list if don't exists
def AssignSubjectToTime(self, subInd, timeInd, timeMoment, classroom = "Anywhere", force = False):
    if len(self.subjects[subInd].timeIsAssigned) <= timeInd:
        logging.warn("time Index is not correct")
        return None
    if self.subjects[subInd].timeIsAssigned[timeInd] == True:
        logging.warn("time is already assigned to:%s"%str(self.subjects[subInd].timeAssignedTime[timeInd]))
        if force: logging.warn("Force Moving Time...")
        else:     return None
    self.subjects[subInd].timeIsAssigned[timeInd] = True
    self.subjects[subInd].timeAssignedTime[timeInd] = timeMoment
    if classroom == "Anywhere":
        logging.info("Assigning random Classroom if not empty...")
        if self.subjects[subInd].timeAssignedClassroom[timeInd] == "":
            self.subjects[subInd].timeAssignedClassroom[timeInd] = classroom
    # logging.info("time assigned to:%s"%str(self.subjects[subInd].timeAssignedTime[timeInd]))
    # self.Update()

def RemoveSubjectTime(self, subInd, timeInd):
    self.subjects[subInd].timeIsAssigned[timeInd] = False
    self.Update()

# SearchSubjectsByCode: Search All Subjects by code
# Member Function of the Simulation
# Input
#   code: code of the subject
# Return
#   idx(list(int)): index of the subjects, empty list if don't exists
def SearchSubjectsByCode(self, code):
    res = list()
    for sub in self.subjects:
        if sub.infoCode == code:
            res.append(sub.idx)
    return res

# SearchSubjectByCodeAndDivision: Search Subject by code and division
# Member Function of the Simulation
# Input
#   code: code of the subject
#   division: Division of the subject
# Return
#   idx(int): index of the subject, -1 if don't exists
def SearchSubjectByCodeAndDivision(self, code, division):
    for sub in self.subjects:
        if sub.infoDivision == division and sub.infoCode == code:
            return sub.idx
    return -1

# SearchStudentById: Search Student by infoId
# Member Function of the Simulation
# Input
#   code: Id of the student
# Return
#   idx(int): index of the student, -1 if don't exists
def SearchStudentById(self, id):
    for stu in self.students:
        if stu.infoId == id:
            return stu.idx
    return -1

# SearchInstructorByName: Search instructor by name
# Member Function of the Simulation
# Input
#   n: Name of the instructor
# Return
#   idx(int): index of the instructor, -1 if don't exists
def SearchInstructorByName(self, n):
    for inst in self.instructors:
        if inst.infoName == n:
            return inst.idx
    return -1

# LeftSubjects: Search instructor by name
# Member Function of the Simulation
# Return
#   idx(int): index of the instructor, -1 if don't exists
def LeftSubjects(self):
    res = []
    for sub in self.subjects:
        if sub.TimeIsAllAssigned() == False:
            res.append(sub)
    return res


# Update: Update students and instructors subjectAssign
# Member Function of the Simulation
#
#
def Update(self):
    for sub in self.subjects:
        if sub.TimeIsAllAssigned():
            for stu in self.students:
                if sub.idx in stu.subject1st:
                    if sub.idx in stu.subjectAssign:
                        continue
                    stu.subjectAssign.append(sub.idx)
            for ins in self.instructors:
                if sub.idx in ins.subjectEnroll:
                    if sub.idx in ins.subjectAssign:
                        continue
                    ins.subjectAssign.append(sub.idx)
        else:
            for stu in self.students:
                if sub.idx in stu.subjectAssign:
                    stu.subjectAssign.remove(sub.idx)
            for ins in self.instructors:
                if sub.idx in ins.subjectAssign:
                    ins.subjectAssign.remove(sub.idx)
    self.CheckCollide()

def FindSameSubject(self, sub):
    result=list()
    for subs in self.subjects:
        if CheckSameSubjectbyName(subs,sub):
            result.append(subs)
    return result

# CheckCollide: check collide student and instructor subject assign
# Member Function of the Simulation
#
def CheckCollide(self):
    for obj in self.students:
        set = obj.subjectColliding
        time_list1 = list()
        for co in set:
            if (self.subjects[co[0]].TimeIsAllAssigned() == False) or (self.subjects[co[1]].timeIsAssigned() == False):
                obj.subjectColliding.remove(co)
                continue
            for i in self.FindSameSubject(self.subjects[co[0]]):
                temp = list()
                if i.TimeIsAllAssigned():
                    for i2, time in enumerate(i.timeAssignedTime):
                        temp.append([i.timeAssignedSplit[i2], TimeValue(time), i.idx])
                    time_list1.append(temp)
            time_list2 = list()
            for i in self.FindSameSubject(self.subjects[co[1]]):
                temp = list()
                if i.TimeIsAllAssigned():
                    for i2, time in enumerate(i.timeAssignedTime):
                        temp.append([i.timeAssignedSplit[i2], TimeValue(time), i.idx])
                    time_list2.append(temp)
            for i in range(len(time_list1)):
                for i2 in range(len(time_list2)):
                    col = 0
                    for i3 in time_list1[i]:
                        for i4 in time_list2[i2]:
                            if i3[1] < i4[1]:
                                if i3[0] + i3[1] < i4[1]:
                                    col += 1
                            if i3[1] > i4[1]:
                                if i4[0] + i4[1] < i3[1]:
                                    col += 1
                    if col == len(time_list1) * len(time_list2) and col != 0:
                        obj.subjectColliding.remove(co)
                        break
                if col == len(time_list1) * len(time_list2) and col != 0:
                    break
        for a in range(len(obj.subjectAssign) - 1):
            sub = obj.subjectAssign[a]
            for b in range(a, len(obj.subjectAssign)):
                sub2 = obj.subjectAssign[b]
                if sub == sub2:
                    continue
                time_list1 = list()
                for i in self.FindSameSubject(self.subjects[sub]):
                    temp = list()
                    if i.TimeIsAllAssigned():
                        for i2, time in enumerate(i.timeAssignedTime):
                            temp.append([i.timeAssignedSplit[i2], TimeValue(time), i.idx])
                        time_list1.append(temp)
                time_list2 = list()
                for i in self.FindSameSubject(self.subjects[sub2]):
                    temp = list()
                    if i.TimeIsAllAssigned():
                        for i2, time in enumerate(i.timeAssignedTime):
                            temp.append([i.timeAssignedSplit[i2], TimeValue(time), i.idx])
                        time_list2.append(temp)
                col_c = 0
                for i in range(len(time_list1)):
                    for i2 in range(len(time_list2)):
                        col = False
                        for i3 in time_list1[i]:
                            for i4 in time_list2[i2]:
                                if i3[1] < i4[1]:
                                    if i3[0] + i3[1] > i4[1]:
                                        col = True
                                if i3[1] > i4[1]:
                                    if i4[0] + i4[1] > i3[1]:
                                        col = True
                            if col == True:
                                col_c += 1
                                break
                if col_c == len(time_list1) * len(time_list2) and col_c != 0:
                    if [self.subjects[sub].idx, self.subjects[sub2].idx] not in obj.subjectColliding:
                        obj.subjectColliding.append([self.subjects[sub].idx, self.subjects[sub2].idx])
    for ins in self.instructors:
        remove = True
        sub_start_time = list()
        for co in ins.subjectColliding:
            sub = co[0]
            sub2 = co[1]
            if (self.subjects[co[0]].TimeIsAllAssigned() == False) or (self.subjects[co[1]].TimeIsAllAssigned() == False):
                ins.subjectColliding.remove(co)
                continue
            for i, time in enumerate(self.subjects[co[0]].timeAssignedTime):
                sub_start_time.append(
                    [self.subjects[sub].timeAssignedSplit[i], TimeValue(time), self.subjects[sub].idx])
            for i, time in enumerate(self.subjects[co[1]].timeAssignedTime):
                sub_start_time.append(
                    [self.subjects[sub2].timeAssignedSplit[i], TimeValue(time), self.subjects[sub2].idx])
            sub_start_time.sort(key=lambda x: x[1])
            for i in range(len(sub_start_time) - 1):
                if sub_start_time[i + 1][1] < sub_start_time[i][0] + sub_start_time[i][1]:
                    remove = False
                    break
            if remove == True:
                ins.subjectColliding.remove(co)
        sub_start_time = list()
        for sub in ins.subjectAssign:
            for i, time in enumerate(self.subjects[sub].timeAssignedTime):
                sub_start_time.append(
                    [self.subjects[sub].timeAssignedSplit[i], TimeValue(time), self.subjects[sub].idx])
        sub_start_time.sort(key=lambda x: x[1])
        for i in range(len(sub_start_time) - 1):
            for i2 in range(i + 1, len(sub_start_time)):
                if sub_start_time[i2][1] < sub_start_time[i][0] + sub_start_time[i][1]:
                    if [sub_start_time[i][2], sub_start_time[i2][2]] not in ins.subjectColliding:
                        ins.subjectColliding.append([sub_start_time[i][2], sub_start_time[i2][2]])
                else:
                    break

import pickle
# Save: Save ttsave to file
# Member Function of the Simulation
# Input
#   dir(str): save file directory
def Save(self, dir="save.ttsave"):
    sf = open(dir,'wb')
    pickle.dump(self, sf)
    sf.close()
    logging.info("Save simulation to %s"%dir)

import csv
def SaveCSV(self, dirr="tt.csv"):
    f = open(dirr, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    for sub in self.subjects:
        if len(sub.timeAssignedTime) < 1:
            continue
        print(sub.infoName, sub.timeAssignedTime, sub.timeAssignedSplit)
        tt = []
        for ind ,t in enumerate(sub.timeAssignedTime):
            tt.append(TimeToText((t[0],t[1],t[2],sub.timeAssignedSplit[ind])))
        wr.writerow([sub.idx, sub.infoCode, sub.infoName, sub.infoDivision,tt])
    f.close()
    logging.info("Saved csv parsed data to %s"%dirr)
    

# Load: Load ttsave from file
# Member Function of the Simulation
# Input
#   dir(str): save file directory
def Load(self, dir="save.ttsave"):
    try:
        sf = open(dir,'rb')
        s = pickle.load(sf)
        self.students = s.students
        self.subjects = s.subjects
        self.instructors = s.instructors
        self.classrooms = s.classrooms
        self.config = s.config
        sf.close()
        logging.info("Load simulation to %s"%dir)
        self.Update()
        return 0
    except:
        return -1


def Export(self):
    # Export to csv
    pass

def SearchNotAssignedSubjects(self):
    lst = []
    for s in self.subjects:
        if self.mode == "exam":
            if s.timeIsAssigned == False:
                lst.append(s)
        else:
            if s.TimeIsAllAssigned() == False:
                lst.append(s)
    return lst


def PrintSubject(s):
    print()
    print("Subject (%s-%d) %s"%(s.infoCode, s.infoDivision, s.infoName))
    print("  Exam : %s / Lecture : %s"%(s.examOn, s.examLectureOnExam))
    print("  Lecture Time %s"%(str(s.examAssignedLectureTime)))
    if s.timeIsAssigned:
        print("  Exam Time %s"%(str(s.timeAssignedTime)))
    else:
        print("  Exam Time not determined")
    if len(s.timePrefer) >= 1:
        print("  Exam prefer time"%(str(s.timePrefer)))
    if len(s.examDivisionUniteList) >= 1:
        print("  Division Unite? "%(str(s.examDivsionUniteList)))

def CUI(self):
    loop = True
    print("Timetable Simualtor v0.1")
    while(loop):
        print("\n"*5)
        print("Current status")
        if self.mode == "exam":
            print("Mode : Exam")
        else:
            print("Mode : Timetable")
        print("# of Subjects    : %4d (Colliding) / %4d (Left) / %4d (Total)"%(-1,len(self.SearchNotAssignedSubjects()),len(self.subjects)))
        print("# of Students    : %4d (Colliding) / %4d (Left) / %4d (Total)"%(-1,-1,len(self.students)))
        print("# of Instructors : %4d (Colliding) / %4d (Left) / %4d (Total)"%(-1,-1,len(self.instructors)))
        print("# of classrooms  : %4d"%len(self.classrooms))
        print(" >> ",end="")
        inp = input().split(" ")
        if   inp[0].lower() in ["xx", "exit"]:
            break
        elif inp[0].lower() in ["l", "load"]:
            if self.mode == "exam":
                if len(inp) <= 2: print("Argument Wrong: load save/subjects/students [directory]")
                elif inp[1] == "save":
                    res = self.Load(inp[2])
                    if res == 0: print("Successly Loaded state from %s"%inp[2])
                    else: print("Loaded state from %s Failed"%inp[2])
                elif inp[1] == "subjects":
                    res = self.LoadExamSubjects(inp[2])
                    if res == 0: print("Successly Loaded Subjects from %s"%inp[2])
                    else: print("Loaded Subjects from %s Failed"%inp[2])
                elif inp[1] == "students":
                    res = self.LoadExamStudents(inp[2])
                    if res == 0: print("Successly Loaded Students from %s"%inp[2])
                    else: print("Loaded Students from %s Failed"%inp[2])
        elif inp[0].lower() in ["x", "execute"]:
            self.Execute()
        elif inp[0].lower() in ["c", "create"]:
            print("Creating")
        elif inp[0].lower() in ["e", "edit"]:
            print("Edit")
        elif inp[0].lower() in ["d", "delete"]:
            print("Delete")
        elif inp[0].lower() in ["cx", "collide"]:
            print("Check collide")
            print(self.CheckCollide())
        elif inp[0].lower() in ["s", "save"]:
            if len(inp) == 1:
                self.Save("save.ttsave")
                print("Saved state to save.ttsave")
            else:
                self.Save(inp[1])
                print("Saved state to %s"%inp[1])
        elif inp[0].lower() in ["sc","savecsv"]:
            if len(inp) == 1:
                self.SaveCSV("tt.csv")
                print("Saved state to tt.csv")
            else:
                self.SaveCSV(inp[1])
                print("Saved state to %s"%inp[1])

        elif inp[0].lower() in ["sub", "subject"]:
            if len(inp) == 1:
                print("Argument Wrong: subject [idx]")
            else:
                PrintSubject(self.subjects[int(inp[1])])
        elif inp[0].lower() in ["t", "setting"]:
            if len(inp) == 1: print("Argument Wrong: setting change [setting name] [value]")
            elif inp[1] == "change":
                cng = False
                if len(inp) == 2: print("Argument Wrong: setting change [setting name] [value]")
                elif inp[2] == "mode":
                    cng = True
                    self.mode = inp[3]
                
                if cng: print("Setting [%s] Changed to [%s]"%(inp[2],inp[3]))
                else: print("Setting didn't changed")

        print("\nPress enter to Proceed\n >> ",end="")
        input()
        

class Simulation:
    def __init__(self, config = None):
        self.students = list()
        self.subjects = list()
        self.instructors = list()
        self.classrooms = list()
        self.mode = "exam"
        if config == None:
            logging.info("Simulation Initiated with empty status")
        else:
            self.config = config
            logging.info("Simulation Initiated with config value")

    AddStudent = AddStudent
    AddSubject = AddSubject
    AddInstructor = AddInstructor
    AddClassroom = AddClassroom
    AssignSubjectToTime = AssignSubjectToTime
    CheckCollide = CheckCollide
    Execute = Execute
    Export = Export
    FindSameSubject = FindSameSubject
    LeftSubjects = LeftSubjects
    Load = Load
    LoadExamStudents = LoadExamStudents
    LoadExamSubjects = LoadExamSubjects
    RemoveSubjectTime = RemoveSubjectTime
    Save = Save
    SaveCSV = SaveCSV
    SearchStudentById = SearchStudentById
    SearchSubjectsByCode = SearchSubjectsByCode
    SearchSubjectByCodeAndDivision = SearchSubjectByCodeAndDivision
    SearchInstructorByName = SearchInstructorByName
    SearchNotAssignedSubjects = SearchNotAssignedSubjects
    Update = Update
    CUI = CUI
    
