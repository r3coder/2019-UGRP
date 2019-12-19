
# CheckSameSubjectbycode: check the two subject is same by code
# input
#   sub1: subject code
#   sub2: subject code
# Return
#   bool: if subject1 and subject is same return True, else return False
def CheckSameSubjectbyCode(sub1,sub2):
    subcode1=sub1.infoCode
    subcode2=sub2.infoCode
    if subcode1[:5]==subcode2[:5]:
        return True
    else:
        return False

# CheckSameSubjectbyName: check the two subject is same by name
# input
#   sub1: subject code
#   sub2: subject code
# Return
#   bool: if subject1 and subject is same return True, else return False
def CheckSameSubjectbyName(sub1,sub2):
    remove_list=["-심화", "-기초"]
    check_list=["음악I","음악Ⅱ","체육I","체육Ⅱ","Thesis(이,공)"]
    subname1=sub1.infoName
    subname2=sub2.infoName
    if subname1==subname2:
        return True
    for i in remove_list:
        if i in subname1:
            subname1 = sub1.infoName.replace(i,"")
        if i in subname2:
            subname2 =sub2.infoName.replace(i,"")
    if subname1==subname2:
        return True
    for i in check_list:
        if (i in subname1) and (i in subname2):
            return True
    return False
