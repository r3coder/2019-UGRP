import Util

# TimetableToCsv: write subject's timetable data to csv file
# - Input argument
#   subjects(list(Subject)): Subject data to wrtie
#   csvDir(str): target csv file location
#   grade: grade to write
# - Output file
#   Writes csv file to csvDir
def TimetableToCsv(subjects, csvDir = "result.csv", grade=[1,2,3,4], mode = "Normal"):
    timetable = list()
    for i in range(48*7):
        timetable.append(list())
    for ind, s in enumerate(subjects):
        if mode == "Exam": t = s.timeExam;
        else: t = s.time
        if len(t) == 0: continue
        if s.targetGrade not in grade:
            continue
        ttIndex = 0
        isEmpty = False
        while isEmpty == False:
            isEmpty = True
            for j in t:
                if type(j) == tuple: j = j[0]*48+j[1] # not stable
                if len(timetable[j]) < ttIndex+1:
                    while len(timetable[j]) <= ttIndex+1:
                        timetable[j].append(-1)
                if timetable[j][ttIndex]!=-1:
                    ttIndex+=1; isEmpty = False; break
        for j in t:
            if type(j) == tuple: j = j[0]*48+j[1] # not stable
            timetable[j][ttIndex] = ind
            
    output_file = open(csvDir, "w", encoding='utf-8-sig')
    for i in range(len(timetable)):
        s = Util.TimeIntToStr(i,start=0,end=48) + ","
        for j in timetable[i]:
            if j >= 0: s += subjects[j].GetLectureStr() + ","
            else: s += ","
        output_file.write(s + "\n")
    output_file.close()

