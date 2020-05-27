import wx


class ColourPickerCtrl(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        kwargs["style"] = kwargs.get("style", wx.CLRP_DEFAULT_STYLE) | wx.CLRP_SHOW_LABEL
        self.sizer = wx.BoxSizer()

        self.color_ctrl = wx.ColourPickerCtrl(self, *args, **kwargs)

        self.sizer.Add(self.color_ctrl, 0, wx.ALL)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)

    def GetValue(self):
        color = self.color_ctrl.GetColour()
        r = color.Red()
        g = color.Green()
        b = color.Blue()
        return r, g, b

    def SetValue(self, value):
        r, g, b = value
        self.color_ctrl.SetColour(wx.Colour(r, g, b))
