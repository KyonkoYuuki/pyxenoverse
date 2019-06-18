import wx
from functools import wraps


def add_entry(func):
    @wraps(func)
    def entry_wrapper(*args, **kwargs):
        panel, label = args[1], args[2]
        if label:
            panel.sizer.Add(wx.StaticText(panel, -1, label), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.TOP, 10)
            kwargs['name'] = label
        control = func(*args, **kwargs)
        panel.sizer.Add(control, 0, wx.LEFT | wx.TOP, 10)
        return control
    return entry_wrapper
