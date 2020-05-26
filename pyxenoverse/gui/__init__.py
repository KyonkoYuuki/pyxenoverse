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
        panel.sizer.Add(control, 0, wx.LEFT | wx.TOP, 5)
        return control
    return entry_wrapper


def _get_parent(list_ctrl, item):
    parent = list_ctrl.GetItemParent(item)
    if parent == list_ctrl.GetRootItem():
        return None
    next_item = list_ctrl.GetNextSibling(parent)
    if not next_item.IsOk():
        next_item = _get_parent(list_ctrl, parent)
    return next_item


def get_next_item(list_ctrl, item):
    next_item = list_ctrl.GetFirstChild(item)[0]
    if not next_item.IsOk():
        next_item = list_ctrl.GetNextSibling(item)
    if not next_item.IsOk():
        parent = _get_parent(list_ctrl, item)
        if parent:
            next_item = parent
    return next_item


def get_first_item(list_ctrl):
    root = list_ctrl.GetRootItem()
    return list_ctrl.GetFirstChild(root)


def get_item_index(list_ctrl, item):
    parent = list_ctrl.GetItemParent(item)
    child, _ = list_ctrl.GetFirstChild(parent)
    index = 0
    while child.IsOk():
        if child == item:
            return index
        child = list_ctrl.GetNextSibling(child)
        index += 1
    return -1
