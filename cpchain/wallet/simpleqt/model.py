
class Model:

    def __init__(self, value):
        self.value_ = value
        self.view = None

    @property
    def value(self):
        return self.value_

    @value.setter
    def value(self, val):
        self.value_ = val
        if self.view:
            self.view.change.emit(val)

    def plain_set(self, val):
        self.value_ = val

    def setView(self, view):
        self.view = view