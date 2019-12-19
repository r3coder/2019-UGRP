import csv

fff = "19SpringStudentEnroll"
fr = open(fff+".csv","r",encoding='utf-8')
fw = open(fff+"_hash.csv","w",encoding='utf-8')
r = csv.reader(fr)
w = csv.writer(fw)
stulist = list()
c = True
for line in r:
    if c: c=False; continue
    if int(line[5]) not in stulist:
        stulist.append(int(line[5]))
    line[5] = stulist.index(int(line[5]))
    w.writerow(line)
fw.close()

