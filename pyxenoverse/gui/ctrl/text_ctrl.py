import wx


class TextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        maxlen = 0
        if "maxlen" in kwargs:
            maxlen = kwargs.pop("maxlen")
        wx.TextCtrl.__init__(self, *args, **kwargs)
        if maxlen:
            self.SetMaxLength(maxlen)

    def GetValue(self):
        return super().GetValue()

    def SetValue(self, value):
        super().ChangeValue(value)
