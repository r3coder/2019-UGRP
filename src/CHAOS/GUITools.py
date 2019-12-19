import wx
import logging
from GUIFrameEdit import FrameEdit

def OpenEdit(self, item):
    if self.mode=="student": logging.info("Editing Student Info #%d"%item.idx)
    elif self.mode=="instructor": logging.info("Editing Instructor Info #%d"%item.idx)
    elif self.mode=="subject": logging.info("Editing Subject Info #%d"%item.idx)
    try: self.frameEdit.Close()
    except: logging.info("self.frameEdit wasn't possible to close.")
    self.frameEdit = FrameEdit(self, self.config, item, self.mode)
    self.frameEdit.Show()

def ShowInfo(self, item):
    if self.mode=="student": logging.info("Showing Student Info #%d"%item.idx)
    elif self.mode=="instructor": logging.info("Showing Instructor Info #%d"%item.idx)
    elif self.mode=="subject": logging.info("Showing Subject Info #%d"%item.idx)
    self.parent.infoIdx = item.idx
    self.UpdatePanel()
    self.parent.UpdatePanel()

# BoxStaticText: Create Button with basic functions
def ButtonAdvanced(self, obj, text, funcLd, funcL, boxW=10, boxH=10, boxB=0):
    bw = self.GetSize()[0]/(int(self.GetSize()[0]/(boxW+boxB*2))+1)-boxB*2
    b = wx.Button(self,label=text,size=(bw,boxH), style=wx.BORDER_MASK)
    b.Bind(wx.EVT_LEFT_DCLICK, lambda event: funcLd(self, obj), b)
    b.Bind(wx.EVT_LEFT_DOWN  , lambda event: funcL (self, obj), b)
    return b

# BoxStaticText: Create Box with Static Text
def BoxStaticText(self, text, style=wx.ALIGN_CENTRE, fontSize=9):
    textHelp = wx.StaticText(self,label=text
            ,style=style, size=(self.GetSize()[0],-1))
    fontHelp = wx.Font(fontSize, wx.MODERN, wx.NORMAL, wx.NORMAL)
    textHelp.SetFont(fontHelp)
    boxHelp = wx.BoxSizer(wx.HORIZONTAL)
    boxHelp.Add(textHelp, flag = wx.LEFT | wx.RIGHT, border=10)
    return boxHelp


