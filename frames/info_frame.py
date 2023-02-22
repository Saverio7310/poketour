import customtkinter

class InfoFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label_t = customtkinter.CTkLabel(self)
        self.label_t.cget("font").configure(size=20)
        self.label_t.grid(row=0, column=0, columnspan=2, sticky='nsew')