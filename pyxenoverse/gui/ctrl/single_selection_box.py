from pyxenoverse.gui.ctrl.multiple_selection_box import MultipleSelectionBox


class SingleSelectionBox(MultipleSelectionBox):
    def __init__(self, parent, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        multiple = kwargs.pop('multiple', False)
        kwargs['choices'] = [('', choices, multiple)]
        super().__init__(parent, *args, **kwargs)

    def on_select(self, e):
        self.hex_ctrl.SetValue(self.selections[0].GetValue())
        e.Skip()

    def on_text(self, e):
        self.selections[0].SetValue(self.hex_ctrl.GetValue())
        if e:
            e.Skip()
