import wx


class UnknownNumCtrl(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.SetName(kwargs.get('name', 'UnknownHexCtrl'))
        self.known_values = kwargs.pop('knownValues', {})
        self.min = kwargs.pop('min', 0)
        self.max = kwargs.pop('max', 0xFFFF)

        self.label = kwargs.pop('label', '')
        sizer = wx.StaticBoxSizer(wx.VERTICAL, self, self.label)
        self.name = wx.StaticText(self, -1, '')
        self.hex_ctrl = wx.SpinCtrl(self, -1, style=wx.SP_ARROW_KEYS | wx.SP_WRAP, min=self.min, max=self.max, **kwargs)
        self.hex_ctrl.Bind(wx.EVT_SPINCTRL, self.on_change)

        sizer.Add(self.name, 0, wx.ALL | wx.VERTICAL, 10)
        sizer.Add(self.hex_ctrl, 0, wx.ALL, 10)

        self.SetSizer(sizer)
        self.SetAutoLayout(1)

    def on_change(self, _):
        self.name.SetLabelText(self.known_values.get(self.hex_ctrl.GetValue(), 'Unknown'))

    def GetValue(self):
        return self.hex_ctrl.GetValue()

    def SetValue(self, value):
        self.hex_ctrl.SetValue(value)
        self.on_change(None)




