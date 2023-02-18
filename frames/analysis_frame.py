import customtkinter

class AnalysisFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        for i in range(20):
            self.btt = customtkinter.CTkButton(self.second_frame, text= str(i))
            self.btt.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")