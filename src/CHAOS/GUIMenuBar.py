import wx
import logging

class MenuBarWorkspace(wx.MenuBar):
    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        self.parent = parent

        # Menu
        menuFile = wx.Menu()
        self.Append(menuFile, '파일') # 파일
        newFile = wx.MenuItem(menuFile, wx.ID_FILE, text = "새 시간표", kind = wx.ITEM_NORMAL)
        saveFile = wx.MenuItem(menuFile, wx.ID_SAVE, text = "저장", kind = wx.ITEM_NORMAL)
        loadFile = wx.MenuItem(menuFile, wx.ID_OPEN, text = "불러오기", kind = wx.ITEM_NORMAL)
        quitFile = wx.MenuItem(menuFile, wx.ID_CLOSE, text = "종료", kind = wx.ITEM_NORMAL)
        
        menuAlgorithm = wx.Menu()
        self.Append(menuAlgorithm, '알고리즘') # 알고리즘
        executeAlgorithm = wx.MenuItem(menuAlgorithm, wx.ID_EXECUTE, text = "알고리즘 실행", kind = wx.ITEM_NORMAL)
        
        menuWindow = wx.Menu() 
        self.Append(menuWindow, '창') # 창
        toolWindow = wx.MenuItem(menuWindow, 1, text = "툴바", kind = wx.ITEM_NORMAL) 
        stu_listWindow = wx.MenuItem(menuWindow, 2, text = "학생 목록", kind = wx.ITEM_NORMAL)
        stu_helpWindow = wx.MenuItem(menuWindow, 3, text = "학생 도움말", kind = wx.ITEM_NORMAL)
        stu_infoWindow = wx.MenuItem(menuWindow, 4, text = "학생 정보", kind = wx.ITEM_NORMAL)
        prf_listWindow = wx.MenuItem(menuWindow, 2, text = "교수 목록", kind = wx.ITEM_NORMAL)
        prf_helpWindow = wx.MenuItem(menuWindow, 3, text = "교수 도움말", kind = wx.ITEM_NORMAL)
        prf_infoWindow = wx.MenuItem(menuWindow, 4, text = "교수 정보", kind = wx.ITEM_NORMAL)
        sub_listWindow = wx.MenuItem(menuWindow, 2, text = "과목 목록", kind = wx.ITEM_NORMAL)
        sub_helpWindow = wx.MenuItem(menuWindow, 3, text = "과목 도움말", kind = wx.ITEM_NORMAL)
        sub_infoWindow = wx.MenuItem(menuWindow, 4, text = "과목 정보", kind = wx.ITEM_NORMAL)
        cls_listWindow = wx.MenuItem(menuWindow, 2, text = "교실 목록", kind = wx.ITEM_NORMAL)
        cls_helpWindow = wx.MenuItem(menuWindow, 3, text = "교실 도움말", kind = wx.ITEM_NORMAL)
        cls_infoWindow = wx.MenuItem(menuWindow, 4, text = "교실 정보", kind = wx.ITEM_NORMAL)
        table_showWindow = wx.MenuItem(menuWindow, 5, text = "시간표", kind = wx.ITEM_NORMAL)
        table_numWindow = wx.MenuItem(menuWindow, 6, text = "시간표 표시 형식을 숫자로 변경", kind = wx.ITEM_NORMAL)
        table_letterWindow = wx.MenuItem(menuWindow, 7, text = "시간표 표시 형식을 글자로 변경", kind = wx.ITEM_NORMAL)
        
        menuHelp = wx.Menu()
        self.Append(menuHelp, '도움말') # 도움말
        helpHelp = wx.MenuItem(menuHelp, 2, text = "도움말", kind = wx.ITEM_NORMAL)
        bug_reportHelp = wx.MenuItem(menuHelp, 3, text = "버그 보고", kind = wx.ITEM_NORMAL)
        infoHelp = wx.MenuItem(menuHelp, 4, text = "프로그램 정보", kind = wx.ITEM_NORMAL)
        
        # Menu-File
        menuFileLoad = wx.MenuItem(menuFile, id=  0, text="遺덈윭�삤湲�"
                , helpString="ttsave�뙆�씪�쓣 遺덈윭�샃�땲�떎.")
        menuFileSave = wx.MenuItem(menuFile, id=  1, text="���옣�븯湲�"
                , helpString="ttsave�뙆�씪�쓣 ���옣�빀�땲�떎.")
        menuFileQuit = wx.MenuItem(menuFile, id=  2, text="醫낅즺"
                , helpString="�봽濡쒓렇�옩�쓣 醫낅즺�빀�땲�떎.")
        # parent.Bind(wx.EVT_MENU, parent.on_quit_click, id=wx.ID_EXIT)

        menuFile.Append(newFile)
        menuFile.Append(saveFile)
        menuFile.Append(loadFile)
        menuFile.AppendSeparator()
        menuFile.Append(quitFile)
        
        menuAlgorithm.Append(executeAlgorithm)
        
        menuWindow.Append(toolWindow)
        menuWindow.AppendSeparator()
        menuWindow.Append(stu_listWindow)
        menuWindow.Append(stu_helpWindow)
        menuWindow.Append(stu_infoWindow)
        menuWindow.AppendSeparator()
        menuWindow.Append(prf_listWindow)
        menuWindow.Append(prf_helpWindow)
        menuWindow.Append(prf_infoWindow)
        menuWindow.AppendSeparator()
        menuWindow.Append(sub_listWindow)
        menuWindow.Append(sub_helpWindow)
        menuWindow.Append(sub_infoWindow)
        menuWindow.AppendSeparator()
        menuWindow.Append(cls_listWindow)
        menuWindow.Append(cls_helpWindow)
        menuWindow.Append(cls_infoWindow)
        menuWindow.AppendSeparator()
        menuWindow.Append(table_showWindow)
        menuWindow.Append(table_numWindow)
        menuWindow.Append(table_letterWindow)
        
        menuHelp.Append(helpHelp)
        menuHelp.Append(bug_reportHelp)
        menuHelp.Append(infoHelp)
        
        
        
        
        
        