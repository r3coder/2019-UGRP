
import wx
import wx.lib.scrolledpanel as scrolled

from GUITools import *

from FunctionsTime import *

class PanelTimetableTime(wx.Panel):
    def __init__(self, parent, config, size):
        logging.info("Creating PanelTimetableTime")
        self.parent = parent; self.config = config; self.size = size
        wx.Panel.__init__(self, parent, size=size) # Initial Size

        self.SetBackgroundColour("#DDDDDD") # Temp Background

        self.cfg_h = config.UI_SUBJECT_ITEM_HEIGHT
        self.cfg_w = config.UI_SUBJECT_TIME_WIDTH
        self.cfg_b = config.UI_SUBJECT_ITEM_BORDER
        self.dayIdx = 0
        self.isTimeSelected = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.Update)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
#        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)  

    def OnPaint(self, event):
        self.dc = wx.PaintDC(self)
    
    def Update(self, event=None):
        self.dc = wx.ClientDC(self)
        self.dc.Clear()

        pen = wx.Pen("#000000", 1)
        brush = wx.Brush("#FFFFFF")
        self.dc.SetPen(pen)
        self.dc.SetBrush(brush)

        pen_none = wx.Pen("#000000", 0)
        pen_select = wx.Pen("#000000", 3)
        pen_normal = wx.Pen("#444444", 1)
        brush_blue_light = wx.Brush("#DDDDFF")
        brush_green_light = wx.Brush("#DDFFDD")

        # Drawing Selected Overlay
        x = 0
        try: x = event.GetX()
        except: logging.info("Couldn't find mouse")
        if self.parent.isTimeSelected:
            div = self.cfg_w/2
            width = self.parent.sim.subjects[self.parent.TimeSelectedSubject].timeAssignedSplit[self.parent.TimeSelectedIndex]/60*self.cfg_w
            self.dc.SetPen(pen_none)
            self.dc.SetBrush(brush_blue_light)
            self.dc.DrawRectangle(x//div*div,0,width,self.size[1])
            self.dc.SetPen(pen)
            self.dc.SetBrush(brush_green_light)
            self.dc.DrawRectangle(x//div*div,self.parent.TimeSelectedSubject*(self.cfg_h+self.cfg_b*2)+self.cfg_b,width,self.cfg_h)

        y = 0
        for indsub, sub in enumerate(self.parent.sim.subjects):
            y += self.cfg_b
            for inditem, item in enumerate(sub.timeAssignedTime):
                if item[0] == self.dayIdx and sub.timeIsAssigned[inditem]:
                    if indsub==self.parent.TimeSelectedSubject and inditem==self.parent.TimeSelectedIndex: self.dc.SetPen(pen_select)
                    else:    self.dc.SetPen(pen_normal)
                    self.dc.SetBrush(wx.Brush(sub.StatusTime(inditem)))
                    x = ((item[1]-9)+item[2]/60)*self.cfg_w
                    self.dc.DrawRectangle(x,y,self.cfg_w*sub.timeAssignedSplit[inditem]/60,self.cfg_h)
                    self.dc.DrawText("%s"%sub.timeAssignedClassroom[inditem], x+5, y+5)
            y += self.cfg_h+self.cfg_b

    def OnRightDown(self, event):
        x = 0; y = 0
        x = event.GetX()
        y = event.GetY()
        xInd = x//(self.cfg_w/2)
        if y%(self.cfg_h+self.cfg_b*2) > self.cfg_b and y%(self.cfg_h+self.cfg_b*2) < self.cfg_b+self.cfg_h:
            yInd = y//(self.cfg_h+self.cfg_b*2)
        tm = (self.dayIdx,int((xInd//2)+9),int((xInd%2)*30))
        if self.parent.isTimeSelected:
            self.parent.isTimeSelected = False
            self.parent.TimeSelectedSubject = -1
            self.parent.TimeSelectedIndex = -1
        else:
            idx = -1
            for i in range(len(self.parent.sim.subjects[yInd].timeIsAssigned)):
                t = self.parent.sim.subjects[yInd].timeAssignedTime[i]
                tt = (t[0],t[1],t[2],self.parent.sim.subjects[yInd].timeAssignedSplit[i])
                if IsTimeInDuration(tm,tt):
                    idx = i; break
            if idx != -1 and self.parent.sim.subjects[yInd].timeIsFixed[idx]==False:
                self.parent.sim.RemoveSubjectTime(yInd,idx)
        
        self.dc.Clear()
        self.parent.Update(event)

    def OnLeftDown(self, event):
        x = 0; y = 0
        x = event.GetX()
        y = event.GetY()
        xInd = x//(self.cfg_w/2)
        if y%(self.cfg_h+self.cfg_b*2) > self.cfg_b and y%(self.cfg_h+self.cfg_b*2) < self.cfg_b+self.cfg_h:
            yInd = y//(self.cfg_h+self.cfg_b*2)
        tm = (self.dayIdx,int((xInd//2)+9),int((xInd%2)*30))
        if self.parent.isTimeSelected:
            self.parent.sim.AssignSubjectToTime(self.parent.TimeSelectedSubject,self.parent.TimeSelectedIndex,tm,force=True)
            self.parent.isTimeSelected = False
            self.parent.TimeSelectedSubject = -1
            self.parent.TimeSelectedIndex = -1
        else:
            idx = -1
            for i in range(len(self.parent.sim.subjects[yInd].timeIsAssigned)):
                t = self.parent.sim.subjects[yInd].timeAssignedTime[i]
                tt = (t[0],t[1],t[2],self.parent.sim.subjects[yInd].timeAssignedSplit[i])
                if IsTimeInDuration(tm,tt):
                    idx = i; break
            if idx != -1 and self.parent.sim.subjects[yInd].timeIsFixed[idx]==False:
                self.parent.TimeSelectedSubject = yInd
                self.parent.TimeSelectedIndex = idx
                self.parent.isTimeSelected = True
                logging.info("PanelTimetableSelect: Subject %d, Index %d"%(self.parent.TimeSelectedSubject,self.parent.TimeSelectedIndex))


        self.dc.Clear()
        self.parent.Update(event)

class PanelTimetableSelect(wx.Panel):
    def __init__(self, parent, config, size):
        logging.info("Creating PanelTimetableSelect")
        self.parent = parent; self.config = config; self.size = size
        wx.Panel.__init__(self, parent, size=size) # Initial Size

        self.SetBackgroundColour("#DDDDDD") # Temp Background
        self.cfg_h = config.UI_SUBJECT_ITEM_HEIGHT
        self.cfg_w = config.UI_SUBJECT_SELECT_WIDTH
        self.cfg_b = config.UI_SUBJECT_ITEM_BORDER
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.Update)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
#        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

    def OnRightDown(self, event):
        if self.parent.isTimeSelected:
            self.parent.isTimeSelected = False
            self.parent.TimeSelectedSubject = -1
            self.parent.TimeSelectedIndex = -1
        else:
            x = event.GetX()
            y = event.GetY()
            if x%(self.cfg_w+self.cfg_b*2) > self.cfg_b and x%(self.cfg_w+self.cfg_b*2) < self.cfg_b+self.cfg_w:
                xInd = x//(self.cfg_w+self.cfg_b*2)
            if y%(self.cfg_h+self.cfg_b*2) > self.cfg_b and y%(self.cfg_h+self.cfg_b*2) < self.cfg_b+self.cfg_h:
                yInd = y//(self.cfg_h+self.cfg_b*2)
            if len(self.parent.sim.subjects[yInd].timeIsAssigned) > xInd and self.parent.sim.subjects[yInd].timeIsFixed[xInd]==False:
                self.parent.sim.RemoveSubjectTime(yInd,xInd)
        
        self.dc.Clear()
        self.parent.Update(event)

    def OnLeftDown(self, event):
        if self.parent.isTimeSelected:
            self.parent.isTimeSelected = False
            self.parent.TimeSelectedSubject = -1
            self.parent.TimeSelectedIndex = -1
        else:
            x = event.GetX()
            y = event.GetY()
            if x%(self.cfg_w+self.cfg_b*2) > self.cfg_b and x%(self.cfg_w+self.cfg_b*2) < self.cfg_b+self.cfg_w:
                xInd = x//(self.cfg_w+self.cfg_b*2)
            if y%(self.cfg_h+self.cfg_b*2) > self.cfg_b and y%(self.cfg_h+self.cfg_b*2) < self.cfg_b+self.cfg_h:
                yInd = y//(self.cfg_h+self.cfg_b*2)

            if len(self.parent.sim.subjects[yInd].timeIsAssigned) > xInd and self.parent.sim.subjects[yInd].timeIsFixed[xInd]==False:
                self.parent.TimeSelectedSubject = yInd
                self.parent.TimeSelectedIndex = xInd
                self.parent.isTimeSelected = True
                logging.info("PanelTimetableSelect: Subject %d, Index %d"%(self.parent.TimeSelectedSubject,self.parent.TimeSelectedIndex))
            
        self.dc.Clear()
        self.parent.Update(event)

    def OnPaint(self, event):
        self.dc = wx.PaintDC(self)

    def Update(self, event=None):
        self.dc = wx.ClientDC(self)
        self.dc.Clear()
        pen_select = wx.Pen("#000000", 3)
        pen_normal = wx.Pen("#444444", 1)

        y = 0
        for indsub, sub in enumerate(self.parent.sim.subjects):
            y += self.cfg_b
            x = 0
            for inditem, item in enumerate(sub.timeIsAssigned):
                if indsub==self.parent.TimeSelectedSubject and inditem==self.parent.TimeSelectedIndex: self.dc.SetPen(pen_select)
                else:    self.dc.SetPen(pen_normal)
                self.dc.SetBrush(wx.Brush(sub.StatusTime(inditem)))
                self.dc.DrawRectangle(x,y,self.cfg_w,self.cfg_h)
                self.dc.DrawText("%d"%sub.timeAssignedSplit[inditem], x+5, y+5)
                x += self.cfg_w+self.cfg_b
            y += self.cfg_h+self.cfg_b

        # x = event.GetX()
        # y = event.GetY()
            


class PanelTimetableScroll(scrolled.ScrolledPanel):
    def __init__(self, parent, config, sim):
        self.parent = parent; self.config = config; self.sim = sim
        logging.info("Creating TimetableScroll")
        self.col_bg = config.UI_SUBJECT_COL_BG
        self.col_line = config.UI_SUBJECT_COL_LINE
        self.cfg_item_height = config.UI_SUBJECT_ITEM_HEIGHT
        self.cfg_item_border = config.UI_SUBJECT_ITEM_BORDER
        

        scrolled.ScrolledPanel.__init__(self, parent, -1, size=(1000,800-20))
        self.infoIdx = -1; self.mode = "subject"
        self.SetBackgroundColour(config.UI_SUBJECT_COL_BG)
        
        self.isTimeSelected = False
        self.TimeSelectedSubject = -1
        self.TimeSelectedIndex = -1
        
        boxMain = wx.BoxSizer(wx.HORIZONTAL)
        boxSubjects = wx.BoxSizer(wx.VERTICAL)
        self.buttonsSub = list()
        for s in sim.subjects:
            b = ButtonAdvanced(self, s, str(s.infoName), OpenEdit, ShowInfo
                    ,200, self.cfg_item_height, self.cfg_item_border)
            self.buttonsSub.append(b)
            boxSubjects.Add(b,0,wx.ALL,self.cfg_item_border)

        boxMain.Add(boxSubjects)
        
        boxMain.Add(wx.StaticLine(self, -1, size=(1, len(sim.subjects)*(self.cfg_item_height+self.cfg_item_border*2)-10)), 0, wx.ALL, 3)
        
        self.panelTimetableSelect = PanelTimetableSelect(self, self.config, (160+3,len(sim.subjects)*(self.cfg_item_height+self.cfg_item_border*2)))
        boxMain.Add(self.panelTimetableSelect)
        
        boxMain.Add(wx.StaticLine(self, -1, size=(1, len(sim.subjects)*(self.cfg_item_height+self.cfg_item_border*2)-10)), 0, wx.ALL, 3)

        self.panelTimetableTime = PanelTimetableTime(self, self.config, (680,len(sim.subjects)*(self.cfg_item_height+self.cfg_item_border*2)))
        boxMain.Add(self.panelTimetableTime)        
        
        self.SetSizer(boxMain)
        
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_MOTION, self.Update)
        self.SetupScrolling()
        self.UpdatePanel()
    
    def OnResize(self, event):
        self.Layout()
    
    def Update(self, event=None):
        self.panelTimetableSelect.Update(event)
        self.panelTimetableTime.Update(event)

    def UpdatePanel(self):
        for ind, but in enumerate(self.buttonsSub):
            but.SetBackgroundColour(self.sim.subjects[ind].Status())

class PanelTimetable(wx.Panel):
    def __init__(self, parent, config, sim):
        self.parent = parent; self.config = config; self.sim = sim
        logging.info("Creating Timetable")
        wx.Panel.__init__(self, parent, size=(1100-20,850))

        boxMain = wx.BoxSizer(wx.VERTICAL)
        self.Layout()
        #Button Boxes
        self.boxButtonsWeek = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonsWeek = list()
        b0 = wx.Button(self,label="월",size=(self.GetSize()[0]/5,30), style=wx.BORDER_MASK)
        b0.Bind(wx.EVT_LEFT_DOWN, lambda event: self.SetWeekIdx(0), b0)
        b1 = wx.Button(self,label="화",size=(self.GetSize()[0]/5,30), style=wx.BORDER_MASK)
        b1.Bind(wx.EVT_LEFT_DOWN, lambda event: self.SetWeekIdx(1), b1)
        b2 = wx.Button(self,label="수",size=(self.GetSize()[0]/5,30), style=wx.BORDER_MASK)
        b2.Bind(wx.EVT_LEFT_DOWN, lambda event: self.SetWeekIdx(2), b2)
        b3 = wx.Button(self,label="목",size=(self.GetSize()[0]/5,30), style=wx.BORDER_MASK)
        b3.Bind(wx.EVT_LEFT_DOWN, lambda event: self.SetWeekIdx(3), b3)
        b4 = wx.Button(self,label="금",size=(self.GetSize()[0]/5,30), style=wx.BORDER_MASK)
        b4.Bind(wx.EVT_LEFT_DOWN, lambda event: self.SetWeekIdx(4), b4)
        self.buttonsWeek.append(b0); self.buttonsWeek.append(b1); self.buttonsWeek.append(b2); self.buttonsWeek.append(b3); self.buttonsWeek.append(b4)
        self.boxButtonsWeek.Add(b0); self.boxButtonsWeek.Add(b1); self.boxButtonsWeek.Add(b2); self.boxButtonsWeek.Add(b3); self.boxButtonsWeek.Add(b4); 

        boxMain.Add(self.boxButtonsWeek)
        
        boxMain.Add(wx.StaticLine(self, -1, size=(1000, 1)), 0, wx.ALL, 3)
    
        # Labels
        self.boxButtonsLabel = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonsLabel = (
            wx.Button(self,label="과목 이름",size=(200,20), style=wx.BORDER_MASK),
            wx.Button(self,label="시간 구분",size=(160,20), style=wx.BORDER_MASK),
            wx.Button(self,label="시간표",size=(680,20), style=wx.BORDER_MASK))
        for b in self.buttonsLabel:
            b.SetBackgroundColour("#FFFFFF")
        self.boxButtonsLabel.AddMany(self.buttonsLabel)
        boxMain.Add(self.boxButtonsLabel)

        # Timetable Scroller
        self.panelTimetableScroll = PanelTimetableScroll(self, config, sim)
        boxMain.Add(self.panelTimetableScroll,0,wx.EXPAND)

        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_SCROLL, self.OnScroll)
        self.SetSizerAndFit(boxMain)
        
        self.panelTimetableScroll.Update()
        self.panelTimetableScroll.panelTimetableTime.Update()

    def SetWeekIdx(self, idx):
        logging.info("Timetable: Set week idx to %d"%idx)
        self.panelTimetableScroll.panelTimetableTime.dayIdx = idx
        self.panelTimetableScroll.Update()
        self.panelTimetableScroll.panelTimetableTime.Update()

    def OnScroll(self, event):  
        # self.panelTimetableScroll.panelTimetableSelect.dc.Clear()
        self.Layout()

    def OnResize(self, event):
        self.Layout()

    def UpdatePanel(self):
        pass
