
import wx
import wx.lib.scrolledpanel as scrolled
import logging

from GUITools import *

class PanelItemScroll(scrolled.ScrolledPanel):
    def __init__(self, parent, config, items, mode):
        self.parent = parent; self.config = config; self.items = items; self.mode = mode
        if   mode == "student":
            self.cfg_item_width = config.UI_STUDENT_ITEM_WIDTH
            self.cfg_item_height = config.UI_STUDENT_ITEM_HEIGHT
            self.cfg_item_border = config.UI_STUDENT_ITEM_BORDER
        elif mode == "instructor":
            self.cfg_item_width = config.UI_INSTRUCTOR_ITEM_WIDTH
            self.cfg_item_height = config.UI_INSTRUCTOR_ITEM_HEIGHT
            self.cfg_item_border = config.UI_INSTRUCTOR_ITEM_BORDER
            
        scrolled.ScrolledPanel.__init__(self, parent, -1, size=(200,100))

        # Add Buttons into Lines
        self.buttonsItem = list()
        for s in self.items:
            b = ButtonAdvanced(self, s, str(s.infoName), OpenEdit, ShowInfo
                    ,self.cfg_item_width, self.cfg_item_height, self.cfg_item_border)
            self.buttonsItem.append(b)
        
        self.SetupScrolling()
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.UpdatePanel()
    
    def OnResize(self, event):
        boxStatus = wx.BoxSizer(wx.VERTICAL)
        boxLine = wx.BoxSizer(wx.HORIZONTAL)
        n = (self.GetSize()[0]-self.config.UI_SCROLLBAR_WIDTH)//(self.cfg_item_width+self.cfg_item_border*2)
        for i, b in enumerate(self.buttonsItem):
            b.SetMinSize(((self.GetSize()[0]-self.config.UI_SCROLLBAR_WIDTH)/n-1,self.cfg_item_height))
            boxLine.Add(b,0,wx.ALL|wx.EXPAND,self.cfg_item_border)
            if i%n == n-1:
                boxStatus.Add(boxLine); boxLine = wx.BoxSizer(wx.HORIZONTAL)
        boxStatus.Add(boxLine)
        self.SetSizer(boxStatus)
        self.Layout()
    
    def UpdatePanel(self):
        if self.mode=="student": logging.info("Updating PanelBasic: Student")
        elif self.mode=="instructor": logging.info("Updating PanelBasic: Instructor")
        for ind, but in enumerate(self.buttonsItem):
            but.SetBackgroundColour(self.items[ind].Status())

class PanelItem(wx.Panel):
    def __init__(self, parent, config, items, mode):
        self.parent = parent; self.config = config; self.items = items; self.mode = mode
        if  mode == "student":
            logging.info("Creating PanelBasic: Student")
            self.col_bg = config.UI_STUDENT_COL_BG
            self.col_line = config.UI_STUDENT_COL_LINE
            self.help_text = "색 범례\n빨강:필수과목 충돌\n주황:필수과목 미반영\n노랑:선택과목 미반영\n초록:문제 없음"
            self.base_text = "학생 정보 표시\n학생을 선택해 주세요."
        elif mode == "instructor":
            logging.info("Creating PanelBasic: Instructor")
            self.col_bg = config.UI_INSTRUCTOR_COL_BG
            self.col_line = config.UI_INSTRUCTOR_COL_LINE
            self.help_text = "색 범례\n빨강: 수업시간 충돌 발생\n노랑: 수업시간 미배정\n초록: 문제 없음"
            self.base_text = "교수 정보 표시\n교수를 선택해 주세요."

        wx.Panel.__init__(self, parent, size=(200,100))
        self.infoIdx = -1

        self.SetBackgroundColour(self.col_bg)
        boxMain = wx.BoxSizer(wx.VERTICAL)
        # Item Scroller
        self.panelItemScroll = PanelItemScroll(self, self.config, self.items, self.mode)
        boxMain.Add(self.panelItemScroll          ,6,wx.EXPAND)
        boxMain.Add(wx.StaticLine(self, -1, size=(self.GetSize()[0], -1)), 0, wx.ALL, 5)
        boxMain.Add(BoxStaticText(self, self.help_text),1,wx.EXPAND)
        boxMain.Add(wx.StaticLine(self, -1, size=(self.GetSize()[0], -1)), 0, wx.ALL, 5)
        self.textInfo = wx.StaticText(self, style=wx.ST_NO_AUTORESIZE, size=(self.GetSize()[0], -1), label="교수 정보 표시\n교수를 선택해 주세요.")
        boxMain.Add(self.textInfo,3,wx.EXPAND)
        self.SetSizerAndFit(boxMain)

        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.UpdatePanel()
    
    def OnResize(self, event):
        self.Layout()

    def UpdatePanel(self):

        if self.infoIdx >= 0:
            # Updating instructor info
            if self.mode == "instructor":
                inst = self.items[self.infoIdx]
                s = "교수 #%d, 이름:%s"%(inst.idx,inst.infoName)
                s0 = "배정 완료된 과목:"
                for v in inst.subjectAssign:
                    s0+=self.parent.sim.subjects[v].infoName + ", "
                s1 = "배정된 과목:"
                for v in inst.subjectEnroll:
                    s1+=self.parent.sim.subjects[v].infoName + ", "
                self.textInfo.SetLabel(s+"\n\n"+s0+"\n\n"+s1)
            # Updating student info
            elif self.mode == "student":
                stu = self.items[self.infoIdx]
                s = "학생 #%d, ID:%d"%(stu.idx,stu.infoId)
                s0 = "수강배정된 과목:"
                for v in stu.subjectAssign:
                    s0+=self.parent.sim.subjects[v].infoName + ", "
                s1 = "수강 필수 과목:"
                for v in stu.subject1st:
                    s1+=self.parent.sim.subjects[v].infoName + ", "
                s2 = "수강 선택 과목:"
                for v in stu.subject2nd:
                    s2+=self.parent.sim.subjects[v].infoName + ", "
                self.textInfo.SetLabel(s+"\n\n"+s0+"\n\n"+s1+"\n\n"+s2)
