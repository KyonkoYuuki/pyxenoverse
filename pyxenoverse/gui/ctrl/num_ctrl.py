from pyxenoverse.gui.ctrl.unknown_num_ctrl import UnknownNumCtrl


class NumCtrl(UnknownNumCtrl):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.hex_ctrl.SetBase(10)
