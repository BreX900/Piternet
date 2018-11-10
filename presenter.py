import logging
from tkinter import messagebox, LEFT
from tkinter.ttk import Button, LabelFrame, Label

from utility.pattern import Singleton


class Presenter(metaclass=Singleton):
    def __init__(self):
        self.frames = {}

    @property
    def getFrames(self):
        return self.frames

    @property
    def infoFrame(self):
        return self.frames['INFO']

    @property
    def iternetFrame(self):
        return self.frames['INTERNET']


class LabelFrameAdvanced(LabelFrame):
    def __init__(self, text, **kw):
        super().__init__(text=text, **kw)
        self.presenter = Presenter()
        self.presenter.frames[text] = self


class Depacker(object):
    def __init__(self, padding={}):
        self._list = []
        self._padding = padding

    def add(self, other):
        self._list.append(other)
        return other
    def addLabel(self, **kw):
        return self.add(Label(**kw))
    def addButton(self, **kw):
        return self.add(Button(**kw))
    def addButtonSecure(self, **kw):
        return self.add(ButtonSecure(**kw))

    def pack(self, horizontal=False):
        if horizontal:
            for pack in self._list:
                pack.pack(side=LEFT, **self._padding)
        else:
            for pack in self._list:
                pack.pack(**self._padding)


class ButtonSecure(Button):
    def __init__(self, secureCommand, **kw):
        self.log = logging.getLogger(__name__ + "." + self.__class__.__name__)
        super().__init__(command=self.secureAction, **kw)
        self._secureCommand = secureCommand

    def secureAction(self):
        self.master.setInfo("Start Command: " + str(self.cget("text")))
        if messagebox.askyesno("Start Command", 'Shall I continue?\n' + str(self.cget("text"))):
            self.log.info("Execute Command: " + str(self.cget("text")))
            self.master.setInfo("Execute Command: " + str(self.cget("text")))
            self._secureCommand()
            # self.master.setInfo("Finish Command: " + str(self.cget("text")))
        else:
            self.master.setInfo("Cancel Command: " + str(self.cget("text")))

    def enable(self):
        self.configure(state='enable')

    def disable(self):
        self.configure(state='disable')
