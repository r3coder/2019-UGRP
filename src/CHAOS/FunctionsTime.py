
import logging

timeText = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# TimeValue: Get TimeValue of the timeMoment / timeDuration tuple
# Input
#   time(timeMoment Tuple): timemoment tuple.
# Return
#   int: time value
# Input
#   time(timeDuration Tuple): timduration tuple. Ignores time length
# Return
#   int: time value
def TimeValue(time):
    return time[0]*60*24+time[1]*60+time[2]

# TimeDuration: Get timeDuration tuple
#  - TimeMoment Tuples
# Input
#   timeStart(timeMoment Tuple): time to start
#   timeEnd(timeMoment Tuple): time to end
# Output
#   (timeDuration Tuple): timeDuration tuple
#  - String
# Input
#   timeString(string): DDD HH:MM~HH:MM style
# Output
#   (timeDuration Tuple): timeDuration tuple
#  - Day(int) + String
# Input
#   timeString(string): Day index: 0~6
#   timeString(string): HH:MM~HH:MM style
# Output
#   (timeDuration Tuple): timeDuration tuple
def TimeDuration(*args, **kwds):
    if len(args) == 1 and type(args[0]) == str:
        day = args[0].split(" ")[0]
        time_lst = args[0].split(" ")[1].split("~")
        day_int = timeText.index(day)
        time = (day_int,int(time_lst[0].split(":")[0]),int(time_lst[0].split(":")[1]))
        time_end = (day_int, int(time_lst[1].split(":")[0]),int(time_lst[1].split(":")[1]))
        return TimeDuration(time, time_end)
    elif len(args) == 2 and type(args[0]) == int and type(args[1]) == str:
        time_lst = args[1].split("~")
        time = (args[0],int(time_lst[0].split(":")[0]),int(time_lst[0].split(":")[1]))
        time_end = (args[0], int(time_lst[1].split(":")[0]),int(time_lst[1].split(":")[1]))
        return TimeDuration(time, time_end)
    elif len(args) == 2:
        return (args[0][0], args[0][1], args[0][2], TimeValue(args[1])-TimeValue(args[0]))

# TimeTuple: Convert timeDuration / timeMoment to timetuple
# Input
#   td(timeDuration Tuple): timeDuration tuple
#   div(int): Division coefficient on 1 day
#   offset(int): Offset
# Output
#   list(timeTuple Tuple): list of timeTuple - timeDuration mode
# Input
#   td(timeMoment Tuple): timeMoment tuple
#   div(int): Division coefficient on 1 day
#   offset(int): Offset
# Output
#   timeTuple Tuple: timeTuple -timeMoment Mode
def TimeTuple(t, div=48, offset=0):
    if len(t) == 3: #timeMoment mode
        return (t[0], int((TimeValue(t)%(24*60))/(24*60)*div)-offset)
    elif len(t) == 4: #timeDuration mode
        res = list()
        curT = TimeValue(t)
        while curT<TimeValue(t)+t[3]:
            print(curT)
            res.append((t[0],int((curT%(24*60))/(24*60)*div)-offset))
            curT += 24*60/48
        return res

# IsTimeInDuration: Check if time is in duration
#  - TimeMoment Tuples
# Input
#   tm(timeMoment Tuple): time to check
#   td(timeDuration Tuple): time Duration
# Output
#   (Bool): True if tm is in td
def IsTimeInDuration(*args, **kwds):
    if len(args) == 2 and len(args[0]) == 3 and len(args[1]) == 4: # td, tm mode
        if TimeValue(args[0]) >= TimeValue(args[1]) and TimeValue(args[0]) < TimeValue(args[1])+args[1][3]:
            return True
        else:
            return False

    return False

def TimeToText(td):
    res = ""
    if   td[0] == 0: res+="월"
    elif td[0] == 1: res+="화"
    elif td[0] == 2: res+="수"
    elif td[0] == 3: res+="목"
    elif td[0] == 4: res+="금"
    res+=" "
    res+="%02d:%02d"%(td[1],td[2])
    if len(td)==4:
        v = td[1]*60+td[2]+td[3]
        res+="~%02d:%02d"%(v//60,v%60)
    return res


def ParseTimeFromTimetableText(s):
    res = list()
    sl = s.replace("\n","").replace(" ","").split(",")
    for item in sl:
        t = item.split("(")[0]
        if   t[0] == "월": d1 = 0
        elif t[0] == "화": d1 = 1
        elif t[0] == "수": d1 = 2
        elif t[0] == "목": d1 = 3
        elif t[0] == "금": d1 = 4
        t = t[1:]
        t = t.split("-")
        if t[0][-1] == "A": d3 = 0
        else: d3 = 30
        d2 = int(t[0][:-1])
        dx = 30 if t[1][-1] == "B" else 0
        d4 = int(t[1][:-1]) * 60 + dx - d2 * 60 - d3
        # print(int(t[1][:-1]) * 60,dx,d2,d3)
        res.append((d1, d2+8, d3, d4))
    return res

def ParseTimeFromText(s):
    res = list()
    sl = s.replace("\n","").replace(" ","").split("/") # Divide time
    for item in sl:
        if item == "": continue
        if "=" in item: #Normal time mode
            i=item.split("=")
            dayRaw = i[0].split(","); timeRaw = i[1].split(",")
        else:
            dayRaw = item.split(","); timeRaw = ["09:00~22:30"]
        l = item.split(",")
        days = list()
        for d in dayRaw:
            if   d in ["월","Mon"]: days.append(0)
            elif d in ["화","Tue"]: days.append(1)
            elif d in ["수","Wed"]: days.append(2)
            elif d in ["목","Thr"]: days.append(3)
            elif d in ["금","Fri"]: days.append(4)
        for day in days:
            for time in timeRaw:
                t = time.split("~"); tt = t[0].split(":") + t[1].split(":")
                ttt = []
                for i in tt:
                    ttt.append(int(i))
                res.append((day,ttt[0],ttt[1],(ttt[2]*60+ttt[3])-(ttt[0]*60+ttt[1])))
    return res



# TimeListReversed: return time list
def TimeListReversed(t, td):
    tt = []
    for i in range(len(t)):
        tt.append((t[i][0], t[i][1], t[i][2], td[i]))
    lst = []
    for day in range(0,5):
        for hour in range (0,24):
            tag = False
            for v in tt:
                if IsTimeInDuration((day, hour, 0), v) == True: tag = True
            if tag == False: lst.append((day, hour, 0))
            tag = False
            for v in tt:
                if IsTimeInDuration((day, hour, 30), v) == True: tag = True
            if tag == False: lst.append((day, hour, 30))
    return lst