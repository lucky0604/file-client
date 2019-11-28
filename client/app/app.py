import wx
import os
import shutil
import pandas as pd
from tqdm import tqdm


class ExportPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(800, 600))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        pnl1 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        pnl2 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        pnl3 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        hbox.Add(pnl1, 1, wx.EXPAND | wx.ALL, 3)
        hbox.Add(pnl2, 1, wx.EXPAND | wx.ALL, 3)
        hbox.Add(pnl3, 1, wx.EXPAND | wx.ALL, 3)
        self.SetSize((400, 500))
        self.SetSizer(hbox)
        self.dir = wx.GenericDirCtrl(pnl1,
                                     -1,
                                     size=(200, 600),
                                     dir='/home/',
                                     style=wx.DIRCTRL_DIR_ONLY
                                     | wx.BORDER_RAISED)
        tree = self.dir.GetTreeCtrl()
        wx.EVT_TREE_SEL_CHANGED(self, tree.GetId(), self.OnSelect)
        self.lc1 = wx.ListCtrl(pnl2, -1, size=(200, 600), style=wx.LC_LIST)
        wx.EVT_LIST_BEGIN_DRAG(self, self.lc1.GetId(), self.OnDragInit)
        tree = self.dir.GetTreeCtrl()
        self.textKey = wx.StaticText(pnl3, -1, 'Total: ', (20, 60))
        self.textValue = wx.StaticText(pnl3, -1, 'Total: ', (20, 80))
        self.picNum = wx.TextCtrl(pnl3,
                                  -1,
                                  'Export Number', (80, 60),
                                  size=(160, 30))
        self.exportBtn = wx.Button(pnl3, -1, 'Generate', (250, 60))
        self.exportBtn.Bind(wx.EVT_BUTTON, self.export)
        self.file_name_key = wx.StaticText(pnl3, -1, 'Filename', (60, 120))
        self.file_name_value = wx.TextCtrl(pnl3,
                                           -1,
                                           'Custom Filename', (120, 120),
                                           size=(160, 30))

        self.OnSelect(0)
        self.Centre()

    def OnSelect(self, event):
        list = os.listdir(self.dir.GetPath())
        self.lc1.ClearAll()
        self.textValue.SetLabel(str(len(list)))
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
        os.mkdir(self.dir.GetPath() + '/' + export_file_name)
        file_num = self.picNum.GetValue()

        if os.path.exists(self.dir.GetPath() + '/' + 'result.xlsx'):
            df = pd.read_excel(self.dir.GetPath() + '/' + 'result.xlsx')
            for file in range(int(file_num)):
                shutil.move(self.dir.GetPath() + '/' + list[file],
                            self.dir.GetPath() + '/' + export_file_name)
                for j in range(len(df['Filename'])):
                    if list[file] == df['Filename'][j]:
                        df['Status'][j] = 'Sending'
            df.to_excel(self.dir.GetPath() + '/' + 'result.xlsx',
                        sheet_name='Sheet1',
                        index=False)
        else:
            df1 = pd.DataFrame({'Filename': list, '': None, 'Status': None})
            for file in range(int(file_num)):
                shutil.move(self.dir.GetPath() + '/' + list[file],
                            self.dir.GetPath() + '/' + export_file_name)
                df1.loc[file]['Status'] = 'Sending'
                df1.to_excel(self.dir.GetPath() + '/' + 'result.xlsx',
                             sheet_name='Sheet1',
                             index=True)


class MergePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, size=(800, 600))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        pnl1 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        pnl2 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        pnl3 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        hbox.Add(pnl1, 1, wx.EXPAND | wx.ALL, 3)
        hbox.Add(pnl2, 1, wx.EXPAND | wx.ALL, 3)
        hbox.Add(pnl3, 1, wx.EXPAND | wx.ALL, 3)
        self.SetSize((400, 500))
        self.SetSizer(hbox)

        self.dir1 = wx.GenericDirCtrl(pnl1,
                                      -1,
                                      size=(200, 600),
                                      dir='/home/',
                                      style=wx.DIRCTRL_DIR_ONLY
                                      | wx.BORDER_RAISED)
        self.dir2 = wx.GenericDirCtrl(pnl2,
                                      -1,
                                      size=(200, 600),
                                      dir='/home/',
                                      style=wx.DIRCTRL_DIR_ONLY
                                      | wx.BORDER_RAISED)

        self.mergeBtn = wx.Button(pnl3, -1, 'Merge', (20, 20))
        self.mergeBtn.Bind(wx.EVT_BUTTON, self.OnMerge)

    def OnMerge(self, event):
        xml_list = []
        img_list = []
        os.mkdir(self.dir1.GetPath() + '/result')
        for home, dirs, files in os.walk(self.dir1.GetPath()):
            for file in files:
                if os.path.splitext(file)[1] == '.jpg' or os.path.splitext(
                        file)[1] == '.png':
                    img_list.append(file)
        for home, dirs, files in os.walk(self.dir2.GetPath()):
            for file in files:
                print(os.path.join(home, file),
                      ' ------------- file ---------------')
                if os.path.splitext(file)[1] == '.xml':
                    xml_list.append(file)
        for i in xml_list:
            for j in img_list:
                if os.path.splitext(i)[0] == os.path.splitext(j)[0]:
                    shutil.move(self.dir1.GetPath() + '/' + j,
                                self.dir1.GetPath() + '/result')
                    for root, dirs, files in os.walk(self.dir2.GetPath()):
                        for file in tqdm(files):
                            if file == j:
                                src_file = os.path.join(root, i)
                                shutil.copy(src_file, self.dir1.GetPath() + '/result')
                    # shutil.copy()

        print(len(xml_list), ' ---------------xml list------------')
        print(len(img_list), ' ---------------img list------------')


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 600))

        p = wx.Panel(self)
        nb = wx.Notebook(p)

        tab1 = ExportPanel(nb)
        tab2 = MergePanel(nb)

        nb.AddPage(tab1, 'tab1')
        nb.AddPage(tab2, 'tab2')

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Client')
        frame.Show()
        self.SetTopWindow(frame)
        return True


app = MyApp(0)
app.MainLoop()