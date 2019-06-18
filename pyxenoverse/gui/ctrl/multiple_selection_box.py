import wx

from pyxenoverse.gui.ctrl.custom_check_box import CustomCheckBox
from pyxenoverse.gui.ctrl.custom_radio_box import CustomRadioBox
from pyxenoverse.gui.ctrl.dummy_ctrl import DummyCtrl
from pyxenoverse.gui.ctrl.hex_ctrl import HexCtrl


class MultipleSelectionBox(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.SetName(kwargs.get('name', 'SelectionBox'))
        cols = kwargs.pop('cols', 100)
        title = kwargs.pop('title', '')

        sizer = wx.StaticBoxSizer(wx.VERTICAL, self, title)
        item_sizer = wx.FlexGridSizer(rows=100, cols=cols, hgap=10, vgap=5)

        self.selections = []
        choices = kwargs.pop('choices', [])

        for name, items, multiple in choices:
            if not items and not multiple:
                self.selections.insert(0, DummyCtrl())
                continue
            kwargs['label'] = name or ''
            kwargs['choices'] = items or []
            if multiple:
                ctrl = CustomCheckBox(self, *args, **kwargs)
            else:
                ctrl = CustomRadioBox(self, *args, **kwargs)
            self.selections.insert(0, ctrl)
            item_sizer.Add(ctrl, 0, wx.EXPAND)
        self.hex_ctrl = HexCtrl(self, max=0xFFFF)
        self.hex_ctrl.Disable()
        sizer.Add(item_sizer, 0, wx.LEFT | wx.RIGHT, 10)
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

    def on_select(self, e):
        value = sum(ctrl.GetValue() << (4 * i) for i, ctrl in enumerate(self.selections))
        self.hex_ctrl.SetValue(value)
        e.Skip()

    def on_text(self, e):
        value = self.hex_ctrl.GetValue()
        for i, ctrl in enumerate(self.selections):
            ctrl.SetValue((value >> (4 * i)) & sum(1 << n for n in range(ctrl.GetLength())))
        if e:
            e.Skip()
