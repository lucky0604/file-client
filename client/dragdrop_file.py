import wx

class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        for name in filenames:
            try:
                file = open(name, 'r')
                text = file.read()
                self.window.WriteText(text)

            except IOError as error:
                msg = 'Error opening file\n {}'.format(str(error))

                dlg = wx.MessageDialog(None, msg)
                dlg.ShowModal()
                return False

            except UnicodeDecodeError as error:
                msg = "Cannot open non asciifiles\n {}".format(str(error))
                dlg = wx.MessageDialog(None, msg)
                dlg.ShowModal()
                return False

            finally:
                file.close()

        return True

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.text = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        dt = FileDrop(self.text)
        self.text.SetDropTarget(dt)
        self.SetTitle('File drag and drop')
        self.Centre()

if __name__ == '__main__':
    app = wx.App()
    ex = MyFrame(None)
    ex.Show()
    app.MainLoop()
