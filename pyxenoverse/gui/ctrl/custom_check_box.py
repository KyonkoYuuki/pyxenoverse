import wx


class CustomCheckBox(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        kwargs.pop('majorDimension', None)
        label = kwargs.pop('label', '')
        orient = kwargs.pop('orient', wx.VERTICAL)
        sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label)
        box_sizer = wx.BoxSizer(orient)
        choices = kwargs.pop('choices', [])

        self.checkboxes = []
        digits = max(4, len(choices))
        for n in range(digits):
            if n < len(choices) and choices[n]:
                checkbox = wx.CheckBox(self, -1, choices[n], **kwargs)
            else:
                checkbox = wx.CheckBox(self, -1, f'Unknown (0x{1 << n})', **kwargs)
            self.checkboxes.append(checkbox)
            box_sizer.Add(checkbox, 0)
        sizer.Add(box_sizer)
        self.SetSizer(sizer)
        self.SetAutoLayout(1)

    def GetValue(self):
        return sum(1 << i for i, ctrl in enumerate(self.checkboxes) if ctrl.GetValue())

    def SetValue(self, value):
        for i, ctrl in enumerate(self.checkboxes):
            ctrl.SetValue(bool((value >> i) & 1))

    def GetLength(self):
        return len(self.checkboxes)
