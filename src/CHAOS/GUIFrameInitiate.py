
import wx
import logging
import os
from functools import partial

from GUIFrameWorkspace import FrameWorkspace
from GUITools import *


class FrameInitiate(wx.Frame):
    def __init__(self, conf):
        # Save config
        wx.Frame.__init__(self, None, title = "Timetable Editor / Simulator v%s"%conf.VERSION
                ,size=(conf.F_INIT_WIDTH, conf.F_INIT_HEIGHT))
        self.conf = conf
        self.width = self.GetSize()[0]
        self.height = self.GetSize()[1]

        self.SetBackgroundColour("#DDDDFF")
        
        # Main Box
        boxMain = wx.BoxSizer(wx.VERTICAL)
        # Title
        boxMain.Add(BoxStaticText(self,"Timetable Editor / Simulator",fontSize=30),1,0,0)
        # Line
        boxMain.Add(wx.StaticLine(self, -1, size=(self.GetSize()[0]-10, -1)), 0, wx.ALL, 5)
        # Text helper 0
        boxMain.Add(BoxStaticText(self,"프로그램 실행을 위해서는 CSV 파일을 불러오거나, ttsave 저장 파일을 불러와야 합니다.",fontSize=15),1,0,0)
        # Line
        boxMain.Add(wx.StaticLine(self, -1, size=(self.GetSize()[0]-10, -1)), 0, wx.ALL, 5)
        # Text helper 1
        boxMain.Add(BoxStaticText(self,"CSV 파일들 불러오기",fontSize=15),1,0,0)
        # LoadSubjectInfos
        self.boxSubjectInfo     ,_,self.subjectInfoTextCtrl     ,_,_ = self.CreateBoxLoadData("과목 정보(.csv)")
        self.boxStudentSurvey   ,_,self.studentSurveyTextCtrl   ,_,_ = self.CreateBoxLoadData("학생 설문조사(.csv)")
        self.boxInstructorSurvey,_,self.instructorSurveyTextCtrl,_,_ = self.CreateBoxLoadData("교수 설문조사(.csv)")
        self.boxClassroomInfo   ,_,self.classroomInfoTextCtrl   ,_,_ = self.CreateBoxLoadData("교실 정보(.csv)")
        boxMain.Add(self.boxSubjectInfo,1,0,0)
        boxMain.Add(self.boxStudentSurvey,1,0,0)
        boxMain.Add(self.boxInstructorSurvey,1,0,0)
        boxMain.Add(self.boxClassroomInfo,1,0,0)
        # Line
        boxMain.Add(wx.StaticLine(self, -1, size=(self.GetSize()[0]-10, -1)), 0, wx.ALL, 5)
        # Text helper 2
        boxMain.Add(BoxStaticText(self,"ttsave 파일 불러오기",fontSize=15),1,0,0)
        # Load from ttsave
        self.boxSave,_,self.saveTextCtrl,_,_ = self.CreateBoxLoadData("저장 파일(.ttsave)","ttsave")
        boxMain.Add(self.boxSave,1,0,0)
        # Line
        boxMain.Add(wx.StaticLine(self, -1, size=(self.GetSize()[0]-10, -1)), 0, wx.ALL, 5)
        # Timetable Button
        buttonTT0 = wx.Button(self, -1, label="수업시간표 만들기",size=(self.GetSize()[0]/2,50))
        buttonTT0.Bind(wx.EVT_BUTTON, lambda event: self.OpenFrameWorkspace(event, 0), buttonTT0)
        buttonTT1 = wx.Button(self, -1, label="시험시간표 만들기",size=(self.GetSize()[0]/2,50))
        buttonTT1.Bind(wx.EVT_BUTTON, lambda event: self.OpenFrameWorkspace(event, 1), buttonTT1)
        self.boxTT = wx.BoxSizer(wx.HORIZONTAL)
        self.boxTT.Add(buttonTT0, 1, wx.EXPAND | wx.ALL, 10)
        self.boxTT.Add(buttonTT1, 1, wx.EXPAND | wx.ALL, 10)
        boxMain.Add(self.boxTT                   ,3, 0, 0)
        self.SetSizer(boxMain)
        logging.info("Created Main box")

        if conf.OPTION_FASTSTART:
            self.OpenFrameWorkspace(None, 0)

    # LoadTextCtrl: Load File's path and set to TextCtrl's value
    # Input
    #   t(textCtrl) = textCtrl object
    #   f(str) = file format
    def LoadTextCtrl(self, event, t, f):
        if f == "csv":
            wildcard = "CSV file (*.csv)|*.csv"
            dialog = wx.FileDialog(self, "Open csv File", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        elif f == "ttsave":
            wildcard = "Timetable save file (*.ttsave)|*.ttsave"
            dialog = wx.FileDialog(self, "Open ttsave File", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        else:
            logging.warning("Unrecognized File Format")
        if dialog.ShowModal() == wx.ID_CANCEL:
            return
        path = dialog.GetPath()
        t.SetValue(path)
        logging.info("Set %s to %s"%(str(t),path))
    
    # EmptyTextCtrl: Empties TextCtrl's value
    def EmptyTextCtrl(self, event, targetTextCtrl):
        targetTextCtrl.SetValue("")
        logging.info("Empited %s"%(str(targetTextCtrl)))

    # Create box that contains default load and cancel feature
    def CreateBoxLoadData(self, txt, f="csv"):
        self.fontBasic = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL)
        text = wx.StaticText(self, label=txt,style = wx.ALIGN_RIGHT)
        text.SetFont(self.fontBasic)
        textDir = wx.TextCtrl(self)
        buttonLoad = wx.Button(self, label="Load")
        buttonLoad.Bind(wx.EVT_BUTTON, lambda event: self.LoadTextCtrl(event, textDir, f), buttonLoad)
        buttonCancel = wx.Button(self, label="Cancel")
        buttonCancel.Bind(wx.EVT_BUTTON, lambda event: self.EmptyTextCtrl(event, textDir), buttonCancel)
        
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(text        , 4, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 10)
        box.Add(textDir     , 4, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 10)
        box.Add(buttonLoad  , 2, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 10)
        box.Add(buttonCancel, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 10)
        return box, text, textDir, buttonLoad, buttonCancel
    
    def LoadConfig(self):
        if self.subjectInfoTextCtrl.GetValue() != "":
            self.conf.FILE_SUBJECT_INFO = self.subjectInfoTextCtrl.GetValue()
        if self.studentSurveyTextCtrl.GetValue() != "":
            self.conf.FILE_STUDENT_SURVEY = self.studentSurveyTextCtrl.GetValue()
        if self.instructorSurveyTextCtrl.GetValue() != "":
            self.conf.FILE_INSTRUCTOR_SURVEY = self.instructorSurveyTextCtrl.GetValue()
        if self.classroomInfoTextCtrl.GetValue() != "":
            self.conf.FILE_CLASSROOM_INFO = self.classroomInfoTextCtrl.GetValue()
        
        if self.SubjectInfoTextCtrl.GetValue() != "":
            self.conf.INITIALIZATION_MODE = 1 
            self.conf.FILE_FILE_SAVE = self.subjectInfoTextCtrl.GetValue()
        else:
            self.conf.INITIALIZATION_MODE = 0
        logging.info("Loaded Config")

    def OpenFrameWorkspace(self, event, mode):
        self.conf.SIMULATION_MODE = mode
        if mode == 0:
            logging.info("Opening Workspace Frame With ClassTime Mode")
        else:
            logging.info("Opening Workspace Frame With ExamTime Mode")
        self.f = FrameWorkspace(self.conf)
        self.f.Show()
        self.Close()

