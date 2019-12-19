
import Util

from Student import Student
from Subject import Subject

from ScoreVar import *
from ScoreUtil import *
from ScorePrint import *

# Assign subject(ind) to t, which is tuple
def AssignSubject(inputInd, t,gapFront=1,gapBack=1):
    if type(t[0]) == int or t[0] in ["0","1","2","3","4","5","6"]:
        t = (int(t[0]),int(t[1]))
    else:
        try:
            t = Util.TimeStrToTuple(t[0]+"-"+t[1])
        except:
            print("Input Command Error")
            return None
    
    if subjects[inputInd].isTimeSet == True:
        print("Subject is already Set to "+str(subjects[inputInd].timeExam))
        return None
    curAttend = subjects[inputInd].studentAttend
    # iterating through subject
    for subInd, sub in enumerate(subjects):
        # Doesn't checking taking class
        if subjects[subInd].isExam == False:
            continue
        # check attending student in each class
        for stu in sub.studentAttend:
            # if it is on current class,
            if stu in curAttend and inputInd not in subjectUnavail[subInd][t]:
                # Add Unavailibility
                for it in range(subjects[inputInd].examLength+gapFront+gapBack):
                    tv = max(min(t[1]+it-gapFront,47),0)
                    subjectUnavail[subInd][(t[0], tv)].append(inputInd)
                # print("Updated Subject " + str(subjects[subInd].codeIndex) + " "+subjects[subInd].name +" @ " + str(t) + "~" + str((t[0],t[1]+subjects[inputInd].examLength-1)))
                # PrintUnavail(subjectUnavail[subInd])
    for it in range(subjects[inputInd].examLength):
        # subjects[inputInd].time.append((t[0],t[1]+it))
        subjects[inputInd].timeExam.append((t[0],t[1]+it))
    subjects[inputInd].isTimeSet = True
    print("Assigned (" +str(subjects[inputInd].codeIndex) + "):" + subjects[inputInd].name + " to " + Util.TimeTupleListToHumanStr(subjects[inputInd].timeExam))

# Pop subject from assigned time
def PopSubject(inputInd):
    # Halt if subject is not taking exam
    if subjects[inputInd].isExam == False:
        print("Subject not taking Exam")
        return None
    # Half if subject's exam time is not set
    elif subjects[inputInd].isTimeSet == False:
        print("Subject's Exam time is not set")
        return None
    # Updating subjectUnavail table
    for i in subjectUnavail:
        for k in i.items():
            if inputInd in k:
                k.remove(inputInd)
    # Set subject's exam time to empty list and update status
    subjects[inputInd].timeExam = list()
    subjects[inputInd].isTimeSet = False
    print("Poped ("+str(subjects[inputInd].codeIndex)+"): " +subjects[inputInd].name)

# Force Move subject using existing function
def MoveSubject(i, j):
    # Basically pop and assign subject
    PopSubject(i)
    AssignSubject(i,j)

# AssignSubjectToRecomTime
# Returns subject id if it put subject to some random time
def AssignSubjectToRecomTime(sind, gapFront=0, gapBack=0):
    # Get recommended time for input subject
    loc = GetRecomTime(sind,gapFront=gapFront,gapBack=gapBack)
    # if there is no recommended time, print subject's subjectValue and subjectUnavail and do nothing
    if loc==(-1,-1):
        print(str(sind) + " " + subjects[sind].name + " Couldn't Assigned")
        PrintTimeValue(subjectValue[sind])
        PrintUnavail(subjectUnavail[sind])
        return -1
    # Else, assign subject to given position
    AssignSubject(sind, loc, gapFront=gapFront,gapBack=gapBack)
    return 0

def Execute():
    # Main Assigning algorithm
    print(GetStrAwesome("Assigning Time"))
    # Manual alias, need to be edited better
    alias = ["SE206", "SE211"] # Manual alias table, if there are more alias table, it needed to be edited better
    # Merging divisions
    for s in subjects:
        if len(s.divisionUnite) > 1 and s.isExam == True:
            # print("Check division:"+s.name+" "+str(s.division)+ str( s.divisionUnite))
            # division printing method need to be resolved. Advanced-1 is not Normal-3
            dl = []
            for m in subjects:
                # Alias, improvement needed
                if s.codeSchool[0:5] in alias and m.codeSchool[0:5] in alias:
                    dl.append(m.codeIndex); continue
                # rest normal cases
                if s.codeSchool[0:5] != m.codeSchool[0:5]: continue
                # if m.division not in s.divisionUnite: continue
                dl.append(m.codeIndex)
            for i in dl[1:]:
                subjects[i].isExam = False
                for stu in subjects[i].studentAttend:
                    subjects[dl[0]].studentAttend.append(stu)
                subjects[i].divisionUnite = dl
            subjects[dl[0]].divisionUnite = dl
            # print(subjects[dl[0]].studentAttend)
        else:
            s.divisionUnite = list()
    
    unaForce = list()
    
    # Assign subjects to timetable
    # Set subject with time is fixed: This should put because they have to put in
    print("Assigning Subjects with Time Fixed")
    for sind, s in enumerate(subjects):
        if s.isFixed == True:
            # Update subjectValue to fixed time
            for d in range(TIME_DAY):
                for t in range(TIME_UNIT):
                    if (d, t) not in s.fixedTime:
                        subjectValue[sind][(d,t)] = 0
            # Assign subject to time if it is not assigned
            if subjects[sind].isTimeSet == False:
                if AssignSubjectToRecomTime(sind, 0, 0)==-1:
                    unaForce.append(sind)
    
    unaFree = list()
    # Assign rest subjects from biggest subject
    print("Assigning Other Subjects")
    while len(GetUnsetSubjects(subjects)) > len(unaFree) + len(unaForce):
        sind = GetMaxStudentsIndex(subjects, unaFree+unaForce)
        if subjects[sind].isFixed == False:
            if AssignSubjectToRecomTime(sind, 1, 0)==-1:
                unaFree.append(sind)
    
    # Print unassigned subjects"
    print(GetStrAwesome("Unavailable Subjects"))
    if len(unaForce)>0:
        print("Force - This is serious problem")
        for i in unaForce:
            print(str(i)+" "+subjects[i].name)
    if len(unaFree)>0:
        print("Free - Meh...")
        for i in unaFree:
            print(str(i)+" "+subjects[i].name)
