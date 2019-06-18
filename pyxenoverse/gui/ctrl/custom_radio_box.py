import wx


class CustomRadioBox(wx.RadioBox):
    def __init__(self, *args, **kwargs):
        self.lookup = []
        self.choices = kwargs.pop('choices', [])
        if type(self.choices) == dict:
            self.lookup = list(self.choices.values())
            self.choices = list(self.choices.keys())
        elif type(self.choices) == list:
            self.lookup = list(self.choices)
        else:
            raise TypeError
        kwargs['choices'] = self.choices
        kwargs.pop('orient', None)
        super().__init__(*args, **kwargs)

    def GetValue(self):
        idx = self.GetSelection()
        if idx == wx.NOT_FOUND:
            return wx.NOT_FOUND
        return self.lookup[idx]

    def SetValue(self, value):
        idx = self.lookup.index(value)
        self.SetSelection(idx)

    def GetLength(self):
        return max(self.lookup).bit_length()
