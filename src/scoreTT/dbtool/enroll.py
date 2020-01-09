import csv
from itertools import chain
import random

csv_open=open('../db/SUBJECT.csv', 'r', encoding='utf-8-sig', newline='')
reader=csv.DictReader(csv_open)
SUBJECTS={int(row['id']):row for row in reader}

csv_open=open('../db/src/18FallStudentEnroll.csv', 'r', encoding='utf-8-sig', newline='')
reader=csv.DictReader(csv_open)
ENROLL2018={k:v for k,v in enumerate(reader)}
non_existed=set()
def find_s(row):
    for k,v in SUBJECTS.items():
        if v['course_no']==row['course_no'] and int(float(v['section']))==int(float(row['section'])): return k
        # if all(v[key]==row[key] for key in ('course_no', 'section')): return k
    non_existed.add((row['course_no'],row['section'], row['title']))

idSTUDs=set(row['idSTUD'] for row in ENROLL2018.values())
ENROLLS={id:{'idSTUD':id,'first':[],'second':[]} for id in idSTUDs}
existed=set()

classes=[id for id in SUBJECTS.keys()]
# mapping from 'deleted' to 'unused' 
pairs={'SE204':'SE253', 'SE206':'SE206a', 'SE211':'SE211a', 'HL321':'HL329', 
        'EM674':'ES725', 'IC584':'IC580', 'IC606':'IC607',
        'IC619':'IC667', 'RT618':'RT623', 'SE248':'SE248a', 'SE425':'SE425a',
        'HL322':'HL346', 'NB549':'NB551', 'SE351':'SE350', 'SE302':'SE118',
        'HL333':'HL474a', 'HL326':'HL327', 'ES603':'BS743', 'ES625':'IC586',
        'CR522':'NB553', 'CR529':'NB513', 'HL480':'SE423', 'HL475a':'HL474a',
        'HL331a':'HL338', 'SE373':'SE378', 'SE376':'SE389'}
a=lambda row, code: row['course_no']==code
n=lambda max_section: [str(i) for i in range(1,max_section+1)][random.randrange(0,max_section)]
b='section'
for k, row in ENROLL2018.items():
    # skip UGRP and thesis, unopen subjects
    if row['course_no'] in ['HL303', 'HL472','NB900'] or 'Thesis' in row['title']: continue
    #or any(code==row['course_no'][:2] for code in ['CR', 'ES']) 
    row['course_no']=pairs.get(row['course_no'], row['course_no'])
    if row['course_no']=='SE253': row['section']='1' if row['section'] in ('1','3') else '2'
    if row['course_no']=='SE118': row['section']=('1','2')[random.randrange(0,2)]
    if row['course_no']=='HL104': row['section']=n(17)
    if a(row,'SE106'): row[b]=n(7)
    if a(row,'SE389'): row[b]=n(2)
    if a(row,'HL301'): row[b]=n(7)
    if a(row,'SE112'): row[b]=n(7)
    if a(row,'SE252'): row[b]=n(2)
    if a(row,'HL203'): row[b]=n(10)
    if a(row,'HL330'): 
        # row['course_no']='HL'+str(322+int(row[b]))
        row['course_no']='HL306'
        row['section']='1'
    if a(row, 'SE202b'): 
        row['course_no']='SE222c'
        row['section']=n(2)
    ENROLLS[row['idSTUD']]['first'].append(find_s(row))
    existed.add(find_s(row))
for k, row in ENROLLS.items(): 
    ENROLLS[row['idSTUD']]['second'].append(random.choice(list(set(classes)-set(ENROLLS[row['idSTUD']]['first']))))

for k, row in ENROLLS.items(): 
    for key in ('first', 'second'): ENROLLS[row['idSTUD']][key]=','.join(str(s) for s in ENROLLS[row['idSTUD']][key])

# print(classes)
with open('../db/ENROLL.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
    fieldnames=['idSTUD','first','second']
    writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
    header_writer=csv.writer(csvfile)
    header_writer.writerow(fieldnames)
    for k,v in ENROLLS.items(): writer.writerow(v)

# #제외 과목: thesis. 
# count_students={1:200, 2:180, 3:160, 4:140}
# BORDER_CREDIT=16
# classes={grade: tuple(id for id in SUBJECTS.keys() 
#     if min(int(SUBJECTS[id]['course_no'][2]),4)==grade and SUBJECTS[id]['course_type']!='연구(Thesis)') for grade in [1,2,3,4]}
# print(set(chain(classes[grade] for grade in (1,2,3,4))))

print('unused')
for id in sorted(list(set(classes)-existed)): print(SUBJECTS[id]['course_no'], SUBJECTS[id]['section'], SUBJECTS[id]['title'], id)
print('\ndeleted')
for i in sorted(list(non_existed)): print(i)

# #ENROLL
# 우선 first, 자기 학년 거 중복제거 16 학점 이상 나오게. 
# 이후 4 학년이 아닐 경우, 50% 확률로 다른 분반 추가 (연쇄 가능)
# 25% 확률로 타학년 과목 추가 (연쇄 가능)
# second는 같은 방법으로 하되, 1 개 이상 추가할 확률이 50% 및 최대 7 학점

# REQUESTS는 직접 입력해보자.
# REQUEST: welcome만 어찌 해보자 (단순하게, 각 요일 아침/오후/저녁으로 나누고 요일1+파트1 가져가게.)