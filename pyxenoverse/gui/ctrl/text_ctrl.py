import wx


class TextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        wx.TextCtrl.__init__(self, *args, **kwargs)

    def GetValue(self):
        return super().GetValue()

    def SetValue(self, value):
        super().ChangeValue(value)
