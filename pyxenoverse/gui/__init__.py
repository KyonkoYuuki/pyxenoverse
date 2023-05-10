from functools import wraps
import os
import time
from shutil import copy
from threading import Thread
from datetime import datetime

import wx


EVT_RESULT_ID = wx.NewId()


def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)


class ResultEvent(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)


class EditThread(Thread):
    def __init__(self, panel):
        Thread.__init__(self)
        self.count = 0
        self.panel = panel
        self.start()
    #UNLEASHED: Lowered the value, users usually leave the fields too fast and value doesn't save
    def run(self):
        while self.count < 0.2:
            time.sleep(0.1)
            self.count += 0.1

        wx.PostEvent(self.panel, ResultEvent())

    def new_sig(self):
        self.count = 0


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


def create_backup(dirname, filename):
    path = os.path.join(dirname, filename)
    if not os.path.exists(path):
        return

    backup_dir = os.path.join(dirname, '.backups')
    try:
        os.mkdir(backup_dir)
    except FileExistsError:
        pass

    backup_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    fileparts = filename.split('.')
    fileparts.insert(1, backup_date)
    backup_path = os.path.join(backup_dir, '.'.join(fileparts))

    copy(path, backup_path)




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
