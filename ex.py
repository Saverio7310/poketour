import customtkinter
from functools import partial
from Database.db_connection import DBConnection
import tkinter as tk

'''
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x300")
        self.title("small example app")
        self.minsize(800, 600)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.textbox = customtkinter.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")

        self.combobox = customtkinter.CTkComboBox(master=self, values=["Sample text 1", "Text 2"])
        self.combobox.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Insert Text")
        self.button.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

    def button_callback(self):
        self.textbox.insert("insert", self.combobox.get() + "\n")




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        l=[0,1,2,3,4]

        for i, _ in enumerate(l):
            # Create the command using partial
            button = customtkinter.CTkButton(self, text="Button number"+str(i), command=partial(self.create_new_page, i))
            button.grid(row=i)

    def create_new_page(self, name_of_page):
        print("Creating new page with name=\"%s\"" % name_of_page)






if __name__ == "__main__":
    app = App()
    app.mainloop()
'''

db = DBConnection()
conn = db.start_connection()
top_moveset, top_tera, top_ability, top_item = db.get_specific_poke_info(conn, tour_code='OCpGIIa9m9BGzlZ8B5Gt', poke_name='Arcanine')

#print(top_moveset)

moveset_list = list()

for moveset in top_moveset:
    moveset_list.append(set(moveset))

moveset_list_final = list()

for move_set1 in moveset_list:
    num = 0
    temp_ind = list()
    for move_set2 in moveset_list:
        if move_set2 == move_set1:
            num += 1
            moveset_list.remove(move_set2)
            print(moveset_list)
    moveset_list_final.append((move_set1, num))

moveset_list_final.sort(key=lambda a : a[1], reverse=True)

print(*moveset_list_final, sep='\n')
#print(*top_ability[:5], sep='\n')
#print(*top_item, sep='\n')
#print(*top_tera, sep='\n')