# Basic settings
HOUR={'START':9, 'LUNCH':12, 'DINNER':18, 'END':23, 'MEAL_DURATION':1}
DAYS, TIME_UNIT = 5, 30
LENGTH_HOUR={
    'MORNING':HOUR['LUNCH']-HOUR['START'], 
    'NOON':HOUR['DINNER']-(HOUR['LUNCH']+HOUR['MEAL_DURATION']), 
    'EVE':HOUR['END']-(HOUR['DINNER']+HOUR['MEAL_DURATION']),
    'DAY':HOUR['END']-HOUR['START']
}; SLOT_COUNT={
    'HOUR':int(60/TIME_UNIT), #it would be 2
    'DAY':LENGTH_HOUR['DAY']*int((60/TIME_UNIT)),
    'WEEK':(LENGTH_HOUR['DAY']*int((60/TIME_UNIT)))*DAYS
}; SLOTS={
    'MEAL': ((h-HOUR['START'])*SLOT_COUNT['HOUR']+i+ j*SLOT_COUNT['DAY']
        for h in (HOUR['LUNCH'], HOUR['DINNER']) for i in range(HOUR['MEAL_DURATION']*SLOT_COUNT['HOUR']) for j in range(DAYS)),
    'MORNING':(i+j*SLOT_COUNT['DAY'] for i in range(LENGTH_HOUR['MORNING']*SLOT_COUNT['HOUR']) for j in range(DAYS)),
    'NOON': ((HOUR['LUNCH']+HOUR['MEAL_DURATION']-HOUR['START'])*SLOT_COUNT['HOUR']+i+j*SLOT_COUNT['DAY'] 
        for i in range(LENGTH_HOUR['NOON']*SLOT_COUNT['HOUR']) for j in range(DAYS)),
    'EVE': ((HOUR['DINNER']+HOUR['MEAL_DURATION']-HOUR['START'])*SLOT_COUNT['HOUR']+i+j*SLOT_COUNT['DAY']
        for i in range(LENGTH_HOUR['EVE']*SLOT_COUNT['HOUR']) for j in range(DAYS))
}
##################################################################################
import csv
import re
import random

csv_open=open('../db/src2/REQ.csv', 'r', encoding='utf-8-sig', newline='')
reader=csv.DictReader(csv_open)
REQs={k:v for k,v in enumerate(reader)}

csv_open=open('../db/SUBJECT.csv', 'r', encoding='utf-8-sig', newline='')
reader=csv.DictReader(csv_open)
SUBJECTS={int(float(row['id'])):row for row in reader}

reg="\((.*?)\)"
#re.findall("\(([^[\]]*)\)", data) # this would be more efficient but sadly no work

weekday={day:SLOT_COUNT['DAY']*i for i, day in enumerate(['월','화','수','목','금'])}
conv_slot=lambda hour: int((hour-HOUR['START'])*SLOT_COUNT['HOUR'])
def union_slots(A,B,typ):
    update={'y':0,'n':1}[typ]
    return [A[i] if A[i]==B[i] else update for i in range(len(A))]
def gen_unwelcome(r):
    unwelcome=[]
    for param in re.findall(reg, r['unwelcome']):
        # if '쓰기' in r['title']: print(param)
        params=param.split(',')
        if(len(params)==2): params.insert(1,HOUR['START'])
        if(len(params)==3): params.insert(2,HOUR['END'])
        days, start, end, typ=params
        current=gen_unwelcome_part(days, float(start), float(end), typ)
        unwelcome=current if not len(unwelcome) else union_slots(current, unwelcome, typ)
    if unwelcome and all(i==1 for i in unwelcome): print(r)
    return unwelcome
def gen_unwelcome_part(days, start, end, typ): #되는 시간을 받고 unwelcome을 return
    base={'y':1,'n':0}[typ]
    coat={'y':0,'n':1}[typ]
    slots=[base]*SLOT_COUNT['WEEK']
    for day in days:
        for i in range(conv_slot(start),conv_slot(end)): slots[weekday[day]+i]=coat
    return slots

non_existed=set()
# def find_s(row):
#     for k,v in SUBJECTS.items():
#         if all(v[key]==row[key] for key in ('course_no', 'section')): return k
#     non_existed.add((row['course_no'],row['section'], row['title']))

def find_s(row):
    for k,v in SUBJECTS.items():
        if v['course_no']==row['course_no'] and int(float(v['section']))==int(float(row['section'])): return k
        # if all(v[key]==row[key] for key in ('course_no', 'section')): return k
    non_existed.add((row['course_no'],row['section'], row['title']))

def find_s_2(classcode):
    no, sec = classcode.split(',')
    for k,v in SUBJECTS.items():
        if no==v['course_no'] and int(float(sec))==int(float(v['section'])): return k
    # non_existed.add(no, sec)

REQUESTS={id:{'idSUBJ':id} for id in SUBJECTS.keys()}

for k, row in REQs.items():
    # print(k, row)
    id=find_s(row)
    if any(ban in row['title'] for ban in ("과목추가", "UGRP", "Thesis")): continue
    if id not in SUBJECTS.keys(): continue # 요청은 했으나 실제로 열리지 않은 과목
    REQUESTS[id]['unwelcome']=gen_unwelcome(row)
    for typ in ['day_separate','day_along','sametime']:
        REQUESTS[id][typ]=[]
        for classcode in re.findall(reg, row[typ]): REQUESTS[id][typ].append(find_s_2(classcode))
    # print(row['stride'])
    # print(re.findall(reg, row['stride']))
    if row['stride']:
        REQUESTS[id]['stride_min'], REQUESTS[id]['stride_max']=re.findall(reg, row['stride'])[0].split(',')

for id in REQUESTS.keys():
    REQUESTS[id]['welcome']=[]
    welcome=[0]*SLOT_COUNT['WEEK']
    for i in range(SLOT_COUNT['DAY']): welcome[weekday[random.choice('월화수목금')]+i]=1
    rdchoice=random.choice(['MORNING','NOON','EVE'])
    # print(type(list(SLOTS[rdchoice])))
    sslots=list(SLOTS[rdchoice])
    # print(sslots)
    for i in sslots: welcome[i]=1
    REQUESTS[id]['welcome']=welcome

for id in REQUESTS.keys():
    # if id==1: print(REQUESTS[id])
    for key in REQUESTS[1].keys(): 
        if key in REQUESTS[id]:
            # print(REQUESTS[id])
            if key in ('day_separate','day_along','sametime'): REQUESTS[id][key]=','.join(str(i) for i in REQUESTS[id][key])
            elif key in ('welcome', 'unwelcome'): REQUESTS[id][key]=''.join(str(i) for i in REQUESTS[id][key])
            # if id==1: print(key, REQUESTS[id][key])
            # if REQUESTS[id][key]==[]: 
            #     print('a')
            #     REQUESTS[id][key]=''

with open('../'+'/db/REQUEST'+'.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
    fieldnames=['idSUBJ','welcome','unwelcome','day_separate','day_along','stride_min','stride_max','sametime']
    writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
    header_writer=csv.writer(csvfile)
    header_writer.writerow(fieldnames)
    for k,v in REQUESTS.items(): writer.writerow(v)