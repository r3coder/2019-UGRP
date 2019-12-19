
import logging

import pprint
pp = pprint.PrettyPrinter(indent=1)

from FunctionsTime import *
from datetime import datetime
import random

class Slot:
    def __init__(self, mode, ty, days, time):
        self.type = ty
        self.time = []
        for day in days:
            if mode == "simple":
                for t in time:
                    l =[]
                    if type(day)==int: l.append((day, t[0],t[1]))
                    else:
                        for i in day: l.append((i, t[0],t[1]))
                    self.time.append(l)
            elif mode == "SP01":
                for t0 in time:
                    self.time.append([(day[0],t0[0],t0[1]),(day[1],t0[0],t0[1]),(3,12,30)])
            elif mode == "SP02":
                for t0 in time:
                    self.time.append([(day[0],t0[0],t0[1]),(day[1],t0[0],t0[1]),(3,16,0)])
        logging.info("Slot %s Length: %d"%(str(self.type),len(self.time)))

def EditChaos(sub, time, val):
    t = time[0]*48+time[1]*2
    if time[2] == 30: t += 1
    sub.timeChaos[t] += val

def EditChaosA(sub, time, val):
    t = time[0]*48+time[1]*2
    if time[2] == 30: t += 1
    sub.timeChaosA[t] = val

def EditChaosDuration(sub, time, dur, val):
    t = time[0]*48+time[1]*2
    if time[2] == 30: t += 1
    for i in range(t, t+dur//30):
        sub.timeChaos[i] += val


CHAOS_MAX = 999
CHAOS_STUDENT = 7
CHAOS_SUBJECT = 150

def TryAddSubject(s, sub, time, chaosTable):
    chaosTableN = []
    for elem in chaosTable:
        chaosTableN.append(elem[:])

    for i, e in enumerate(sub.subInstructors):
        if e==0: continue
        for tt in time:
            chaosTableN[i][TimeIndex(tt)] = -1
    """
    for indss, ss in enumerate(s.subjects):
        for tt in time:
            if chaosTableN[indss][TimeIndex(tt)] == -1: continue
            chaosTableN[indss][TimeIndex(tt)] += CHAOS_SUBJECT
    """
    for i, e in enumerate(sub.subStudents):
        if e==0: continue
        for tt in time:
            if chaosTableN[i][TimeIndex(tt)] == -1: continue
            chaosTableN[i][TimeIndex(tt)] += CHAOS_STUDENT*e
    v = CalculateChaos(chaosTableN)
    return v
    

def CalculateChaos(chaosTable): # Change calculating method... plz plz!!!!!
    sum = 0.0
    for sub in chaosTable:
        sum2 = 0.0
        for iv, v in enumerate(sub):
            if iv%48<18 or iv%48>44: continue
            if v != -1: sum2 += v/1000
            else:       sum2 += 1
        sum += sum2 / (5*(48-21))
    return sum

def PrintChaos(chaosTable, len=3, div = 12):
    day = ["월", "화", "수", "목", "금"]
    s = ""
    for ind, val in enumerate(chaosTable):
        s+="\n"
        for ind1,val1 in enumerate(val):
            s+="%3d"%val1
            if ind1%div == div -1: s+=" "
            if ind1%48 == 47: s+="\n"
        s+="\n"
    print(s)


def TimeIndex(t):
    return t[0]*48+t[1]*2+t[2]//30

def TimeIntList(td):
    res = []
    s = TimeIndex(td); e=TimeIndex(td)+td[3]//30
    return range(s,e)

# Execute: Executing Simulation
# Input
#   arguments(dict) simulation presets
def Execute(self, args=dict()):
    logging.info("Simulation Executed")
    timeStart = datetime.now()
    chaosTable = []
    chaosTableSlot = []
    for sub in self.subjects:
        chaosTable.append([0]*5*48)
        if sub.TimeType() == 0:
            chaosTableSlot.append([])
            sub.slotLen = -1
        else:
            chaosTableSlot.append([0]*len(self.config.SIM_SLOTS[sub.TimeType()].time))
            sub.slotLen = len(self.config.SIM_SLOTS[sub.TimeType()].time)
        sub.subStudents = [0]*len(self.subjects)
        sub.subInstructors = [0]*len(self.subjects)

    for inst in self.instructors:
        for i in inst.subjectEnroll:
            self.subjects[i].subInstructors[inst.idx] += 1
    for stu in self.students:
        for i in stu.subject1st:
            self.subjects[i].subStudents[stu.idx]+= 1

    # Basic time limitation
    for ind, sub in enumerate(self.subjects):
        for day in range(0, 5):
            for time in range(0, 48):
                if time<18 or time>45: chaosTable[ind][day*48+time] = -1
        if sub.TimeIsAllFixed():
            # logging.info("Appending Chaos to infoName:%s"%sub.infoName)
            for t in TimeListReversed(sub.timeAssignedTime, sub.timeAssignedSplit):
                chaosTable[ind][TimeIndex(t)] = -1
        
        for tt in sub.timeExclude:
            for t in TimeIntList(tt):
                chaosTable[ind][t] = -1
        for inst in sub.infoInstructor:
            for tt in self.instructors[inst].timeImpossible:
                for t in TimeIntList(tt):
                    chaosTable[ind][t] = -1
    logging.info("Set CHAOS for fixed subjects...")    
    logging.info("Set CHAOS using Subject Exclude time")    
    logging.info("Set CHAOS using Instructor Exclude time")
    # PrintChaos(chaosTable)
    
    timeLast = datetime.now()
    logging.info("Simulation Ready! Elapsed: %s"%str(datetime.now() - timeStart))
    # Simulation Begins...
    epoch=0
    while len(self.LeftSubjects()) > 0:
        epoch+=1
        chaosOrig = CalculateChaos(chaosTable)
        for indsub, sub in enumerate(self.subjects): #GPU Friendily code...
            if sub.TimeIsAllAssigned(): continue
            print(sub.infoName)
            isSubjectPlaceable = False
            for indslot, slot in enumerate(self.config.SIM_SLOTS[sub.TimeType()].time):
                possible = True
                loopBreaker = False
                for ttind, tt in enumerate(slot):
                    for t in TimeIntList((tt[0],tt[1],tt[2],self.config.SIM_SLOTS[sub.TimeType()].type[ttind])):
                        if chaosTable[indsub][t] == -1:
                            possible = False; loopBreaker = True; break
                        if self.subjects[indsub].command:
                            if len(self.subjects[indsub].commandSubSame)> 0: # Same command
                                for ssind in self.subjects[indsub].commandSubSame:
                                    for i in self.subjects:
                                        if i.commandIdx == ssind: realInd = i.idx; break
                                    if chaosTable[realInd][t] == -1:
                                        possible = False; loopBreaker = True; break
                            if len(self.subjects[indsub].commandSubDiffDay) > 0:
                                pass # Maybe broke my code..
                        if loopBreaker: break
                    if loopBreaker: break
                    # If every cell is impossible, I shoulda handle that...
                if possible:
                    chaosTableSlot[indsub][indslot] = TryAddSubject(self, sub, slot,chaosTable) - chaosOrig
                    isSubjectPlaceable = True
                else:
                    chaosTableSlot[indsub][indslot] = self.config.SIM_SLOT_MAX
            if isSubjectPlaceable == False:
                logging.warn("This subject is unable to place...: [%d]:%s"%(indsub,str(sub.infoName)))

        # Get the highest
        cHighVal = 0
        cHighList = []
        for ind, cts in enumerate(chaosTableSlot):
            if self.subjects[ind].TimeIsAllAssigned(): continue
            totalC = 0
            for i in cts: totalC += i
            totalC /= len(cts)
            if totalC >= self.config.SIM_SLOT_MAX: totalC = self.config.SIM_SLOT_MAX
            if totalC  > cHighVal: cHighVal = totalC; cHighList = []
            if totalC == cHighVal: cHighList.append(ind)
        random.shuffle(cHighList) # Method 2. Put One at one time
        putInd = cHighList[0]
        # Finding index 
        minChaosInd = [0]
        minChaosVal = chaosTableSlot[putInd][0]
        for ind, val in enumerate(chaosTableSlot[putInd]):
            if val  < minChaosVal: minChaosVal = val; minChaosInd = []
            if val == minChaosVal: minChaosInd.append(ind)
        random.shuffle(minChaosInd)
        # And finally assigning
        for ind, val in enumerate(self.config.SIM_SLOTS[self.subjects[putInd].TimeType()].time[minChaosInd[0]]):
            self.AssignSubjectToTime(putInd, ind, val, force=True)
            if self.subjects[putInd].command:
                if len(self.subjects[putInd].commandSubSame)> 0: # Same command
                    for ssind in self.subjects[putInd].commandSubSame:
                        for i in self.subjects:
                            if i.commandIdx == ssind: realInd = i.idx; break
                        self.AssignSubjectToTime(realInd, ind, val, force=True)
            # How about fail assigning subject to the time -> more epoch, more accurate? -> shouldn't it could be infinite loop?

        logging.info("*"*60)
        logging.info("Epoch %d Time: %s / %s"%(epoch, str(datetime.now() - timeLast), str(datetime.now() - timeStart)))
        timeLast = datetime.now()
        logging.info("Assigned [%d]%s-%d:%s to %s"%
                (self.subjects[putInd].idx, self.subjects[putInd].infoCode, self.subjects[putInd].infoDivision, self.subjects[putInd].infoName,self.subjects[putInd].TimeAssignedString()))
        logging.info("Left Subjects:%d / %d "%(len(self.LeftSubjects()), len(self.subjects)))
        s = ""
        for i in chaosTableSlot[putInd]:
            if i==-1: s += "XXXXXX "
            else: s += "%1.4f "%i
        logging.info("CHAOS Slot VALUE: %s"%s)

        if epoch%self.config.SIM_SAVE_DURATION==0:
            logging.info("Saving Checkpoint")
            self.SaveCSV("checkpoint_%d.csv"%epoch)
        
    self.Save()
    self.SaveCSV()
    self.Update() # <- this is problem...
    logging.info("Simulation Complete! Time: %s"%(str(datetime.now() - timeStart)))
    return 0