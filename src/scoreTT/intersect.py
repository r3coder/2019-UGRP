from itertools import combinations as cC, product

def joint(*argv):
    for a in argv:
        for i in range(len(a)):a[i]=set(a[i])
    subjects_all_sections=[tuple(a) for a in argv]
    section_count=[len(each_subject) for each_subject in argv] #[3,3,3]
    J={}
    ranges=[tuple(i for i in range(count)) for count in section_count]
    for p in product(*ranges): # (0,0,0)~(2,2,2)
        sets=[subjects_all_sections[idx][p[idx]] for idx in range(len(p))]
        p_plus=tuple([str(i+1)+'분반' for i in p])
        J[p_plus]=len(set.intersection(*sets))
    for i,v in J.items(): print(i,v)

A=[['std9', 'std7', 'std11', 'std5'], ['std8', 'std1', 'std3', 'std2'], ['std10', 'std4', 'std12', 'std6']]
B=[['std10', 'std7', 'std5', 'std3'], ['std11', 'std1', 'std12', 'std8'], ['std6', 'std2', 'std9', 'std4']]
C=[['std7', 'std4', 'std9', 'std6'], ['std12', 'std8', 'std3', 'std10'], ['std11', 'std5', 'std2', 'std1']]
joint(A,B,C)


#########################################################################################################ㅍ
# a=[(1,3,5),(2,6,9),(4,8,10)]
# b=[(2,5,9),(1,4,10),(3,6,8)]

def joint_try1(*argv):
    for a in argv:
        for i in range(len(a)):a[i]=tuple(a[i])
    listed=[tuple(a) for a in argv]
    idxDict={subject: i+1 for i, subject in enumerate(listed)}
    J={(idxDict[s1],idxDict[s2]): len(set(c1) & set(c2)) 
        for s1, s2 in cC(listed,2) for c1,c2 in product(s1,s2)}
    print(J)
    # for idx, (c1,c2) in enumerate(product(a,b)): J[(int(idx/3+1),idx%3+1)]=len(set(c1) & set(c2))