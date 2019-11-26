import wx

class HelloFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(HelloFrame, self).__init__(*args, **kwargs)

        pnl = wx.Panel(self)

        st = wx.StaticText(pnl, label = 'Hello')
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(st, wx.SizerFlags().Border(wx.TOP|wx.LEFT, 25))
        pnl.SetSizer(sizer)

        self.makeMenuBar()

        self.CreateStatusBar()
        self.SetStatusText('welcome')

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H", "Help string shown in status bar for this menu item")

        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(helpMenu, '&Help')

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnHello(self, event):
        self.Close(True)

    def OnExit(self, event):
        wx.MessageBox('Hello again')

    def OnAbout(self, event):
        wx.MessageBox('This is wxPython', 'About hello 2', wx.OK|wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App()
    frm = HelloFrame(None, title = 'Hello')
    frm.Show()
    app.MainLoop()
