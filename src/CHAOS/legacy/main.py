#-*-coding:utf-8-*-
import DataLoad
import Util
from Student import Student
from Subject import Subject

courseList = DataLoad.FromFileWithTag("../data/19SpringCourseList.csv")
# print(courseList)
subjects = []
for i in courseList:
    subjects.append(Subject(i))


# Add and remove student to class example
# lst = [100,101,102,103]
# l1 = lst.copy()
# l2 = lst.copy()
# a = Student(201611130, 1, l1)
# b = Student(201611140, 1, l2)
# print(subjects[1].studentAttend, a.subjectSurvey, b.subjectSurvey)
# # subjects[1].EnrollStudent(a)
# # subjects[1].EnrollStudent(b)
# # a.EnrollSubject(subjects[1])
# # b.EnrollSubject(subjects[1])
# print(subjects[1].studentAttend, a.subjectSurvey, b.subjectSurvey)
# subjects[1].DismissStudent(a)
# print(subjects[1].studentAttend, a.subjectSurvey, b.subjectSurvey)

# data loading
# courseList = DataLoad.FromFileWithTag("../data/19SpringCourseList.csv")
# classrooms = DataLoad.FromFileWithTag("../data/19SpringClassRoom.csv")
# instructor = DataLoad.FromFileWithTag("../data/19SpringInstructorSurvey.csv")
# student = DataLoad.FromFileWithTag("../data/19SpringStudentSurveySubject.csv")
