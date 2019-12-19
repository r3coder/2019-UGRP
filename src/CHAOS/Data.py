
import logging
import csv

from FunctionsTime import *

# GetDataFromCSV: Read data from csv file using csv module
# Input
#   file_directory(str): directory of the input file
#   encoding(str): encoding of the file
# Output
#   res(list): data converted into list of list
def GetDataFromCSV(file_directory, encoding="utf-8"):
    f = open(file_directory, 'r', encoding=encoding, newline='')
    r = csv.reader(f, delimiter=',')
    r = list(r)
    f.close()
    logging.info("Read data from %s"%file_directory)
    return r

# LoadSubjectInfo: Add subject using subject information file
# Input
#   s(simulation): Simulation Class
#   fileLoc(str): location of datafile
def LoadSubjectInfo(s, fileLoc):
    sub_mode = 1
    args_ind = dict()
    data_subject_info = GetDataFromCSV(fileLoc)
    for line in data_subject_info:
        isSubject = False
        if line[0] == "class" or line[0] == "exam": # Set index
            for ind, elem in enumerate(line):
                if elem == "": continue
                args_ind[elem.lower()] = ind
                if line[0] == "class": sub_mode = 1
                elif line[0] == "exam": sub_mode = 2
                    
        args_sub = dict()
        try: # Check if that line is subject - checking if first row is number
            if int(line[0]) == -1: break
            isSubject = True
            args_sub["commandIdx"] = int(line[0])
        except:
            isSubject = False
        if not isSubject: continue
        args_sub["mode"] = sub_mode
        args_sub["infoCode"] = line[args_ind["code"]]
        # infoCredit
        credit = line[args_ind["credit"]].split(":")
        args_sub["infoCreditTotal"] = int(credit[0])
        args_sub["infoCreditClass"] = int(credit[1])
        args_sub["infoCreditPractice"] = int(credit[2])

        args_sub["infoDivision"] = int(line[args_ind["division"]])

        # infoInstructor
        isName = True; inst_name_raw = ""
        for i in line[args_ind["instructor"]]:
            if i == "(" or i == ":": isName = False
            if i == "\n": inst_name_raw += ","; isName = True; continue
            if isName: inst_name_raw += i
            if i == ")": isName = True
        inst_names = inst_name_raw.split(",")
        inst_idxs = list()
        # Add Instructor if doesn't exists on simulator
        for inst_name in inst_names:
            inst_name = inst_name.split("(")[0]
            inst_name_idx = s.SearchInstructorByName(inst_name)
            if inst_name_idx == -1:
                args_inst = dict()
                args_inst["infoName"] = inst_name
                args_inst["subjectEnroll"] = [len(s.subjects)]
                s.AddInstructor(args_inst)
                inst_name_idx = s.SearchInstructorByName(inst_name)
            else:
                s.instructors[inst_name_idx].subjectEnroll.append(len(s.subjects)) #Add subject to assign
            inst_idxs.append(inst_name_idx)
        args_sub["infoInstructor"] = inst_idxs

        # infoName
        args_sub["infoName"] = line[args_ind["name"]]

        args_sub["studentCapacity"] = int(line[args_ind["capacity"]])

        # timeSplit
        if line[args_ind["t_fixed"]] != "": #If time preset is set
            tas= ParseTimeFromText(line[args_ind["t_fixed"]])
            tass=[]; tasa=[]
            for i in tas: tass.append(i[3]); tasa.append((i[0],i[1],i[2])) 
            args_sub["timeAssignedSplit"] = tass
            args_sub["timeIsAssigned"] = [True]*len(tass)
            args_sub["timeIsFixed"] = [True]*len(tass)
            args_sub["timeAssignedTime"] = tasa
            args_sub["timeAssignedClassroom"] = [line[args_ind["classroom"]]]*len(tas)
        else: # Time preset is not set
            tas = line[args_ind["t_split"]].split(",")
            for i in range(len(tas)): tas[i] = int(tas[i])
            args_sub["timeAssignedSplit"] = tas
            args_sub["timeIsAssigned"] = [False]*len(tas)
            args_sub["timeIsFixed"] = [False]*len(tas)
            args_sub["timeAssignedTime"] = [(0,0,0)]*len(tas)
            args_sub["timeAssignedClassroom"] = [""]*len(tas)
            args_sub["timePrefer"] = ParseTimeFromText(line[args_ind["t_prefer"]])
            args_sub["timeExclude"] = ParseTimeFromText(line[args_ind["t_exclude"]])
            
        cmdraw = line[args_ind["command"]]
        if cmdraw != "":
            args_sub["command"] = True
            cmdraw.replace("\n","").replace(" ","")
            cmds = cmdraw.split("/")
            for cmd in cmds:
                cc = cmd.split(",")
                if cc[0].lower() in ["subsame"]:
                    l=[args_sub["commandIdx"]]
                    for i in cc[1:]: l.append(int(i))
                    args_sub["commandSubSame"] = l
                elif cc[0].lower() in ["subclose"]:
                    l=[args_sub["commandIdx"]]
                    for i in cc[1:]: l.append(int(i))
                    args_sub["commandSubClose"] = l
                elif cc[0].lower() in ["subdiffhour"]:
                    l=[args_sub["commandIdx"]]
                    for i in cc[1:]: l.append(int(i))
                    args_sub["commandSubDiffHour"] = l
                elif cc[0].lower() in ["subdiff", "subdiffday"]:
                    l=[args_sub["commandIdx"]]
                    for i in cc[1:]: l.append(int(i))
                    args_sub["commandSubDiffDay"] = l
        s.AddSubject(args_sub)
    logging.info("Loaded %d Subjects, %d Instructors"%(len(s.subjects),len(s.instructors)))

# LoadStudentSurvey: Load Student Survey
# Input
#   s(simulation): Simulation Class
#   fileLoc(str): location of datafile
def LoadStudentSurvey(s, fileLoc):
    data_student_survey = GetDataFromCSV(fileLoc)
    subjectTuple = list()
    subjectDivisionCount = dict()
    for ind in data_student_survey[1]:
        sub_code = ind.split("\t")[0].split(" ")[0]
        # ISSUE: Check division for SE105 and SE111 -> SE105a, SE105b etc... > line 118
        if len(s.SearchSubjectsByCode(sub_code)) > 0:
            if sub_code in subjectDivisionCount:
                subjectDivisionCount[sub_code] += 1
                division = subjectDivisionCount[sub_code]
            else:
                division = 1
                subjectDivisionCount[sub_code] = 1
            subjectTuple.append((sub_code, division))
        else:
            subjectTuple.append(0)

    for line in data_student_survey[2:]:
        args_stu = dict()
        args_stu["infoId"] = int(line[0])
        args_stu["infoGeneration"] = line[8]
        args_stu["subject1st"] = list()
        args_stu["subject2nd"] = list() 
        for ind, sub in enumerate(subjectTuple):
            if sub == 0: continue
            sub_ind = s.SearchSubjectByCodeAndDivision(sub[0], sub[1])
            if sub_ind == -1: # ISSUE: Can't find subject > line 97
                logging.warning("couldn't find Subject:%s-%d"%(sub[0],sub[1]))
                continue
            if line[ind] == "필수":
                args_stu["subject1st"].append(sub_ind)
            elif line[ind] == "선택":
                args_stu["subject2nd"].append(sub_ind)
        s.AddStudent(args_stu)

    logging.info("Loaded %d Students"%len(s.students))

def LoadInstructorSurvey(s, fileLoc):
    data_instructor_survey = GetDataFromCSV(fileLoc)
    countUpdate = 0
    for line in data_instructor_survey[1:]:
        ind_inst = s.SearchInstructorByName(line[0])
        if ind_inst == -1:
            logging.warning("couldn't find Instructor:%s"%line[0])
            continue
        args_inst = dict()
        s.instructors[ind_inst].timeImpossible = ParseTimeFromText(line[1])
        s.instructors[ind_inst].timePrefer1st = ParseTimeFromText(line[2])
        s.instructors[ind_inst].timePrefer2nd = ParseTimeFromText(line[3])
        s.instructors[ind_inst].timePrefer3rd = ParseTimeFromText(line[4])
        countUpdate += 1
    logging.info("Updated %d Instructors"%countUpdate)

def LoadClassroomInfo(s, fileLoc):
    data_classroom_info = GetDataFromCSV(fileLoc)
    for line in data_classroom_info[1:]:
        args_cls = dict()
        args_cls["infoCode"] = line[1]
        args_cls["infoName"] = line[2]
        if line[3] in ["","X"]:
            args_cls["infoIsAssignable"] = False
        else:
            args_cls["infoIsAssignable"] = True
            args_cls["subjectAssignable"] = line[3].split(",")
        if line[4]=="" or int(line[4])==0: v = False
        else: v = True
        args_cls["infoIsRecordable"] = v
        args_cls["infoBoardType"] = line[5]
        args_cls["infoShape"] = line[6]
        if line[7]=="": v = 0
        else: v = int(line[7])
        args_cls["infoCapacity"] = v
        if line[4]=="" or int(line[4])==0: v = False
        else: v = True
        args_cls["infoIsProjector"] = v
        s.AddClassroom(args_cls)


# LoadExamStudents: Load ExamStudent data
def LoadExamStudents(self, dir, ver="1.0"):
    ai = dict()
    data = GetDataFromCSV(dir)
    if data[0][0] != "examstudent":
        logging.error("Input file is wrong")
        return -1
    for ind, elem in enumerate(data[1]):
        if elem == "": continue
        ai[elem] = ind
        
    for line in data[2:]:
        stu_ind = self.SearchStudentById(int(line[ai["id"]]))
        if stu_ind == -1:
            # logging.info("Adding student %d"%int(line[ai["id"]]))
            ds = dict()
            ds["infoId"] = int(line[ai["id"]])
            self.AddStudent(ds)
            stu_ind = self.SearchStudentById(int(line[ai["id"]]))
        sub_ind = self.SearchSubjectByCodeAndDivision(line[ai["code"]], int(line[ai["division"]]))
        if sub_ind == -1:
            # logging.warning("couldn't find Subject:%s-%d"%(line[ai["code"]], int(line[ai["division"]])))
            continue
        self.subjects[sub_ind].studentAttend.append(stu_ind)
    return 0

def ParseBoolFromText(s):
    if s in ["O", "1", "o"]:
        return True
    return False


# LoadExamSubjects: Load ExamSubject data
def LoadExamSubjects(self, dir, ver="1.0"):
    ai = dict()
    data = GetDataFromCSV(dir)
    if data[0][0] != "examsubject":
        logging.error("Input file is wrong")
        return -1
    for ind, elem in enumerate(data[1]):
        if elem == "": continue
        ai[elem] = ind

    for line in data[2:]:
        if ParseBoolFromText(line[ai["examon"]])==False and ParseBoolFromText(line[ai["lectureonexam"]])==False:
            continue
        ds = dict()
        ds["infoCode"] = line[ai["code"]]
        ds["infoName"] = line[ai["name"]]
        ds["infoDivision"] = int(line[ai["division"]])
        # ds["instructor"] <- Additional work

        tas= ParseTimeFromTimetableText(line[ai["timeassigned"]])
        tass=[]; tasa=[]
        for i in tas: tass.append(i[3]); tasa.append((i[0],i[1],i[2])) 
        ds["examAssignedLectureTime"] = tasa
        ds["examAssignedLectureSplit"] = tass
        ds["examOn"] = ParseBoolFromText(line[ai["examon"]])
        ds["timeIsAssigned"] = [False]
        ds["timeAssignedTime"] = []
        ds["timeAssignedSplit"] = []
        if line[ai["examlength"]] != "":
            ds["timeAssignedSplit"] = [int(line[ai["examlength"]])]
        if ParseBoolFromText(line[ai["lectureonexam"]]):
            ds["examLectureOnExam"] = True
            ds["timeAssignedTime"] = tasa
            ds["timeAssignedSplit"] = tass
            ds["timeIsAssigned"] = [True] * len(tasa)
        if ParseBoolFromText(line[ai["examonlecture"]]):
            if ParseBoolFromText(line[ai["eolfront"]]):
                ds["timeAssignedTime"] = [tasa[0]]
                ds["timeAssignedSplit"] = [tass[0]]
                ds["timeIsAssigned"] = [True]
            elif ParseBoolFromText(line[ai["eolback"]]):
                ds["timeAssignedTime"] = [tasa[1]]
                ds["timeAssignedSplit"] = [tass[1]]
                ds["timeIsAssigned"] = [True]
            elif ParseBoolFromText(line[ai["eoleither"]]): # Might need change
                ds["timeAssignedTime"] = [tasa[0]]
                ds["timeAssignedSplit"] = [tass[0]]
                ds["timeIsAssigned"] = [True]
            elif ParseBoolFromText(line[ai["eolall"]]):
                ds["timeAssignedTime"] = tasa
                ds["timeAssignedSplit"] = tass
                ds["timeIsAssigned"] = [True]* len(tasa)
        
        if line[ai["examtimeprefer"]] != "":
            ds["timePrefer"] = ParseTimeFromText(line[ai["examtimeprefer"]])
        
        self.AddSubject(ds)

    return 0