import wx
from functools import partial


class UnknownNumCtrl(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.SetName(kwargs.get('name', 'UnknownHexCtrl'))
        self.known_values = kwargs.pop('knownValues', {})
        self.show_known = kwargs.pop('showKnown', False)
        self.min = kwargs.pop('min', 0)
        self.max = kwargs.pop('max', 0xFFFF)
        cols = kwargs.pop('cols', 100)

        self.label = kwargs.pop('label', '')
        sizer = wx.StaticBoxSizer(wx.VERTICAL, self, self.label)

        if self.show_known:
            button_sizer = wx.FlexGridSizer(rows=100, cols=cols, hgap=10, vgap=5)
            sizer.Add(button_sizer, 0, wx.LEFT, 10)
            for value, text in self.known_values.items():
                button = wx.Button(self, -1, text)
                button.Bind(wx.EVT_BUTTON, partial(self.on_click, value=value))
                button_sizer.Add(button, 0, wx.EXPAND)

        #UNLEASHED: Small Hack to increase the width, idk how to do it otherwise
        self.name = wx.StaticText(self, -1, 'PLACEHOLDERPLACEHOLDERPLACEHOLDERPLACEHOLDERPLACEHOLDER')
        self.hex_ctrl = wx.SpinCtrl(self, -1, style=wx.SP_ARROW_KEYS | wx.SP_WRAP, min=self.min, max=self.max, **kwargs)
        self.hex_ctrl.Bind(wx.EVT_SPINCTRL, self.on_change)

        sizer.Add(self.name, 0, wx.LEFT, 10)
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

    def on_click(self, _, value):
        self.SetValue(value)
