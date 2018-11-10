from tkinter.ttk import Label, LabelFrame

import parameter

DEVELOPMENT = 0

def devolopment() :
    return ("DEVELOPMENT" if DEVELOPMENT else "RUN APP")

class DevelopmentFrame(LabelFrame):
    def __init__(self, **kw):
        super().__init__(text='GOOOOO', **kw)

        text = 'DEVELOPMENT' if DEVELOPMENT else 'RUN APP'
        Label(self, text=text).pack(parameter.PADDING_WIDGET)
