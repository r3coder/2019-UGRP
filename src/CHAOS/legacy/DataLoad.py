# DataLoad.py
# Functions about data loading from file

import Util
import csv


def FromCsvFile(loc, ignore = [0, 1]):
    res = []
    f = open(loc, 'r', encoding='utf-8'); c = 0
    r = csv.reader(f)
    for line in r:
        if c not in ignore:
            res.append(line)
        c+=1
    return res

# DataLoad.FromFile : Load data from file, and return list with parsed.
# - Input Arguments
#   loc(str): file location
#   delim(str): Optional, delimiter
#   ignore(list[int]): Optional, ignoring line
# - Output
#   res(list[list[str]]): list that holds data from file with parsed.
def FromFile(loc, delim=",", ignore=[0, 1]):
    res = []
    f = open(loc); c = 0;
    for idx in f.readlines():
        if c not in ignore:
            res.append(idx.replace("\n","").replace("\r","").split(delim))

        c += 1
    f.close()
    return res

# DataLoad.FromFileWithTag : Load data from file, and return dictionary with key and values
# - Input Arguments
#   loc(str): file location
#   delim(str): Optional, delimiter
#   ignore(list[int]): Optional, ignoring line
#   tag(list[str]): Optional, tag for dictionary. If empty, uses first line of raw data. If a element of tag is empty, then it ignores that row
#   tagType(list[str]): Optional, type for each tag
# - Output
#   res(list[dict]): list of dict that holds data from file with parsed.
def FromFileWithTag(loc, delim=",", ignore=[0, 1], tag=[], tagType=[]):
    res = []
    f = open(loc, 'r', encoding='utf-8-sig');  c = 0;
    for idx in f.readlines():
        if c == 0 and len(tag)==0:
            tag = idx.replace("\n","").replace("\r","").split(delim)
        if c == 1 and len(tagType)==0:
            tagType = idx.replace("\n","").replace("\r","").split(delim)
        if c not in ignore:
            l = idx.replace("\n","").replace("\r","").split(delim)
            t = dict()
            for idx in range(len(tag)):
                if tag[idx] != "":
                    t[tag[idx]] = Util.StrToType(l[idx], tagType[idx])
            res.append(t)
        c+=1
    f.close()
    return res

# DataLoad.StudentEnroll: Load StudentEnroll data and return things
# - Input Arguments
#   loc(str): studnet enroll file location
#   code(list[str]): list of subject code
# - Output
#   res(dict()): dictionary that holds key as student id and value as enroll data
# This code ignores subject that is not existing in current subject code
def StudentEnroll(loc, code):
    res = dict()
    f = open(loc)
    # ignore first line (title)
    f.readline()
    for idx in f.readlines():
        k = idx.split(",")
        if k[1] in code:
            if k[3] in res.keys():
                res[k[3]].append(code.index(k[1]))
            else:
                res[k[3]] = [code.index(k[1])]
    return res
