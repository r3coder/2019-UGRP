import csv
#load csv files
def csv_loader(fname):
    csv_open=open('../db/src2/'+str(fname)+'.csv', 'r', encoding='utf-8-sig', newline='')
    return csv.DictReader(csv_open)
csv_reader=csv_loader('SUBJECT_APPEND')
SUBJECT_APPEND={(row['course_no'], row['section']):row for row in csv_reader}
csv_reader=csv_loader('SUB')
SUBJECTS={}

#put limit and split(int of list) info
id=1
for row in csv_reader:
    row['id']=id
    if row['course_type']=='연구(Thesis)' or 'UGRP' in row['title']: continue
    row_key=(row['course_no'], str(int(row['section']))) # 멋대로 숫자 앞에 0을 붙임
    for typ in ['limit','limit2']: row[typ]=SUBJECT_APPEND.get(row_key, {typ: '0'})[typ].replace('제한없음','0')
    units=int(max(float(row[typ]) for typ in ('theory','lab'))*2)

    split=2 if row['course_no'][:5]=='HL204' or row['areas']!='인문사회' and units>=6 else 1
    if row['course_no'] in ('SE118','SE272','SE383','HL328','HL321'): split=1 # 임시로 추가
    if row['course_no'] in ('HL101','HL101a','HL111','HL111a','HL345'): split=2 # 임시로 추가
    row['split']=','.join([str(int(units/split))]*split)
    SUBJECTS[id]=row
    id+=1
    
#output
with open('../db/SUBJECT.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
    fieldnames=['id','course_no','section','title','classification','course_type','isLab','fields','areas','credit','theory','lab','limit','limit2','split','remarks']
    csv_writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
    csv_header_writer=csv.writer(csvfile)
    csv_header_writer.writerow(fieldnames)
    for k,v in SUBJECTS.items(): csv_writer.writerow(v)