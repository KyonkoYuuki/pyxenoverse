import wx

VALID_VALUES = 'ABCDEFabcdef0123456789\x08\x7f'


class HexCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        self.max = kwargs.pop('max', 0xFFFFFFFF)
        if self.max < 0:
            raise ValueError
        if 'value' not in kwargs:
            kwargs['value'] = '0x0'
        wx.TextCtrl.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_CHAR, self.on_char)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)

    def GetValue(self):
        try:
            return int(super().GetValue(), 16)
        except Exception:
            return 0

    def SetValue(self, value):
        super().ChangeValue(f'0x{value:X}')

    def GetMax(self):
        return self.max

    def SetMax(self, max_value):
        if max_value < 0:
            raise ValueError
        self.max = max_value

    def on_kill_focus(self, e):
        try:
            value = self.GetValue()
            if value > self.max:
                value = self.max
        except:
            value = 0
        self.SetValue(value)
        e.Skip()

    def on_char(self, e):
        keycode = e.GetKeyCode()
        if 32 <= keycode < 255 and chr(keycode) not in VALID_VALUES:
            return
        e.Skip()


