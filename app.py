import tkinter as tk


from main_frame import MainFrame


class Application(tk.Tk):

    def __init__(self, *args, **kwargs) -> None:
        super(Application, self).__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.title("Voice Unlocker")
        self.geometry('380x170')
        self.resizable(False, False)

        self.frame = MainFrame(self)
        self.frame.pack()

