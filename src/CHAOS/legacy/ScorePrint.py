
import Exam
import Util
from ScoreVar import *
from ScoreUtil import *

# Print Unavaility of timetable. Use on subjectUnavail
def PrintUnavail(d, gap=6, l=1):
    print(GetUnavailStr(d,gap,l))
def GetUnavailStr(d, gap=6,l=1):
    res = ""
    for day in range(TIME_DAY):
        res += Util.week[day]+" "
        for t in range(TIME_UNIT):
            if(t%gap==0): res+= " "
            if len(d[(day,t)])==0: res += "-"
            elif len(d[(day,t)])<10: res += "%1d"%(len(d[(day,t)]))
            else: res+="+"
        res+="\n"
    return res

# Print Time value for subjectValue
def PrintTimeValue(d, gap=6, l=1):
    print(GetTimeValueStr(d,gap,l))
def GetTimeValueStr(d, gap=6, l=1):
    res = ""
    for day in range(TIME_DAY):
        res += Util.week[day] + " "
        for t in range(TIME_UNIT):
            if(t%gap==0): res += " "
            if(d[(day,t)]==1.0): res += "@"*l
            elif(d[(day,t)]==0.0): res+="-"*l
            else:
                if  (l==1): res += "{:1d}".format(int(d[(day,t)]*10  ))
                elif(l==2): res += "{:2d}".format(int(d[(day,t)]*100 ))
                elif(l==3): res += "{:3d}".format(int(d[(day,t)]*1000))
        res += "\n"
    return res
# Print students with certain options
def PrintStudents(msg):
    try:
        if msg[0]=="all": # Print All students
            for stu in students: stu.PrintExamTimetable(subjects,mode=0)
        elif msg[0]=="ideal": # Print Students with not ideal tt
            ide = Exam.IdealCheck(students,subjects,minGap=int(msg[1]),maxExam=int(msg[2]))
            for stu in ide: students[studentsId.index(stu)].PrintExamTimetable(subjects,mode=0)
            print("Students with minor problems("+str(len(ide))+"):"+str(ide))
        elif msg[0]=="subs": # Print Students with same subjects
            for stu in students:
                isOK = True
                for i in msg[1:]:
                    if int(i) not in stu.subjectEnrolled:
                        isOK = False
                        break
                if isOK:
                    stu.PrintExamTimetable(subjects,mode=0)

        elif ":" in msg[0]: # Print students from first until second
            ran = msg[0].split(":")
            for stu in students[int(ran[0]):int(ran[1])]: stu.PrintExamTimetable(subjects,mode=0)
        else: # Print students
            for stu in msg[0:]: students[int(stu)].PrintExamTimetable(subjects,mode=0)
    except:
        print(GetStrAwesome("HALT: Command Couldn't understand"))

# Print single subject
def PrintSubject(s):
    print(GetSubjectInfoStr(s))

def GetSubjectInfoStr(s):
    res = ""
    res+=GetStrAwesome(str(s.codeIndex)+" "+s.name+" ("+s.codeSchool+"-"+str(s.division)+")")
    res+="\n"
    res+="This subject...\n"
    if s.isExam: res+="  Takes exam on exam week\n"
    if s.isExamOnLecture: res+="  Takes exam on lecture time\n"
    if s.isLectureOnExam: res+="  Do lecture on Exam week\n"
    if len(s.divisionClassroom)>0: res+="  Divisions should be united as" + str(s.divisionClassroom) + "\n"
    if s.isFixed: res+="  Exam should on @ " + Util.TimeTupleListToHumanStr(s.fixedTime) + "\n"
    if len(s.desiredTime)>0: res+="  Exam may on @ " + Util.TimeTupleListToHumanStr(s.desiredTime) + "\n"
    res +="\n"
    if s.isExam:
        res+="Time Value\n"
        res+=GetTimeValueStr(subjectValue[s.codeIndex])
        res+="Unavaility\n"
        res+=GetUnavailStr(subjectUnavail[s.codeIndex])
        res+="\n"
    if s.isTimeSet: res+="Assigned timeExam: "+Util.TimeTupleListToHumanStr(s.timeExam)+"\n"
    else: res+="timeExam isn't assigned yet\n"
    res+="Note: "+s.memo+"\n"
    res+="\n"
    res+="Attending Students: "+str(s.studentAttend)+"\n"
    res+="Connected Subjects that has exam\n"
    for subs in subjects:
        if subs.codeIndex == s.codeIndex: continue
        if not subs.isExam: continue
        sind = list()
        for stu in s.studentAttend:
            if stu in subs.studentAttend:
                sind.append(stu)
        if len(sind)>0:
            res+="  "+str(subs.codeIndex).zfill(3)+" "+subs.name+"-"+str(subs.division)+" @ "+ Util.TimeTupleListToHumanStr(subs.timeExam) + " = ("+str(len(sind))+") " + str(sind) + "\n"
    return res


# Print Subjects with given options
def PrintSubjects(msg):
    if msg[0] in ["all", "a"]: # Print all subjects
        for sub in subjects: PrintSubject(sub)
    elif msg[0] in ["exam", "e"]: # Print subjects with exam
        for sub in subjects:
            if sub.isExam: PrintSubject(sub)
    elif ":" in msg[0]: # Print subject from first, until second
        ran = msg[0].split(":")
        for sub in subjects[int(ran[0]):int(ran[1])]: PrintSubject(sub)
    elif msg[0] in ["listexam","le"]: # Print subject list with exam
        for sub in subjects:
            if sub.isExam:
                print("{:3d} {:s}  ".format(sub.codeIndex,sub.name),end="") 
                if sub.isTimeSet: print(Util.TimeTupleListToHumanStr(sub.timeExam))
                else: print("Not Assigned")
    elif msg[0] in ["listall", "la"]: # Print subject list all
        for sub in subjects:
            print("{:3d} {:s}  ".format(sub.codeIndex,sub.name),end="")
            if not sub.isExam: print("Not Taking Exam")
            else:
                if sub.isTimeSet: print(Util.TimeTupleListToHumanStr(sub.timeExam))
                else: print("Not Assigned")
    else: # Print single or several subject
        for sub in msg[0:]: PrintSubject(subjects[int(sub)])

# Print conflicting subjects
def PrintConflict():
    col = Exam.CollisionCheck(students,subjects)
    if len(col) == 0:
        print(GetStrAwesome("There's no conflicting Subjects! Good job!"))
    else:
        print(GetStrAwesome("Oof! some subjects collides."))
        print("Amount:", len(col))
        print("Ids:",col)
        print("Names: ",end="")
        for i in col:
            print(subjects[i].name,end=", ")


