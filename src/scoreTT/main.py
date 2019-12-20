# score 변화 없음
## welcome
## constraint
# 확률과 통계에서 계속 빙빙 도는데 그래도 되는지 확인

# sametime 고치기

# 아웃풋, 사람이 읽을 수 있게 출력
# CPU 병렬 연산 이용 (속도 향상)
# 2차로 코드 만질 때, 연습 과목 별도로 생성하고 학생들 자동 배치
import heapq
import csv
from itertools import combinations as cC, combinations_with_replacement as cH, accumulate, product, chain
import numpy as np
# import random 

H={'START':9, 'LUNCH':12, 'DINNER':18, 'END':23} # Hour
MEAL_DURATION=1
DAYS=5 
TIME_UNIT=30 # units: mins

# WIGGLE = 0.03 #돌릴때마다 매번 같은 결과를 내지 않도록 스코어 계산에서 약간의 랜덤을 부여
ENROLL_CHOICE=('first','second','third')[:2] # choices when making enrollment request
BORDER_CREDIT=16
W_POTENTIAL=0.15
W_POP={'MEAL':0.2, 'MORN':1.0, 'NOON':1.8, 'EVE':0.8}
W_PRIORITY={'공필':2, '교필':1, '교양':0.5}
W_WELCOME=(0, 6, 3, 1)
W_ENROLL={(t1, t2): sum({'first':4, 'second':1}[typ] for typ in (t1, t2))/2 for (t1, t2) in cH(ENROLL_CHOICE, 2)}
FACTOR_DECAY={'unwelcome':0.97, 'day':0.7, 'enroll':0.975}
FACTOR_SCALE={'unwelcome':65, 'day':10, 'enroll':0.8, 'enroll_sub':0.5, 'length':0.5} # 'welcome' uses unwelcome's weighted scale
##################################################################################
SLOT_PER_HOUR=int(60/TIME_UNIT) #it would be 2
SLOT_COUNT={ # hour unit yet
    'MORN':H['LUNCH']-H['START'], 
    'NOON':H['DINNER']-(H['LUNCH']+MEAL_DURATION), 
    'EVE':H['END']-(H['DINNER']+MEAL_DURATION),
    'MEAL':MEAL_DURATION,
    'DAY':H['END']-H['START']}
for typ in SLOT_COUNT.keys(): SLOT_COUNT[typ]*=SLOT_PER_HOUR
SLOT_COUNT['WEEK']=SLOT_COUNT['DAY']*DAYS

def SLOT_START(typ):
    if typ not in H.keys(): typ={'MORN':'START','NOON':'LUNCH','EVE':'DINNER'}[typ]
    start_hour=H[typ]-H['START']
    if typ in ('NOON','EVE'): start_hour+=MEAL_DURATION
    return start_hour*2
SLOTS={typ: [SLOT_START(typ)+i for i in range(SLOT_COUNT[typ])] for typ in ('MORN','NOON','EVE')} # only a day yet
SLOTS['MEAL']=[SLOT_START(typ)+i for typ in ('LUNCH','DINNER') for i in range(SLOT_COUNT['MEAL'])]
for typ in SLOTS.keys(): SLOTS[typ]=tuple(i+day*SLOT_COUNT['DAY'] for i in SLOTS[typ] for day in range(DAYS)) # now in a whole week
##################################################################################
# Preprocess and calculate rating of requests and order to put depending on their rating
def credit(e):
    courses={typ:[] for typ in ENROLL_CHOICE}
    for typ in ENROLL_CHOICE:
        for id in e[typ]:
            if id not in SUBJECTS.keys(): continue # skip UGRP, thesis etc.
            if id not in chain(courses[t] for t in ENROLL_CHOICE): courses[typ].append(id)
    return {typ: sum(SUBJECTS[id]['credit'] for id in courses[typ]) for typ in ENROLL_CHOICE}  

def csv_loader(fname):
    csv_open=open('./db/'+str(fname)+'.csv', 'r', encoding='utf-8-sig', newline='')
    csv_reader=csv.DictReader(csv_open)
    csv_keys={'SUBJECT': 'id', 'REQUEST': 'idSUBJ', 'ENROLL': 'idSTUD'}
    defaults={'stride_min':0,'stride_max':5,'welcome':[1]*SLOT_COUNT['WEEK'],'unwelcome':[0]*SLOT_COUNT['WEEK']}
    output={}
    for row in csv_reader:
        for key in row.keys():
            if row[key]:
                if any(typ in key for typ in ('id','limit','stride')
                ) or key in ('section','credit','theory','lab'): row[key]=int(float(row[key]))
                elif key[:3]=='day' or key in ('split','sametime')+ENROLL_CHOICE: row[key]=tuple(int(i) for i in row[key].split(','))
                if 'welcome' in key: row[key]=tuple(int(i) for i in row[key])
            elif key in defaults: row[key]=defaults[key]
        if fname=='SUBJECT': row['rotating']=0
        output[row[csv_keys[fname]]]=row
    return output
SUBJECTS, REQUESTS, ENROLLS = [csv_loader(fname) for fname in ('SUBJECT', 'REQUEST', 'ENROLL')]
for id, e in ENROLLS.items(): ENROLLS[id]['credits']=credit(e)

# Calculate maximum value of each request type and req_ordered; 'no condition' gets max maximum value
ld_unpop=lambda key: max(W_POP.values())+min(W_POP.values())-W_POP[key]
ld_decay=lambda key, v: FACTOR_SCALE[key]*FACTOR_DECAY[key]**sum(v)
req_unordered=[]
for id, req in REQUESTS.items():
    rating={}
    rating['unwelcome']=ld_decay('unwelcome', (ld_unpop(key)*req['unwelcome'][i] for key in SLOTS.keys() for i in SLOTS[key]))
    pre_welcome=[W_WELCOME[req['welcome'][i]] for i in range(SLOT_COUNT['WEEK'])]; sum_pw=sum(pre_welcome)
    REQUESTS[id]['w_welcome']=[ld_unpop(key)*pre_welcome[i]/sum_pw*rating['unwelcome'] for key in SLOTS.keys() for i in SLOTS[key]]
    rating['welcome']=sum(REQUESTS[id]['w_welcome'])
    rating['day']=ld_decay('day', (len(req[typ]) for typ in ['day_separate', 'day_along']))
    REQUESTS[id]['rating']=rating
    # req_unordered.append(tuple([req, -sum(rating.values())])) # note that negative sign
    req_unordered.append(tuple([req, rating['unwelcome']])) # 까다로운 게 먼저 들어가도록
    # print(SUBJECTS[id]['title'], SUBJECTS[id]['section'], rating)
req_ordered=tuple(req[0]['idSUBJ'] for req in sorted(req_unordered, key=lambda r: r[1]))

# Calculate rating of each pair of subjects with students' requests
ld_scaled_e=lambda e: FACTOR_SCALE['enroll']-FACTOR_SCALE['enroll_sub']*max(e['credits']['first']-BORDER_CREDIT,0)
N=max(SUBJECTS.keys())+1
E=np.zeros([N,N]).astype(int)
for i,v in {(s1,s2): ld_scaled_e(e)*W_ENROLL[(t1,t2)] 
    for e in ENROLLS.values() 
    for t1, t2 in cH(ENROLL_CHOICE, 2) 
    for s1, s2 in [p for p in product(e[t1],e[t2])]
    if SUBJECTS[s1]['course_no']!=SUBJECTS[s2]['course_no'] and s1<=s2}.items(): E[i]=v
E=E+E.T-np.diag(E.diagonal()) # make the matrix symmetric
# print(np.count_nonzero(E)); exit()
# print(len(np.unique(E))); exit()
for (i, j) in cC(SUBJECTS.keys(), 2):
    # if (i,j) not in E: E[(i,j)]=0
    if '공통필수' in (SUBJECTS[xth]['classification'] for xth in (i, j)): E[(i,j)]*=W_PRIORITY['공필']
    elif '인문소양' in (SUBJECTS[xth]['fields'] for xth in (i, j)): E[(i,j)]*=W_PRIORITY['교양']
    else: E[(i,j)]*=W_PRIORITY['교필']
# np.savetxt('fooo.csv', E, delimiter=',',fmt='%d')
E=E.tolist()
## Functions ##################################################################################
ld_first_slots=lambda units, slots: [slots[i] for idx,i in enumerate(accumulate(tuple([0])+units)) if idx<len(units)]
def EnqueueTT(tt): # Put a new subject to all possible slots and calculate a score of each case
    r=REQUESTS[req_ordered[len(tt)]]
    s=SUBJECTS[r['idSUBJ']]
    print('Putting',s['title'],'(',s['course_no'],s['section'],')')
    stride=lambda xth: (2,1)[s['rotating']%2]*xth*SLOT_COUNT['DAY']
    outstep=lambda xth: (1,-1)[s['rotating']%2]*int(s['rotating']/2)*max(s['split']) if xth else 0 #first unit does not move
    day=lambda slot: int(slot/SLOT_COUNT['DAY'])
    day_overflow=lambda slot, xth: day(slot+outstep(xth))!=day(slot+outstep(xth)+s['split'][xth])
    ## Intelligent split-considering slot locating
    old_len=len(heapTT)
    while(old_len==len(heapTT)):
        for slot in range(SLOT_COUNT['WEEK']): # generate slots and calculate for each new tt
            if any([day_overflow(slot, xth) for xth in range(len(s['split']))]): continue
            slots=tuple([(slot+outstep(xth)+stride(xth)+i)%SLOT_COUNT['WEEK'] 
                for xth in range(len(s['split'])) for i in range(s['split'][xth])])
            if r['unwelcome'].count(0)==sum(s['split']): 
                slots=tuple([i for i in range(SLOT_COUNT['WEEK']) if r['unwelcome'][i]==0])
            fs=ld_first_slots(s['split'],slots)
            if any(fs[i+1]==fs[i] for i in range(len(fs)-1)): continue # no different sections are in same day
            tt_new=tt.copy(); tt_new.append((r['idSUBJ'], slots)) #tt_new[r['idSUBJ']]=slots 
            if hash(tuple(tt_new)) not in hashTT: # calculate and put to heap only when the tt is new
                hashTT.add(hash(tuple(tt_new)))
                score=CalScore(tt_new)
                if score!=-float("inf"): heapq.heappush(heapTT, ((-1)*score, tt_new))
                if r['unwelcome'].count(0)==sum(s['split']): break
        if old_len==len(heapTT): 
            s['rotating']+=1
        if s['rotating']>=140: break
            # print(REQUESTS[req_ordered[len(tt)]],SUBJECTS[req_ordered[len(tt)]])
            # print('rotating is now',s['rotating'],'set size:',len(slots_temp))
            # REQUESTS[req_ordered[len(tt)]]['unwelcome']=[0]*SLOT_COUNT['WEEK']    

ld_length=lambda tt: len(tt)**1.02
ld_space=lambda v: -v**0.9
# ld_space=lambda max_v: -max(max_v-MAX_CAPACITY, 0)**1.8   # no use
# def ld_power(sorted_list, typ):
#     decayed_list=[sorted_list[i]*FACTOR_DECAY[typ]**i for i in range(len(sorted_list))]
#     print(sum(decayed_list[:5000]))
#     # print(decayed_list[:300]); exit()
#     # print(FACTOR_SCALE[typ]*sum(decayed_list)); exit()
#     return FACTOR_SCALE[typ]*sum(decayed_list)

ld_power=lambda sorted_list, typ: FACTOR_SCALE[typ]*sum(sorted_list[i]*FACTOR_DECAY[typ]**i for i in range(len(sorted_list)))
def CalScore(tt):
    score_len=ld_length(tt)*FACTOR_SCALE['length']
    score_req={}
    size=[0]*SLOT_COUNT['WEEK']
    for (id, slots) in tt:
        score_req[id]={'constraint':0}
        s,r=SUBJECTS[id],REQUESTS[id]
        score_req[id]['welcome']=r['rating']['welcome']*([slot in r['welcome'] for slot in slots].count(True)/len(slots))
        for typ in ('unwelcome','stride_min','stride_max','day_separate','day_along','sametime'): 
            score_req[id]['constraint']+=check_constraint(r,s,slots,typ)
        if score_req[id]['constraint']==-float("inf"): return -float("inf")
        for slot in slots: size[slot]+=s['limit']+s['limit2']
    score_size=ld_space(max(size))
    for id in SUBJECTS.keys(): # other unput subjects have potential as well
        if id not in score_req.keys():
            if id not in score_req: score_req[id]={}
            score_req[id]['welcome']=W_POTENTIAL*r['rating']['welcome']
            score_req[id]['constraint']=W_POTENTIAL*(sum(r['rating'].values())-r['rating']['welcome'])
    #Calculate how much the timetable meets requests from students
    score_req[id]['enroll']=ld_power(sorted(
        [(W_POTENTIAL**2)*E[s1][s2] if any(s not in tt for s in (s1, s2))
        else (0, E[s1][s2])[int(set(tt[s1]).isdisjoint(set(tt[s2])))]
        for s1, s2 in cC(SUBJECTS.keys(), 2)], reverse=True), 'enroll')
    # print(SUBJECTS[id]['title'], SUBJECTS[id]['section'], score_req[id])
    # print('len:', score_len, 'size:', score_size, 'rating:', sum(sum(score_req[id].values()) for id in SUBJECTS.keys()))
    return score_len+score_size+sum(sum(score_req[id].values()) for id in SUBJECTS.keys()) #+random.random()*1200-600

# ld_split=lambda units, slots: [[slots.pop(0) for _ in range(units[i])] for i in range(len(units))] #slots should be backed up
def check_constraint(r,s,slots,key):
    day=lambda slot: int(slot/SLOT_COUNT['DAY'])
    if key=='unwelcome': 
        if all(r['unwelcome'][slot]==0 for slot in slots): return r['rating']['unwelcome']
        return -float("inf")
    if 'stride' in key:
        fslots=ld_first_slots(s['split'], slots)
        day_diff=[(day(fslots[i+1])-day(fslots[i]))%5 for i in range(len(s['split'])-1)]
        # if 'English' in s['title']: print(all(d >= r['stride_min'] for d in day_diff))
        if 'min' in key and (not r['stride_min'] or all(d >= r['stride_min'] for d in day_diff)): return 0
        if 'max' in key and (not r['stride_max'] or all(d <= r['stride_max'] for d in day_diff)): return 0
        return -float("inf")
    return 0
    # else:
    #     A=ld_first_slots(s['split'],slots)
    #     A=set(day(a) for a in A) if key!='sametime' else set(A)
    #     for id in r[key]:
    #         if id not in dict(tt): continue
    #         B=ld_first_slots(SUBJECTS[id]['split'], dict(tt)[id])
    #         B=set(day(b) for b in B) if key!='sametime' else set(B)
    #         if (key=='day_separate' and not A.isdisjoint(B)) or (
    #             key=='day_along' and not (A.issubset(B) or A.issuperset(B))) or (
    #             key=='sametime' and A!=B): return -float("inf")
    #     if 'day' in key: return r['rating']['day']
    #     return 0

def printTT(tt):
    for id,slots in tt:
        s=SUBJECTS[id]
        print(s['title'],s['section'], slots)
## Main #################################################################################
heapTT=[] #heap of timetable(tt); tt is a list of (idSUBJ, tuple of slots)
hashTT=set() #set
heapq.heappush(heapTT, (0, [])) #start with empty timetable; dictionary type is not hashable
count=0
while len(heapTT[0][1])<N:
    tt=heapq.heappop(heapTT)[1] #[0]: -(score)
    EnqueueTT(tt)
    if not len(heapTT): print("There're conflicts between top priorities."); exit(tt) #return tt
    print('count:',count,'tt size:',len(tt),'heap size:',len(heapTT),'score:',-heapTT[0][0])
    count+=1
print(heapq.heappop(heapTT)[1])