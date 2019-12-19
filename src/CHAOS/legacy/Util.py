# Util.py
# Several useful functions

import datetime

week = ["Mon","Tue","Wed","Thr","Fri","Sat","Sun"]

# Util.TimeStrToInt: Convert time string to int value
# - Input Arguments
#   value(str): time as string, "### HH:MM" Style
#   unit(int): Optional, minimum timetable division unit ex) 1h: 24, 30min: 48, 15min: 96
#   start(int): Optional, starting division
#   end(int): Optional, ending division ex) if timetable ends at 22:30, with division is 48, end is 45
# - Output
#   res(int): time as int, return -1 if first 
def TimeStrToInt(value, unit=48, start=18, end=45):
    res = 0
    try:
        res += week.index(value[:3])*(end-start)
    except: # week text is not available
        return -1
    res += int((int(value[4:6])*60+int(value[7:]))*unit/(24*60))-start
    return res
# Util.TimeIntToStr: Convert time int to string value
# - Input Arguments
#   value(int): time as int
#   unit(int): Optional, minimum timetable division unit ex) 1h: 24, 30min: 48, 15min: 96
#   start(int): Optional, starting division
#   end(int): Optional, ending division ex) if timetable ends at 22:30, with division is 48, end is 45
# - Output
#   res(str): time as string
def TimeIntToStr(value, unit=48, start=18, end=45):
    res = ""
    res += week[value//(end-start)] + "-"
    t = (value%(end-start)+start)*(24*60)//unit
    res += str(t//60).zfill(2) + ":"
    res += str( t%60).zfill(2)
    return res

# Util.TimeStrToTuple: Convert time string to tuple, (Day, Time)
# - Input Arguments
#   value(str): time as string, "### HH:MM" Style
#   unit(int): Optional, minimum timetable division unit ex) 1h: 24, 30min: 48, 15min: 96
# - Output
#   res(tuple): time as tuple (Day, Time), return None if first 
def TimeStrToTuple(value, unit=48):
    t = int((int(value[4:6])*60+int(value[7:]))*unit/(24*60))
    try:
        return (week.index(value[:3]), t)
    except: # week text is not available
        return None

# Util.TimeTupleToStr: Convert time tuple to string value
# - Input Arguments
#   value(tuple): time as tuple
#   unit(int): Optional, minimum timetable division unit ex) 1h: 24, 30min: 48, 15min: 96
# - Output
#   res(str): time as string
def TimeTupleToStr(value, unit=48):
    res = ""
    res += week[value[0]] + "-"
    t = value[1]*(24*60)/unit
    res += str(t//60).zfill(2) + ":"
    res += str(t%60).zfill(2)
    return res

# Util.TimeRangeToList: convert data range to List
# - Input Arguments
#   value(str): input value
# - Output
#   res(list(string)): list of time range

def TimeRangeToList(value):
    res=[]
    if 'or' in value:
        for i in value.split('or'):
            if i[0]==" ":
                i=i[1:]
            for j in TimeRangeToList(i):
                res.append(j)
    else:
        day=value.split()[0]
        start=day+" "+value.split()[1].split('-')[0]
        end=day+" "+value.split()[1].split('-')[1]
        for i in range(TimeStrToInt(start),TimeStrToInt(end)):
            res.append(TimeIntToStr((i)))
    return res

# Util.StrToType: Convert input data to given type
# - Input Arguments
#   value(str): input value
#   valueType(str): Optional, input type
#   delim: Optional, delimiter if input is listofstr or listofint
# - Output
#   (type): value converted with valueType type
def StrToType(value, valueType="string", delim=" "):
    if valueType=="string" or valueType=="str":
        return value
    elif valueType=="int":
        try: return int(value)
        except: return None
    elif valueType=="float":
        try: return float(value)
        except: return None
    elif valueType=="bool":
        if value=="1" or value=="True" or value=="true": return True
        else: return False
    elif valueType=="listofstr" or valueType=="listofstring":
        try: return value.split(delim)
        except: return None
    elif valueType=="listofint":
        tl = value.split(" ")
        res = []
        for e in tl:
            try: res.append(int(e))
            except: return None
        return res

# Util.InstructorStrToId: Convert instructor string to id
# - Input arguments
#   inst(list(str)): instructor list string
#   data(list): instructor name as list
#   delim(str): optional, delimiter
# - Output
#   res(list(int)): instructor id as list
def InstructorStrToId(inst, data, delim=" "):
    res = []
    for i in inst.split(delim):
        try: res.append(data.index(i))
        except: return None
    return res

# Util.ListToStr: Convert List to string with delimiter
# - Input arguments
#   l(list): list to convert into string
#   delim(str): optional, delimiter string between elements
# - Output
#   res(str): string converted from list
def ListToStr(l,delim=","):
    res = ""
    for i in l:
        res += str(i) + delim
    res = res[0:len(res)-1]
    return res

# Util.ListsToStrRecursive: Convert n-dim List to string with delimiter
# - Input arguments
#   l(n-dim list): n-dimentionary list to convert into string (ex) list of list, list of list of list, etc...
#   delim(list(str)): optional, delimiter string between elements, from deepest list
# - Output
#   res(str): string converted from list
def ListsToStrRecursive(l, delim=[",","\n"]):
    res = ""
    delen = 1 if len(delim)==1 else len(delim)-1
    if type(l[0]) == list:
        for i in l:
            res += ListsToStrRecursive(i,delim[:delen]) + delim[len(delim)-1]
    else:
        res += ListToStr(l,delim[0])
    return res 

# Util.GetCurrentTimeStr: Get current time string
# - Output
#   res(str): current time string
def GetCurrentTimeStr():
    d = datetime.datetime.now()
    return str(d.year).zfill(4)+str(d.month).zfill(2)+str(d.day).zfill(2)+"_"+str(d.hour).zfill(2)+str(d.minute).zfill(2)+str(d.second).zfill(2)

#Utill.DgistStrToTimeStrList: convert DGISTStr to general Str list
# - Input arguments
#   value(str): DGIST string("#1B-3A(E4 - 114), #1B-3A(E4 - 114)") (# is korean)
# - Output
#   res(list(str)): string time range convert time list
def DgistStrToTimeStrList(value):
    koreanWeek=["월","화","수","목","금","토","일"]
    res=[]
    for i in value.split("("):
        for j in koreanWeek:
            if j in i:
                i=i[i.find(j)+1:]
                [startStr,endStr]=i.split("-")
                if startStr[-1] == "A":
                    start = int(startStr[:-1]) * 2 -2 +27*koreanWeek.index(j)
                elif startStr[-1]=="B":
                    start = int(startStr[:-1]) * 2 -1+27*koreanWeek.index(j)
                if endStr[-1] == "A":
                    end = int(endStr[:-1]) * 2 - 2+27*koreanWeek.index(j)
                elif endStr[-1]=="B":
                    end = int(endStr[:-1]) * 2 -1+27*koreanWeek.index(j)
                for i2 in range(start,end+1):
                    res.append(TimeIntToStr(i2))
    return res

#Utill.DgistStrToClassroomStrList: get classroom from string
# - Input arguments
#   value(str): DGIST string("#1B-3A(E4 - 114), #1B-3A(E4 - 114)") (# is korean)
# - Output
#   res(list(str)): classroom list
def DgistStrToClassroomStrList(value):
    res=[]
    for i in value.split("("):
        if ")" in i:
            res.append(i.split(")")[0])
    return res

#Utill.Union: get classroom from string
# - Input arguments
#   value(list): list(int) or list(tuple)
# - Output
#   res(list(type)): union list

def UnionList(listt,index="x"):
    if len(listt) <1:
        return listt
    res=[]
    intList=[]
    for time in listt:
        intList.append(int(time[0])*48+int(time[1]))
    i2 = intList[0]
    temp_i=0
    for i in range(len(intList[0:])):
        if intList[i] - i2 > 1:
            temp=[]
            for j in range(min(intList[temp_i:i]), max(intList[temp_i:i])+1):
                temp.append((j//48,j%48))
            res.append(temp)
            temp = []
            for j in range(min(intList[i:]), max(intList[i:])+1):
                temp.append((j//48,j%48))
            res.append(temp)
            temp_i=i
        i2 = intList[i]
    if temp_i==0:
        res.append(listt)
        return res
    if index=="x":
        return res
    else:
        return res[index]


def LimitStrToTupleList(value):
    res = list()
    for si, s in enumerate(value.split(",")):
        msg = ""
        if s[0] == "x":
            for i in s[1:]:
                msg += "1" if int(i,16)%16>=8 else "0"
                msg += "1" if int(i,16)%8 >=4 else "0"
                msg += "1" if int(i,16)&4 >=2 else "0"
                msg += "1" if int(i,16)&2 ==1 else "0"
        elif s[0] == "t":
            msg = s[1:]
            while len(msg)>=8:
                startTime = int(msg[0:2])*2+int(msg[2:4])//30
                endTime = int(msg[4:6])*2+int(msg[6:8])//30
                for i in range(startTime,endTime):
                    res.append((si, i))
                if len(msg)==8: break
                else: msg = msg[8:]
            continue
        else:
            msg = s[0:]
        l = len(msg)
        for vi, v in enumerate(msg):
            if v=="1":
                for idd in range(48//l*vi,(48//l)*(vi+1)):
                    res.append((si, idd))
    return res


def XOToBool(x):
    if x == "" or x == None:   return False
    elif x == "x" or x == "X": return False
    elif x == "o" or x == "O": return True
    else:                      return True

def TimeTupleListToHumanStr(inputList):
    temp=UnionList(inputList)
    res=""
    for i in temp:
        res+=str(week[i[0][0]]).zfill(2)+"-"
        res+=str(i[0][1]//2).zfill(2)+":"+str((i[0][1]%2)*30).zfill(2)+"~"
        res+=str(week[i[-1][0]]).zfill(2)+"-"
        res+=str((i[-1][1]+1)//2).zfill(2)+":"+str(((i[-1][1]+1)%2)*30).zfill(2)+", "
    return res[:-2]
