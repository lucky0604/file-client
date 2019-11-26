import wx
import os, shutil


class MyTextDropTarget(wx.TextDropTarget):
    def __init__(self, object):
        wx.TextDropTarget.__init__(self)
        self.object = object

    def OnDropText(self, x, y, data):
        self.object.InsertStringItem(0, data)


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(700, 600))

        splitter1 = wx.SplitterWindow(self, -1)
        splitter2 = wx.SplitterWindow(splitter1)
        splitter3 = wx.SplitterWindow(splitter2)
        self.dir = wx.GenericDirCtrl(splitter1,
                                     -1,
                                     dir='/home/',
                                     style=wx.DIRCTRL_DIR_ONLY
                                     | wx.BORDER_RAISED)
        tree = self.dir.GetTreeCtrl()
        wx.EVT_TREE_SEL_CHANGED(self, tree.GetId(), self.OnSelect)
        self.lc1 = wx.ListCtrl(splitter2, -1, style=wx.LC_LIST)
        wx.EVT_LIST_BEGIN_DRAG(self, self.lc1.GetId(), self.OnDragInit)
        tree = self.dir.GetTreeCtrl()
        splitter1.SplitVertically(self.dir, splitter2, 100)
        splitter2.SplitVertically(self.lc1, splitter3, 200)
        self.textKey = wx.StaticText(splitter3, -1, 'Total: ', (20, 60))
        self.textValue = wx.StaticText(splitter3, -1, 'Total: ', (20, 80))
        self.picNum = wx.TextCtrl(splitter3,
                                  -1,
                                  'Export Number', (80, 60),
                                  size=(160, 30))
        self.exportBtn = wx.Button(splitter3, -1, 'Generate', (250, 60))
        self.exportBtn.Bind(wx.EVT_BUTTON, self.export)
        self.file_name_key = wx.StaticText(splitter3, -1, 'Filename',
                                           (60, 120))
        self.file_name_value = wx.TextCtrl(splitter3,
                                           -1,
                                           'Custom Filename', (120, 120),
                                           size=(160, 30))

        self.OnSelect(0)
        self.Centre()

    def OnSelect(self, event):
        list = os.listdir(self.dir.GetPath())
        self.lc1.ClearAll()
        self.textValue.SetLabel(str(len(list)))
        print(len(list), ' ----------------- len list ---------------')
        for i in range(len(list)):
            if list[i][0] != '.':
                self.lc1.InsertItem(0, list[i])

    def OnDragInit(self, event):
        text = self.lc1.GetItemText(event.GetIndex())
        tdo = wx.PyTextDataObject(text)
        tds = wx.DropSource(self.lc1)
        tds.SetData(tdo)
        tds.DoDragDrop(True)

    def export(self, event):
        list = os.listdir(self.dir.GetPath())
        export_file_name = self.file_name_value.GetValue()
        print(list, ' ------- export file name ---------')
        os.mkdir(self.dir.GetPath() + '/' + export_file_name)
        file_num = self.picNum.GetValue()
        print(file_num, ' -------- file num --------')
        for file in range(int(file_num)):
            shutil.move(self.dir.GetPath() + '/' + list[file], self.dir.GetPath() + '/' + export_file_name)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Client')
        frame.Show()
        self.SetTopWindow(frame)
        return True


app = MyApp(0)
app.MainLoop()