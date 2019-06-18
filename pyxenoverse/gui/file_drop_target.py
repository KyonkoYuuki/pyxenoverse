import os

import wx
from pubsub import pub


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, window, publish_target):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.publish_target = publish_target

    def OnDropFiles(self, x, y, filenames):
        dirname, filename = os.path.split(filenames[0])
        if not filename:
            return False
        pub.sendMessage(self.publish_target, filename=filename, dirname=dirname)
        return True
