import wx

from pyxenoverse.gui.ctrl.hex_ctrl import HexCtrl


class SplitHexCtrl(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.SetName(kwargs.get('name', 'SelectionBox'))
        cols = kwargs.pop('cols', 100)
        title = kwargs.pop('title', '')
        bytes = kwargs.pop('bytes', 1)

        sizer = wx.StaticBoxSizer(wx.VERTICAL, self, title)
        item_sizer = wx.FlexGridSizer(rows=100, cols=cols, hgap=10, vgap=5)

        self.selections = []

        for i in range(bytes * 2):
            label = wx.StaticText(self, -1, chr(65+i))
            item_sizer.Add(label, 0, wx.EXPAND)
            ctrl = wx.SpinCtrl(self, *args, **kwargs, min=0, max=15)
            self.selections.append(ctrl)
            item_sizer.Add(ctrl, 0, wx.EXPAND)
        self.hex_ctrl = HexCtrl(self, max=0xFF * bytes)
        self.hex_ctrl.Disable()
        sizer.Add(item_sizer, 0, wx.LEFT | wx.RIGHT, 10)
        sizer.Add(self.hex_ctrl, 0, wx.ALL, 10)

        self.Bind(wx.EVT_TEXT, self.on_text)

        self.SetSizer(sizer)
        self.SetAutoLayout(1)

    def GetValue(self):
        return self.hex_ctrl.GetValue()

    def SetValue(self, value):
        self.hex_ctrl.SetValue(value)
        value = self.hex_ctrl.GetValue()
        for i, ctrl in enumerate(self.selections):
            ctrl.SetValue(value >> (4 * i) & 0xf)

    def on_text(self, e):
        value = sum(ctrl.GetValue() << (4 * i) for i, ctrl in enumerate(self.selections))
        self.hex_ctrl.SetValue(value)
        e.Skip()
