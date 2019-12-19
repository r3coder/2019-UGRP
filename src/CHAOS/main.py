
import logging
logging.basicConfig(
        format="%(asctime)-15s [%(levelname)s] %(funcName)s: %(message)s", level=logging.INFO)

import wx

from Simulation import Simulation
from Student import Student
from Subject import Subject
from Instructor import Instructor
from Classroom import Classroom
from SimulationExecute import Slot
from GUIFrameInitiate import FrameInitiate
from GUIFrameWorkspace import FrameWorkspace

# Argparse
import argparse
def str2bool(v):
    if v.lower() in ["true", "t", "1"]: return True
    elif v.lower() in ["false", "f", "0"]: return False
    else: raise argparse.ArgumentTypeError("Not Boolean value")

parser = argparse.ArgumentParser()
parser.add_argument("-gui","--gui", type=str2bool, default=False,
        help = "Turn on GUI?")
'''
parser.add_argument("-i","--int", type=int, choices=[0,1,2], default=1,
        help = "Integer with choices")
parser.add_argument("-sb","--str2bool", type=str2bool, default=False,
        help = "String to Bool")
parser.add_argument("-s","--string", type=str, default = "",
        help = "String")
'''

args = parser.parse_args()


class config:
    VERSION = "0.1"
    F_INIT_WIDTH = 900
    F_INIT_HEIGHT = 600
    FILE_STUDENT_SURVEY = "../data/2019Fall/19FallStudentSurvey_CompletedOnly.csv"
    FILE_SUBJECT_INFO = "../data/2019Fall/19FallSubjectInfo.csv"
    FILE_INSTRUCTOR_SURVEY = "../data/2019Fall/19FallInstructorSurvey.csv"
    FILE_CLASSROOM_INFO = "../data/Classroom.csv"
    FILE_SAVE = ""
    INITIALIZATION_MODE = 0 # 0 - Basic, 1 - Save

    # OPTION_FASTSTART = True
    OPTION_LOADMODE = False
    
    SIM_SLOTS=[None,
    Slot("simple",
        [90, 90],
        [(0,2),(0,3),(1,3),(1,4),(2,4)],
        [( 9, 0),(10,30),(13, 0),(14,30),(16, 0)]), # 90,90
    Slot("simple",
        [120],
        [(0),(1),(2),(3),(4)],
        [(10, 0),(12,30),(14,30),(16, 0),(19, 0)]), # 120
    Slot("simple",
        [180],
        [(0),(1),(2),(3),(4)],
        [( 9, 0),(13, 0),(15, 0),(17, 0),(19, 0)]), # 180
    Slot("simple",
        [240],
        [(0),(1),(2),(3),(4)],
        [(13, 0),(19, 0)]), # 240
    Slot("simple",
        [60],
        [(0),(1),(2),(3),(4)],
        [(11, 0), (13, 0),(19, 0)]) # 60
    ]
    SIM_SAVE_DURATION = 30
    SIM_SLOT_MAX = 1


    UI_SCROLLBAR_WIDTH = 25

    UI_WORKSPACE_WIDTH = 1600
    UI_WORKSPACE_HEIGHT = 900


    UI_STUDENT_COL_BG         = "#FDDFDF"
    UI_STUDENT_COL_LINE       = "#7E6F6F"
    UI_STUDENT_ITEM_WIDTH     = 40
    UI_STUDENT_ITEM_HEIGHT    = 25
    UI_STUDENT_ITEM_BORDER    = 1

    UI_INSTRUCTOR_COL_BG      = "#DEFDE0"
    UI_INSTRUCTOR_COL_LINE    = "#6F7E78"
    UI_INSTRUCTOR_ITEM_WIDTH  = 60
    UI_INSTRUCTOR_ITEM_HEIGHT = 25
    UI_INSTRUCTOR_ITEM_BORDER = 1

    UI_SUBJECT_COL_BG         = "#DEF3FD"
    UI_SUBJECT_COL_LINE       = "#6F7A7E"
    UI_SUBJECT_ITEM_HEIGHT    = 25
    UI_SUBJECT_ITEM_BORDER    = 1
    UI_SUBJECT_SELECT_WIDTH   = 40
    UI_SUBJECT_TIME_WIDTH     = 60

    UI_TIMETABLE_COL_BG       = "#FDDEFD"

if __name__ == "__main__": 
    conf = config()
    logging.info("Program initiated")
    if args.gui:
        a = wx.App()
        f = FrameWorkspace(conf)
        f.Show()
        a.MainLoop()
    s = Simulation(conf)
    s.CUI()