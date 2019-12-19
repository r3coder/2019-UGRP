import wx
import logging



class FrameEdit(wx.Frame):
    def __init__(self, parent, config, item, mode):
        wx.Frame.__init__(self, parent, size=(600,400))
        self.parent = parent
        self.SetBackgroundColour("#6666FF")
        
        textInfo = wx.StaticText(self,label="myid:%d"%item.idx
                ,style=wx.ALIGN_CENTRE, size=(self.GetSize()[0],-1))
        fontHelp = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL)
        textInfo.SetFont(fontHelp)
        
        self.config = config
        self.mode = mode
        self.item = item
        
        self.boxMain = wx.BoxSizer(wx.VERTICAL)
        self.boxMain.Add(textInfo)
        self.boxSubList = wx.BoxSizer(wx.VERTICAL)
        
        if self.mode == "student":
            self.s = self.parent.parent.parent.parent.parent.parent.s # Get Already-exist simulation result from GUIFrameWorkspace
            
            
            self.subjectList = self.item.GetLeftSubjects1st() + self.item.GetLeftSubjects2nd() # Add all students subjects; both mandatory and selective
            self.temporarySubList = self.subjectList
            
            for sub in self.subjectList:
                self.boxList = wx.BoxSizer(wx.HORIZONTAL)
                text = self.s.subjects[sub].infoName
                textHelp = wx.StaticText(self,label=text, size=(250,-1))
                buttonAdd = self.ButtonAdd()
                buttonDelete = self.ButtonDelete()
                self.boxList.Add(textHelp, proportion = 1, flag = wx.ALL, border = 5)
                self.boxList.Add(buttonAdd, proportion = 1, flag = wx.ALL, border = 5)
                self.boxList.Add(buttonDelete, proportion = 1, flag = wx.ALL, border = 5)
                self.boxSubList.Add(self.boxList)
        
        elif self.mode == "instructor":
            self.s = self.parent.parent.parent.parent.parent.parent.s # Get Already-exist simulation result from GUIFrameWorkspace
            print("instructor")
        
        else:
            self.s = self.parent.parent.parent.parent.s # Get Already-exist simulation result from GUIFrameWorkspace
            print("subject")
            
         
        self.boxMain.Add(self.boxSubList)
        
        self.boxButton = wx.BoxSizer(wx.HORIZONTAL)
        self.boxButton.Add(self.ButtonEdit(), flag = wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, border = 10)
        self.boxButton.Add(self.ButtonSave(), flag = wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, border = 10)
        
        self.boxMain.Add(self.boxButton, flag = wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND|wx.ALIGN_RIGHT, border = 10)
            
        self.SetSizer(self.boxMain)
        
    def ButtonEdit(self):
        b = wx.Button(self, label = "Edit", size = (200, 20))
        return b
    
    def ButtonSave(self):
        b = wx.Button(self, label = "Save", size = (200, 20))
        b.Bind(wx.EVT_BUTTON, self.SaveList)
        return b
        
    def ButtonAdd(self):
        b = wx.Button(self, label = "+", size = (20, 20))
        b.Bind(wx.EVT_BUTTON, self.AddSubject)
        return b
    
    def ButtonDelete(self):
        b = wx.Button(self, label = "-", size = (20, 20))
        b.Bind(wx.EVT_BUTTON, self.DeleteSubject)
        return b
    
    def AddSubject(self, event):
        frame = self.AddWindow(self)
        #frame = self.AddWindow(self.s, self.temporarySubList)
        frame.Show()
    
    def DeleteSubject(self, event):
        btn = event.GetEventObject().GetPosition()
        delbox = 0
        index = 0
        for box in self.boxSubList.GetChildren():
            box.SetId(index)
            index += 1
        for box in self.boxSubList.GetChildren():
            tar = box.GetSizer().GetItem(2).GetPosition()
            if tar - btn == (-5, -5):
                self.boxSubList.Hide(delbox)
                self.boxSubList.Remove(delbox)
                self.temporarySubList.pop(delbox)
            else:
                delbox += 1 
                
        self.boxSubList.Layout()
        
    def SaveList(self, event):
        self.item.subject1st = self.temporarySubList
        self.item.subject2nd = []

# Functions for the AddWindow

                
    def AddList(self, sub):
        self.temporarySubList.append(sub.idx)
        print(self.temporarySubList)
                
                
    class AddWindow(wx.Frame):
        def __init__(self, parent):
            self.parent = parent
            #self.s = s
            #self.list = list
            
            wx.Frame.__init__(self, None, title = "Add Subject", size = (400, 300))
            self.SetBackgroundColour("#66FFFF")
            self.boxMain = wx.BoxSizer(wx.VERTICAL)
            
            self.textSearch = wx.TextCtrl(self, size = (200, 20))
            self.textSearch.Bind(wx.EVT_TEXT_ENTER, self.SearchSubject)
            self.boxMain.Add(self.textSearch, flag = wx.ALL, border = 10)
            
            self.SetSizer(self.boxMain)    
            
        def SearchSubject(self, event):
            command = self.textSearch.GetValue()
            self.textSearch.Clear()
            for item in self.boxMain.GetChildren():
                if item.IsSizer():
                    self.boxMain.Remove(item)
            
            self.boxMain.Layout()
            
            for sub in self.parent.s.subjects:
                if command in sub.infoName:
                    self.boxList = wx.BoxSizer(wx.VERTICAL)
                    self.boxSub = wx.BoxSizer(wx.HORIZONTAL)
                    txtInfo = wx.StaticText(self, label = sub.infoName, size=(250,-1))
                    btnAdd = wx.Button(self, label = "Add", size = (200, 20))
                    btnAdd.Bind(wx.EVT_BUTTON, lambda event : self.parent.AddList(sub))
                    btnAdd.Bind(wx.EVT_BUTTON, self.onClose)
                    self.boxSub.Add(txtInfo, flag = wx.ALL, border = 5)
                    self.boxSub.Add(btnAdd, flag = wx.ALL|wx.EXPAND, border = 5)
                    self.boxMain.Add(self.boxSub, flag = wx.ALL, border = 5)
                    
                    self.boxMain.Layout()
                     
                    print(sub.infoName)
                    
        def onClose(self, event):
            self.Close(True)
