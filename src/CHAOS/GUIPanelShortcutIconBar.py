import wx
import wx.lib.scrolledpanel as scrolled


class PanelShortcutIconBar(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1, size=(300,50))

        self.SetBackgroundColour((255,255,255))

        button00 = wx.Button(self, -1, label="00",size=(50,50))
        button01 = wx.Button(self, -1, label="01",size=(50,50))
        button02 = wx.Button(self, -1, label="02",size=(50,50))
        button03 = wx.Button(self, -1, label="03",size=(50,50))
        button04 = wx.Button(self, -1, label="04",size=(50,50))
        button05 = wx.Button(self, -1, label="05",size=(50,50))

        s = wx.BoxSizer(wx.HORIZONTAL)
        s.Add(button00, 0, 0, 0)
        s.Add(button01, 0, 0, 0)
        s.Add(button02, 0, 0, 0)
        s.Add(button03, 0, 0, 0)
        s.Add(button04, 0, 0, 0)
        s.Add(button05, 0, 0, 0)
        self.SetSizer(s)