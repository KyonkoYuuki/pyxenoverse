import wx

from pyxenoverse.gui.ctrl.custom_radio_box import CustomRadioBox
from pyxenoverse.gui.ctrl.hex_ctrl import HexCtrl


class SingleSelectionInfoBox(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.SetName(kwargs.get('name', 'SelectionBox'))
        cols = kwargs.pop('cols', 100)
        title = kwargs.pop('title', '')

        sizer = wx.StaticBoxSizer(wx.VERTICAL, self, title)
        item_sizer = wx.FlexGridSizer(rows=100, cols=cols, hgap=10, vgap=5)

        self.lookup = kwargs.pop('choices', [])
        self.index = kwargs.pop('index', 0)

        kwargs['choices'] = {f'{key}: {value[0]}': key for key, value in self.lookup.items()}
        self.ctrl = CustomRadioBox(self, *args, **kwargs)
        item_sizer.Add(self.ctrl, 0, wx.EXPAND)

        self.text_value = wx.StaticText(self, -1, '')
        self.hex_ctrl = HexCtrl(self, max=0xFFFF)
        self.hex_ctrl.Disable()
        sizer.Add(item_sizer, 0, wx.LEFT | wx.RIGHT, 10)
        sizer.Add(self.text_value, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(self.hex_ctrl, 0, wx.ALL, 10)

        self.Bind(wx.EVT_TEXT, self.on_text)
        self.Bind(wx.EVT_RADIOBOX, self.on_select)
        self.Bind(wx.EVT_CHECKBOX, self.on_select)

        self.SetSizer(sizer)
        self.SetAutoLayout(1)

    def GetValue(self):
        return self.hex_ctrl.GetValue()

    def SetValue(self, value):
        self.hex_ctrl.SetValue(value)
        self.on_text(None)

    def set_text(self, value):
        lookup = self.lookup[value]
        if len(lookup) > 1:
            self.text_value.SetLabelText(lookup[1].get(self.index, ''))
        else:
            self.text_value.SetLabelText('')

    def on_select(self, e):
        value = self.ctrl.GetValue()
        self.hex_ctrl.SetValue(value)
        self.set_text(value)
        e.Skip()

    def on_text(self, e):
        value = self.hex_ctrl.GetValue()
        self.ctrl.SetValue(value)
        self.set_text(value)
        if e:
            e.Skip()
