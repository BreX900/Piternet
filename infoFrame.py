from tkinter import StringVar

import parameter
from presenter import LabelFrameAdvanced, ButtonSecure
from presenter import Depacker


class InfoFrame(LabelFrameAdvanced):
    def __init__(self, **kw):
        super().__init__(text='INFO', **kw)
        dp = Depacker(parameter.PADDING_WIDGET)
        self._infoLabelText = StringVar()
        dp.addButtonSecure(master=self, text="Reset Info Message", secureCommand=self.resetInfoMessage)
        dp.addLabel(master=self, textvariable=self._infoLabelText)
        dp.pack(True)

    def setInfo(self, text):
        self._infoLabelText.set(text)

    def resetInfoMessage(self):
        self.setInfo("______________________________________")
