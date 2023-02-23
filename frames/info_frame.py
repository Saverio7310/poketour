import tkinter
import customtkinter

class InfoFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, name, moveset, tera, ability, item, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1)

        self.label_name = customtkinter.CTkLabel(self, text=name, anchor='center')
        self.label_name.cget("font").configure(size=20)
        self.label_name.grid(row=0, column=1, sticky='nsew', pady = (10, 30))

        self.label_info = customtkinter.CTkLabel(self, text='Info')
        self.label_info.cget("font").configure(size=20)
        self.label_info.grid(row=1, column=0, sticky='nsew', pady = (10, 30))

        self.label_data = customtkinter.CTkLabel(self, text='Dati', anchor='center')
        self.label_data.cget("font").configure(size=20)
        self.label_data.grid(row=1, column=1, sticky='nsew', pady = (10, 30))

        self.label_values = customtkinter.CTkLabel(self, text='Valori')
        self.label_values.cget("font").configure(size=20)
        self.label_values.grid(row=1, column=2, sticky='nsew', pady = (10, 30))

        # moveset
        self.label_moveset = customtkinter.CTkLabel(self, text='Moveset')
        self.label_moveset.cget("font").configure(size=20)

        i = 2
        start = i

        for moves, usage in moveset[:3]:
            string = ', '.join(moves)
            label = customtkinter.CTkLabel(self, text=string)
            label.grid(row=i, column=1, sticky='nsew')
            label = customtkinter.CTkLabel(self, text=usage)
            label.grid(row=i, column=2, sticky='nsew')
            i += 1

        last = i
        if last-start == 1:
            self.label_moveset.grid(row=i-1, column=0, sticky='nsew')
        elif last-start > 1:
            self.label_moveset.grid(row=i-2, column=0, sticky='nsew')

        # linea che separa gli elementi
        self.separator_frame = tkinter.Frame(self, background="white", height=2)
        self.separator_frame.grid_propagate(0)
        self.separator_frame.grid(row=i, column=0, sticky='ew', columnspan=3, padx=(50,50), pady=(20,20))
        i += 1
        start = i

        # tera
        self.label_tera = customtkinter.CTkLabel(self, text='Teratipo')
        self.label_tera.cget("font").configure(size=20)

        for teratype, usage in tera[:3]:
            #string = ', '.join(moves)
            label = customtkinter.CTkLabel(self, text=teratype)
            label.grid(row=i, column=1, sticky='nsew')
            label = customtkinter.CTkLabel(self, text=usage)
            label.grid(row=i, column=2, sticky='nsew')
            i += 1

        last = i
        if last-start == 1:
            self.label_tera.grid(row=i-1, column=0, sticky='nsew')
        elif last-start > 1:
            self.label_tera.grid(row=i-2, column=0, sticky='nsew')

        # linea che separa gli elementi
        self.separator_frame = tkinter.Frame(self, background="white", height=2)
        self.separator_frame.grid_propagate(0)
        self.separator_frame.grid(row=i, column=0, sticky='ew', columnspan=3, padx=(50,50), pady=(20,20))
        i += 1
        start = i

        # ability
        self.label_ability = customtkinter.CTkLabel(self, text='Abilità')
        self.label_ability.cget("font").configure(size=20)

        for abil, usage in ability[:3]:
            #string = ', '.join(moves)
            label = customtkinter.CTkLabel(self, text=abil)
            label.grid(row=i, column=1, sticky='nsew')
            label = customtkinter.CTkLabel(self, text=usage)
            label.grid(row=i, column=2, sticky='nsew')
            i += 1

        last = i
        if last-start == 1:
            self.label_ability.grid(row=i-1, column=0, sticky='nsew')
        elif last-start > 1:
            self.label_ability.grid(row=i-2, column=0, sticky='nsew')

        # linea che separa gli elementi
        self.separator_frame = tkinter.Frame(self, background="white", height=2)
        self.separator_frame.grid_propagate(0)
        self.separator_frame.grid(row=i, column=0, sticky='ew', columnspan=3, padx=(50,50), pady=(20,20))
        i += 1
        start = i

        # item
        self.label_item = customtkinter.CTkLabel(self, text='Oggetto')
        self.label_item.cget("font").configure(size=20)

        for it, usage in item[:3]:
            #string = ', '.join(moves)
            label = customtkinter.CTkLabel(self, text=it)
            label.grid(row=i, column=1, sticky='nsew')
            label = customtkinter.CTkLabel(self, text=usage)
            label.grid(row=i, column=2, sticky='nsew')
            i += 1

        last = i
        if last-start == 1:
            self.label_item.grid(row=i-1, column=0, sticky='nsew')
        elif last-start > 1:
            self.label_item.grid(row=i-2, column=0, sticky='nsew')

        """ self.label_name = customtkinter.CTkLabel(self, text=moveset[0][0])
        self.label_name.cget("font").configure(size=20)
        self.label_name.grid(row=2, column=1, sticky='nsew')

        self.label_name = customtkinter.CTkLabel(self, text=moveset[1][0])
        self.label_name.cget("font").configure(size=20)
        self.label_name.grid(row=3, column=1, sticky='nsew')

        self.label_name = customtkinter.CTkLabel(self, text=moveset[2][0])
        self.label_name.cget("font").configure(size=20)
        self.label_name.grid(row=4, column=1, sticky='nsew') """

        """ # tera
        self.label_name = customtkinter.CTkLabel(self, text=name)
        self.label_name.cget("font").configure(size=20)
        self.label_name.grid(row=0, column=0, columnspan=3, sticky='nsew')

        self.label_name = customtkinter.CTkLabel(self, text='Info')
        self.label_name.cget("font").configure(size=20)
        self.label_name.grid(row=1, column=0, sticky='nsew')

        self.label_name = customtkinter.CTkLabel(self, text='Dati')
        self.label_name.cget("font").configure(size=20)
        self.label_name.grid(row=1, column=1, sticky='nsew')

        self.label_name = customtkinter.CTkLabel(self, text='Valori')
        self.label_name.cget("font").configure(size=20)
        self.label_name.grid(row=1, column=2, sticky='nsew') """