import wx


class ColourPickerCtrl(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        kwargs["style"] = kwargs.get("style", wx.CLRP_DEFAULT_STYLE) | wx.CLRP_SHOW_LABEL
        sizer = wx.BoxSizer()

        self.color_ctrl = wx.ColourPickerCtrl(self, *args, **kwargs)
        self.alpha_ctrl = wx.Slider(self, -1, minValue=0, maxValue=255)
        self.alpha_ctrl.Bind(wx.EVT_SLIDER, self.on_alpha_change)
        self.alpha_value = wx.StaticText(self, -1, '0', size=(50, -1))

        sizer.Add(self.color_ctrl, 0, wx.ALL)
        sizer.Add(wx.StaticText(self, -1, 'Alpha'), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        sizer.Add(self.alpha_ctrl, 0, wx.ALL)
        sizer.Add(self.alpha_value, 0, wx.ALIGN_CENTER_VERTICAL)

        self.SetSizer(sizer)
        self.SetAutoLayout(1)

    def GetValue(self):
        color = self.color_ctrl.GetColour()
        r = color.Red()
        g = color.Green()
        b = color.Blue()
        a = self.alpha_ctrl.GetValue()
        return r, g, b, a

    def SetValue(self, value):
        r, g, b, a = value
        self.color_ctrl.SetColour(wx.Colour(r, g, b))
        self.alpha_ctrl.SetValue(a)
        self.alpha_value.SetLabelText(f'{a}')

    def on_alpha_change(self, e):
        alpha = self.alpha_ctrl.GetValue()
        self.alpha_value.SetLabelText(f'{alpha}')
        e.Skip()
