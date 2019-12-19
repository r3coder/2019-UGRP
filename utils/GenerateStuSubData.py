import csv

fff = "../data/19SpringStudentEnroll_hash"
fr = open(fff+".csv","r")

subjectId = list()
subjectData = list()
studentId = list()
studentData = list()
r = csv.reader(fr)
c = True

for line in r:
    if c: c=False; continue # ignore first line
    # make new subject
    if line[0]+line[2] not in subjectId:
        subjectId.append(line[0]+line[2])
        t = list()
        t.append(len(subjectData))
        t.append(line[0]+"-"+line[2])
        t.append(line[1])
        subjectData.append(t)
    # make new student
    if int(line[5]) not in studentId:
        studentId.append(int(line[5]))
        studentData.append([len(studentId)])
    subjectData[subjectId.index(line[0]+line[2])].append(line[5])
    studentData[studentId.index(int(line[5]))].append(subjectId.index(line[0]+line[2]))

fwt = open(fff+"_student.csv","w")
wt = csv.writer(fwt)
for i in studentData:
    wt.writerow(i)
fwt.close()
fwu = open(fff+"_subject.csv","w")
wu = csv.writer(fwu)
for i in subjectData:
    wu.writerow(i)
fwu.close()
