import Util

# CollisionCheck: check if students have colliding timetable
# - Input Arguments
#   students: student data
#   subjects: subject data
def CollisionCheck(students, subjects):
    colSubjects = set()
    for stu in students:
        indexs = list()
        times = list()
        for sub in stu.subjectEnrolled:
            for j in subjects[sub].timeExam:
                if j in times:
                    colSubjects.add(sub)
                    colSubjects.add(indexs[times.index(j)])
                times.append(j)
                indexs.append(sub)
    return list(colSubjects)

# IdealCheck: find the student has examtable that does not satisfy condition
# - Input Arguments
#   students: student data
#   subjects: subject data
#   minGap: minimun of gap between exam
#   maxExam: maxium number of Exam for one day
def IdealCheck(students, subjects, minGap=2, maxExam=2):
    notAcceptStudents=[]
    for stu in students:
        table=[]
        for sub in stu.subjectEnrolled:
            if len(subjects[sub].timeExam) == 0: continue
            if type(subjects[sub].timeExam[0]) == tuple:
                examTimelist=[]
                for time in subjects[sub].timeExam:
                    examTimelist.append(int(time[0])*48+int(time[1]))
            else:
                examTimelist=subjects[sub].timeExam
            table.append([min(examTimelist), max(examTimelist)])
            i2= examTimelist[0]
            for i in range(len(examTimelist[1:])):
                if examTimelist[i]-i2>1:
                    table.remove(table[-1])
                    table.append([min(examTimelist[:i]), max(examTimelist[:i])])
                    table.append([min(examTimelist[i:]), max(examTimelist[i:])])
                    break
                i2=examTimelist[i]
        for day in ["Mon","Tue","Wed","Thr","Fri","Sat","Sun"]:
            testForDay=[]
            flag=False
            for i in table:
                if day in Util.TimeIntToStr(i[0],start=0,end=48):
                    testForDay.append(i)
            if len(testForDay)>maxExam:
                notAcceptStudents.append(stu.id)
                break
            elif len(testForDay)>1:
                for j,i in enumerate(testForDay):
                    start1=i[0]
                    end1=i[1]
                    for j2 in testForDay[j+1:]:
                        start2=j2[0]
                        end2=j2[1]
                        tempGap1=start1-end2
                        tempGap2=start2-end1
                        gap=max(tempGap1,tempGap2)
                        if gap<=minGap:
                            notAcceptStudents.append(stu.id)
                            flag=True
                            break
                    if flag==True:
                        break
            if flag==True:
                break
    return notAcceptStudents
