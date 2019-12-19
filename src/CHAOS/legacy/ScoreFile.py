import sys
import pickle

import DataWrite
import DataLoad
import Util

from Student import Student
from Subject import Subject

from ScoreUtil import *
from ScoreVar import *

# Save timetable to csv file
def SaveTimetable(loc = ""):
    timeStr = Util.GetCurrentTimeStr()
    if loc == "":
        loc = "Timetable_"+timeStr+".csv"
    print("Writing to {:s}...".format(loc))
    DataWrite.TimetableToCsv(subjects, loc, mode = "Exam")
    print("Saving Complete! Timetable saved at "+loc)

# Save working data
def SaveData(loc = "save"):
    # Not working properly
    f = open(loc + ".data", "wb")
    for i in subjects:
        pickle.dump(i, f)
    print("Saved {:d} subject data to {:s}".format(len(subjects), loc + ".data"))

# Load working data
def LoadData(loc = "save"):
    # Not working properly
    f = open(loc + ".data", "rb")
    global subjects # Define needs to be used as global
    subjects = list()
    print("Emptied Subject data",subjects)
    while True:
        try: line = pickle.load(f)
        except EOFError: break
        subjects.append(line)
    print("Loaded {:d} subject data from {:s}".format(len(subjects), loc + ".data"))

# Load initial data
def DataInit():
    # Data loading
    print(GetStrAwesome("Step 1: Loading data"))
    locStudentEnroll = "../data/19SpringStudentEnroll_hash.csv"
    # locTestSurvey = "../data/19SpringMidExamSurvey.csv"
    locTestSurvey = "../data/19SpringFinalExamSurvey.csv"
    # Loading course data with student enrollment data
    try:
    # if True:
        print("Reading course data from " + locStudentEnroll)
        tmpData = DataLoad.FromCsvFile(locStudentEnroll, [])
    except:
        print("FATAL ERROR: Course data load failed..!"); sys.exit()
    subjectIds = list() # id of subjects to check overlap
    for index, line in enumerate(tmpData):
        # temp code format : "SE101 1" [codeSchool] [Division]
        tmpCode = line[0] + " " + line[2]
        # If subject is not on the list, add subject
        if tmpCode not in subjectIds:
            subjectIds.append(tmpCode)
            t = Subject(len(subjectIds)-1, "Exam")
            # set Basic subject information
            if  (line[0][2]=="1"): t.targetGrade = 1
            elif(line[0][2]=="2"): t.targetGrade = 2
            elif(line[0][2]=="3"): t.targetGrade = 3
            else                 : t.targetGrade = 4
            t.codeSchool = line[0]
            t.name = line[1]
            t.division = int(line[2])
            t.instructor = line[3].split(",")
            t.time = list()
            t.timeLecture = list()
            t.timeExam = list()
            t.studentAttend = list()
            # Add lecture time and location
            for TimeStrInd in line[4].split(","):
                t.locationStr = Util.DgistStrToClassroomStrList(TimeStrInd)
                timeStrTmp = Util.DgistStrToTimeStrList(TimeStrInd)
                for ind,val in enumerate(timeStrTmp):
                    timeStrTmp[ind] = Util.TimeStrToTuple(val)
                t.AddTimeLectures(timeStrTmp)
            subjects.append(t)
        # Add Student to class, we need to do something with line...
        subjects[subjectIds.index(tmpCode)].AddStudent(int(line[len(line)-1]))
    print("Processed " + str(index+1) + " enrollment data")
    print("Created " + str(len(subjectIds)) + " subjects")
    # Loading survey data
    # try:
    if True:
        print("Reading survey data from "+locTestSurvey)
        tmpData = DataLoad.FromCsvFile(locTestSurvey,[0])
    # except:
        # print("FATAL ERROR: Survey data load failed..!"); sys.exit()

    for index, line in enumerate(tmpData):
        # Find the index of the course
        try:
            i = subjectIds.index(line[0] + " " + str(line[2]))
        except:
            print("Subject not exists!")
            continue
        # Applying data
        subjects[i].isExam = Util.XOToBool(line[7])
        if subjects[i].isExam:
            if line[8] == None or line[8] == "": line[8] = 0;
            subjects[i].examLength = int(line[8])//30
            if subjects[i].examLength == 0:
                subjects[i].examLength = 3
            subjects[i].isExamOnLecture = Util.XOToBool(line[9])
            if subjects[i].isExamOnLecture: # Check survey stuffs
                tfT = [Util.XOToBool(line[10]), Util.XOToBool(line[11]), Util.XOToBool(line[12])]
                if not (tfT[0]^tfT[1]):
                    subjects[i].isFixed = True
                    subjects[i].fixedTime = subjects[i].timeLecture
                elif tfT[0]: #is there any elegant way?
                    subjects[i].isFixed = True
                    subjects[i].fixedTime = subjects[i].timeLecture[0:3]
                else:
                    subjects[i].isFixed = True
                    subjects[i].fixedTime = subjects[i].timeLecture[3:]
            if Util.XOToBool(line[13]):
                # Need One More Option
                subjects[i].isFixed = True
                subjects[i].fixedTime = subjects[i].timeLecture
            # Add Desired Time
            # subjects[i].isFixed = False
            # Unite Division - need more work
            subjects[i].divisionUnite = line[15].split(",")
            subjects[i].divisionClassroom = line[16].split("/")
            if len(line[19])>0:
                subjects[i].isFixed = True
                subjects[i].fixedTime = Util.LimitStrToTupleList(line[19])
            if len(line[20])>0:
                subjects[i].desiredTime = Util.LimitStrToTupleList(line[20])
        # if lecture on exam
        subjects[i].isLectureOnExam = Util.XOToBool(line[17])
        subjects[i].lectureOnExamIndex = line[18].split(",")
    print("Processed " + str(index+1) + " Survey data")
    for sind, s in enumerate(subjects):
        for i in s.studentAttend:
            if i not in studentsId:
                mys = Student(i,1)
                mys.subjectEnrolled.append(sind)
                studentsId.append(i)
                students.append(mys)
            else:
                if sind not in students[studentsId.index(i)].subjectEnrolled:
                    students[studentsId.index(i)].subjectEnrolled.append(sind)
    print("Assigned Students to Subjects")
    # Add time values
    for s in subjects:
        subjectValue.append(InitTimeValue(s))
        subjectUnavail.append(InitUnavail())


