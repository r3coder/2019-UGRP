#indexing instructors and subjects
import csv
inst_csv=open('INSTRUCTOR.csv', newline='', encoding='utf-8-sig')
reader=csv.reader(inst_csv, delimiter=',', quotechar='"')
inst_dict={}
for line in reader:
    if 'portal_id' in line: continue #skip the header
    inst_dict[line[1]]=line[0]
inst_dict['미배정']=0
inst_csv.close()

#SUBJECTwithINST.csv has identical schema to 개설강좌.xlsx
csv_input=open('SUBJECTwithINST.csv', 'r', encoding='utf-8-sig', newline='') 
csv_output=open('TEACH.csv', 'w', encoding='utf-8-sig', newline='')
rd=csv.reader(csv_input)
wr=csv.writer(csv_output)
for line in rd:
    if '담당교수' in line: #print the header
        wr.writerow(['idSUBJ','idINST'])
    else: 
        for inst in line[-1].split(', '):
            wr.writerow([line[0]]+[inst_dict[inst]])
csv_input.close()
csv_output.close()

# subj_csv=open('SUBJECT.csv', newline='', encoding='utf-8-sig')
# reader=csv.reader(subj_csv, delimiter=',', quotechar='"')
# subj_dict={}
# for line in reader:
#     if 'title' in line: continue #skip the header
#     subj_dict[(line[3], line[4])]=line[0]
# subj_csv.close()


# #put idSUBJ
# csv_input=open('개설강좌.csv', 'r', encoding='utf-8-sig', newline='')
# csv_output=open('preTEACH.csv', 'w', encoding='utf-8-sig', newline='')
# rd=csv.reader(csv_input)
# wr=csv.writer(csv_output)
# for line in rd:
#     if '담당교수' in line: #print the header
#         wr.writerow(line)
#         continue
#     try: 
#         idsubj=subj_dict[(line[1], line[2])]
#         wr.writerow([idsubj]+line[1:])
#     except KeyError: wr.writerow(line)
# csv_input.close()
# csv_output.close()

# #split instructors with each rows
# csv_input=open('preTEACH.csv', 'r', encoding='utf-8-sig', newline='')
# csv_output=open('TEACH.csv', 'w', encoding='utf-8-sig', newline='')
# rd=csv.reader(csv_input)
# wr=csv.writer(csv_output)
# for line in reader:
#     for inst in line[3].split(', '):
#         wr.writerow(line[:-1]+[inst_dict[inst]])
# f.close()
# csvfile.close()