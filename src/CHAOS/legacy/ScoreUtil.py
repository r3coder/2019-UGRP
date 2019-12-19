

from ScoreVar import *


# Get list of time except input
def GetTimeListExcept(l):
    lst = []
    for day in range(TIME_DAY):
        for t in range(TIME_UNIT):
            if(day,t) not in l:
                lst.append((day,t))
    return lst

# Initialize Basic Time value using basic information table
def InitTimeValue(s):
    res=dict()
    for day in range(TIME_DAY):
        for t in range(TIME_UNIT):
            res[(day,t)] = VALUE_DAY[t]*VALUE_WEEK[day]/10000
    # appling subject data
    return res

# Initialize unavailability for each table
def InitUnavail():
    res=dict()
    for day in range(TIME_DAY):
        for t in range(TIME_UNIT):
            res[(day,t)] = []
    return res

# Get list of subjects that time is not set
def GetUnsetSubjects(subjects):
    res = []
    for ind, val in enumerate(subjects):
        if not val.isTimeSet and val.isExam:
            res.append(ind)
    return res

# Get index of subject that has maximum students
def GetMaxStudentsIndex(subjects, expt):
    mx = 0; res = -1
    for ind, val in enumerate(subjects):
        if ind in expt: continue
        if not val.isTimeSet and val.isExam:
            if mx < len(val.studentAttend):
                mx = len(val.studentAttend)
                res = ind
    return res

# Get recommended time for subject(ind)
def GetRecomTime(ind,gapFront=1,gapBack=1):
    loc = (-1, -1)
    ttVal = 0
    curTT = dict()
    for day in range(TIME_DAY):
        for t in range(TIME_UNIT-subjects[ind].examLength):
            flag = False
            for i in range(subjects[ind].examLength+gapFront+gapBack):
                tv = max(min(t+i-gapFront,47),0)
                if len(subjectUnavail[ind][(day, tv)])>0 or subjectValue[ind][(day, tv)] == 0:
                    flag = True; break
            if flag: continue
            if ttVal < subjectValue[ind][(day, t)]:
                loc = (day, t)
                ttVal = subjectValue[ind][(day, t)]
    return loc

# Get AWESOME STRING
def GetStrAwesome(s, w=60, e=1):
    return "\n"+"-"*w+"\n"*e+" "*(w//2-len(s)//2)+s+"\n"*e+"-"*w
