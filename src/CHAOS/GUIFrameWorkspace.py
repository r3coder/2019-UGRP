import wx
import wx.lib.scrolledpanel as scrolled
import logging

from Simulation import Simulation
from Data import *

from GUIMenuBar import MenuBarWorkspace
from GUIPanelShortcutIconBar import PanelShortcutIconBar
from GUIPanelItem import PanelItem
from GUIPanelTimetable import PanelTimetable
from GUITools import *
from GUITools import BoxStaticText

class PanelInfo(scrolled.ScrolledPanel):
    def __init__(self, parent, config, sim):
        self.parent = parent; self.config = config; self.sim = sim
        scrolled.ScrolledPanel.__init__(self, parent, -1, size=(400,500))
        boxMain = wx.BoxSizer(wx.HORIZONTAL)
        boxMain.Add(PanelItem(self, config, sim.students, "student"), 1, wx.EXPAND)
        boxMain.Add(wx.StaticLine(self, -1, size=(1, -1)), 0, wx.ALL, 5)
        boxMain.Add(PanelItem(self, config, sim.instructors, "instructor"), 1, wx.EXPAND)
        self.SetSizerAndFit(boxMain)
        self.SetupScrolling()

class PanelLeft(scrolled.ScrolledPanel):
    def __init__(self, parent, config, sim):
        scrolled.ScrolledPanel.__init__(self, parent, -1, size=(400,500))
        boxMain = wx.BoxSizer(wx.VERTICAL)
        boxMain.Add(PanelShortcutIconBar(self), 0, wx.EXPAND)
        boxMain.Add(wx.StaticLine(self, -1, size=(-1, 1)), 0, wx.ALL, 5)
        boxMain.Add(PanelInfo(self, config, sim),1,wx.EXPAND,0)
        self.parent = parent
        self.SetSizerAndFit(boxMain)
        self.SetupScrolling()

class PanelWorkspace(scrolled.ScrolledPanel):
    def __init__(self, parent, config, sim):
        scrolled.ScrolledPanel.__init__(self, parent, -1, size=(1600,900))
        self.SetBackgroundColour("#FFFFFF")
        boxMain = wx.BoxSizer(wx.HORIZONTAL)
        boxMain.Add(PanelLeft(self, config, sim), 5, wx.EXPAND)
        boxMain.Add(wx.StaticLine(self, -1, size=(1, 800)), 0.1, wx.ALL, 5)
        boxMain.Add(PanelTimetable(self, config, sim), 11, wx.EXPAND)
        self.parent = parent
        self.SetSizerAndFit(boxMain)
        self.SetupScrolling()

class FrameWorkspace(wx.Frame):
    def __init__(self, config):
        wx.Frame.__init__(self, None, title = "Timetable Editor / Simulator v%s"%config.VERSION, size = (config.UI_WORKSPACE_WIDTH, config.UI_WORKSPACE_HEIGHT))
        
        self.SetMinSize((1600,900))
        self.config = config
        self.width = self.GetSize()[0]
        self.height = self.GetSize()[1]

        # Set menu bar
        self.SetMenuBar(MenuBarWorkspace(self))

        # Simulation Setup
        self.s = Simulation(config)
        # LoadSubjectInfo(self.s, config.FILE_SUBJECT_INFO)
        # LoadStudentSurvey(self.s, config.FILE_STUDENT_SURVEY)
        # LoadInstructorSurvey(self.s, config.FILE_INSTRUCTOR_SURVEY)
        # LoadClassroomInfo(self.s, config.FILE_CLASSROOM_INFO)
        if config.OPTION_LOADMODE:
            logging.info("Load mode") 
            self.s.Load()
        else:
            logging.info("Execute Mode") 
            # self.s.Execute()

        # Set Main Panel
        p = PanelWorkspace(self, config, self.s)

        self.Show()
