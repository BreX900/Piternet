import logging.config
import tkinter

import parameter
from utility.development import DevelopmentFrame
from infoFrame import InfoFrame
from presenter import LabelFrameAdvanced, Depacker
from piternet import Board, Piternet

from tkinter import Tk, StringVar, messagebox
from tkinter.ttk import Frame, Style


class PiternetFrame(LabelFrameAdvanced):
    def __init__(self, master, **kw):
        self.log = logging.getLogger(__name__ + "." + self.__class__.__name__)

        super(PiternetFrame, self).__init__(master=master, text="INTERNET", **kw)
        self._board = Board()
        self._piternet = Piternet(self._board)

        dp = Depacker(parameter.PADDING_WIDGET)
        self._statusPiternet = StringVar()
        dp.addButton(master=self, textvariable=self._statusPiternet, command=self.refreshStatusPiternetButtonAction)
        self._startPiternetButton = dp.addButtonSecure(master=self, text="Start", secureCommand=self.startPiternetButtonAction)
        self._stopPiternetButton = dp.addButtonSecure(master=self, text="Stop", secureCommand=self.stopPiternetButtonAction)
        self._restartPiternetButton = dp.addButtonSecure(master=self, text="Restart", secureCommand=self.restartPiternetButtonAction)
        dp.addButtonSecure(master=self, text="Info Board", secureCommand=self.infoBoard)
        dp.pack(True)

        if self._piternet.isOnline():
            self._startPiternetButton.disable()
        else:
            self._stopPiternetButton.disable()
            self._restartPiternetButton.disable()

    def startPiternetButtonAction(self):
        self._startPiternetButton.disable()
        self._piternet.start()
        self._restartPiternetButton.enable()
        self._stopPiternetButton.enable()
        self.refreshStatusPiternet()

    def stopPiternetButtonAction(self):
        self._startPiternetButton.enable()
        self._piternet.stop()
        self._restartPiternetButton.disable()
        self._stopPiternetButton.disable()
        self.refreshStatusPiternet()

    def restartPiternetButtonAction(self):
        self.setInfo("Internet Connection: Stopping...")
        self._restartPiternetButton.disable()
        self._stopPiternetButton.disable()
        self._startPiternetButton.disable()
        self._piternet.restart()
        self.after(10000, self.restartPiternetButtonActionStepTwo)
        self.refreshStatusPiternet()
        self.setInfo("Internet Connection: Restarting...")

    def restartPiternetButtonActionStepTwo(self):
        self._piternet.restartStepTwo()
        self._restartPiternetButton.enable()
        self._stopPiternetButton.enable()
        self.refreshStatusPiternet()
        self.refreshStatusPiternet()
        self.setInfo("Internet Connection: ONLINE")

    def setInfo(self, text):
        self.presenter.infoFrame.setInfo(text)

    def refreshStatusPiternetButtonAction(self):
        self.refreshStatusPiternet()
        status = "ONLINE" if self._piternet.isOnline() else "OFFLINE"
        self.setInfo("Refresh Status Internet: " + status)
        self.after(2500, self.resetInfoMessage)

    def refreshStatusPiternet(self):
        self._statusPiternet.set("ONLINE" if self._piternet.isOnline() else "OFFLINE")

    def resetInfoMessage(self):
        self.presenter.infoFrame.resetInfoMessage()

    def infoBoard(self):
        self.setInfo(self._board.info())


class StColors(object):
    black = '#252a2c'
    dark_grey = '#33393b'
    mid_grey = '#FF0000'
    bright_green = '#DDDDDD' #verde
    light_grey = '#FFFFFF'



class TurnChangeWindows(Tk):
    def __init__(self, **kw):
        self.log = logging.getLogger(__name__ + "." + self.__class__.__name__)

        super(TurnChangeWindows, self).__init__(**kw)

        style = Style()
        style.theme_create("st_app", parent="alt", settings={
            ".": {"configure": {"font": ("Calibri", 13, 'bold'),
                                "background": StColors.dark_grey,
                                "foreground": StColors.light_grey,
                                "relief": "flat",
                                "highlightcolor": StColors.bright_green, }, },
            "TLabel": {"configure": {"foreground": StColors.bright_green,
                                     "padding": 5,
                                     "font": ("Calibri", 11)}},

            "TNotebook": {"configure": {"padding": 5}},
            "TNotebook.Tab": {"configure": {"padding": [25, 5],
                                            "foreground": "white"},
                              "map": {"background": [("selected", StColors.mid_grey)],
                                      "expand": [("selected", [1, 1, 1, 0])]}},

            "TCombobox": {"configure": {"selectbackground": StColors.dark_grey,
                                        "fieldbackground": "white",
                                        "background": StColors.light_grey,
                                        "foreground": "black"}},

            "TButton": {"configure": {"font": ("Calibri", 13),
                                      "background": StColors.black,
                                      "foreground": StColors.bright_green},
                        "map": {"background": [("active", StColors.bright_green), ("disabled", '#2d3234')],
                                "foreground": [("active", 'black'), ("disabled", '#919282')]}},

            "TEntry": {"configure": {"foreground": "black"}},
            "Horizontal.TProgressbar": {"configure": {"background": StColors.mid_grey}}
        })
        style.theme_use("st_app")

        self.title("Piternet")
        self.geometry("630x230")
        self.configure(background=StColors.black)

        s = Style()
        s.configure('My.TFrame', background=StColors.black)

        frame = Frame(self, style='My.TFrame')
        self._developmentFrame = DevelopmentFrame(master=frame)
        self._infoFrame = InfoFrame(master=self)
        self._turnChangeFrame = PiternetFrame(master=frame)

        # self.bind("<Button-1>", self.callback)
        self._refreshKey = False
        self.bind_all('<KeyPress>', self.keyPress)

        self._infoFrame.pack(expand=True, fill='x', **parameter.PADDING_FRAME_EXTERNAL_TOP)

        self._developmentFrame.pack(side=tkinter.LEFT, expand=False, **parameter.PADDING_FRAME_LEFT)
        self._turnChangeFrame.pack(side=tkinter.RIGHT, expand=False, **parameter.PADDING_FRAME_RIGHT)

        frame.pack(fill='x', **parameter.PADDING_FRAME_EXTERNAL_BOT)

        self.protocol("WM_DELETE_WINDOW", self.onExit)
        self._turnChangeFrame.refreshStatusPiternet()




    def callback(self, event):
        self._turnChangeFrame.refreshStatusPiternet()
        return

    def onExit(self):
        if messagebox.askyesno("Exit", "Quit?"):
            Board().reset()
            self.destroy()

    def keyPress(self, event):
        if event.keysym == 'r':
            if self._refreshKey:
                pass
            else:
                self._refreshKey = True
                self._turnChangeFrame.refreshStatusPiternetButtonAction()
                self.after(3000, self.refreshStatusPiternetKeyPress)

    def refreshStatusPiternetKeyPress(self):
        self._refreshKey = False


'''if __name__ == '__main__':
    #os.environ["DISPLAY"] = "192.168.178.45:10.0"#"192.168.178.45:0.0"

    application = TurnChangeWindows()
    application.mainloop()'''
