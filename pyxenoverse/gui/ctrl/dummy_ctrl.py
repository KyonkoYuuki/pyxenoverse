class DummyCtrl():
    def __init__(self):
        self.value = False

    def GetValue(self):
        return self.value

    def SetValue(self, value):
        self.value = value

    def ChangeValue(self, value):
        self.value = value

    def GetLength(self):
        return 4
