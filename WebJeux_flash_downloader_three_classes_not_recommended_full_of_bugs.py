import requests
from bs4 import BeautifulSoup
from PIL import Image
import customtkinter as ctk
import tkinter as tk
import os

ctk.set_appearance_mode("dark")
img = Image.open('flipline_studio.png')

class suggestion:
    def __init__(self):
        self.gui_class = None
        #going through the sugestion file and appending them all to "suggestions" list
        with open("Webjeux_games_names.txt","r") as f:
            self.suggestions = [line.strip() for line in f if line.strip()]

        self.item = ""
    #function responsible of updating suggestions while typing game's name
    def on_type(self,event):
        #removing bottom labels
        self.gui_class.label6_forget()
        self.gui_class.label4_forget()
        self.gui_class.label5_forget()
        #getting the typed text and removing the listbox to update it based on if it is empty or not
        text = self.gui_class.get_entry1_text().lower()
        self.gui_class.listbox_clear()
        #going through the suggestion list to find matches,if so, it gets inserted to the listbox
        if text:
            for self.item in self.suggestions:
                if self.item.lower().startswith(text):
                    self.gui_class.listbox_adding_suggestion()
            #packing the listbox if it's not empty       
            if self.gui_class.listbox_size()>0:
                self.gui_class.label2_forget()
                self.gui_class.dropbox_forget()
                self.gui_class.entry2_forget()
                self.gui_class.button1_forget()
                self.gui_class.listbox_pack()
                self.gui_class.label2_pack()
                self.gui_class.dropbox_pack()
                #packing the path entry if checkbow state is 'custom'
                if self.gui_class.inst_choice==1:
                    self.gui_class.entry2_pack()
                self.gui_class.button1_pack()
                return
        #removing the listbox if it's empty    
        self.gui_class.listbox_forget()
        
    #function responsible of adding selected suggestion to the entry box   
    def on_select(self,event):
        if self.gui_class.listbox_selection_tupple:
            self.gui_class.entry1_clear()
            self.gui_class.entry1_adding_suggestion()
            self.gui_class.listbox_forget() 

class download:
    def __init__(self):
        self.gui_class = None
    #name cleaner    
    def name_cleaner(self):
        un_gm_nm = self.gui_class.get_entry1_text()
        un_gm_nm = un_gm_nm.lower()
        un_gm_nm = un_gm_nm.replace(" ","-")
        self.game_name = un_gm_nm
        print("game name : ",self.game_name)

    #path handler    
    def path_handler(self):
        if self.gui_class.inst_choice:
            custom_path = self.gui_class.get_entry2_text()
            self.path = os.path.join(custom_path, self.game_name)
        else:
            self.path = 'C:\\Users\\HP\\Downloads\\flash games\\'+self.game_name

    #error handler
    def error_handler(self):
        try:    
            self.r = requests.get("https://www.webjeux.com/jouer/"+self.game_name+".html")
        except requests.exceptions.RequestException:
            print("Failed to reach the server. Please check your internet connection ")
            self.gui_class.label6_forget()
            self.gui_class.label5_forget()
            self.gui_class.label4_pack()
            return 1
        print("WebJeux status code : ",self.r.status_code)
        if self.r.status_code == 404:
            print("Game not found")
            self.gui_class.label4_forget()
            self.gui_class.label5_forget()
            self.gui_class.label6_pack()
            return 1
        return 0
    
    #game download    
    def body(self):  
        self.name_cleaner()
        self.path_handler()
        if self.error_handler():
            return
        soup = BeautifulSoup(self.r.text, "html.parser")
        swfs = soup.find(attrs={"data":True})
        swf = swfs["data"]
        r2 = requests.get(swf)
        print("swf status code : ",r2.status_code)
        headers = r2.headers
        print("Content type : ",headers["Content-Type"])
        with open(self.path+'.swf','wb') as f:
            f.write(r2.content)
            print("Success")
        #packing success message    
        self.gui_class.label6_forget()
        self.gui_class.label4_forget()
        self.gui_class.label5_pack()
            

class gui:
    def __init__(self, obj_download, obj_suggestion):
        #class objects
        self.download_class = obj_download
        self.suggestion_class = obj_suggestion
        #the root, instance choice variable to 0 in default
        #instance choice variable is used in body function to create the download path (default or custom), It's used again in on_type function to pack the enrty if choice is "custom",it's needed to pack the listbox (listbox is above the entry)
        self.root = ctk.CTk()
        self.root.title("WebJeux.com flash games downloader")
        self.root.geometry("520x640")
        self.root.resizable(False,False)
        self.inst_choice = 0
        #functions calling
        self.user_com()
        self.bottom_labels()
        self.img_frame()
        
    #function responsible of showing the errors and the success in the bottom
    def bottom_labels(self):
        self.label4 = ctk.CTkLabel(self.root, text='Failed to reach the server. Please check your internet connection', font=ctk.CTkFont("arial black", 12),text_color="#E21F1F")
        self.label5 = ctk.CTkLabel(self.root, text='The game is successfully downloaded', font=ctk.CTkFont("arial black", 12),text_color="#55BD21")
        self.label6 = ctk.CTkLabel(self.root, text='Game not found', font=ctk.CTkFont("arial black", 12),text_color="#E21F1F")
            
    #function responsible of the main GUI layout
    def user_com(self):
        
        self.label1 = ctk.CTkLabel(self.root, text='Welcome to WebJeux flash games.\nEnter game name :',font=ctk.CTkFont("arial black", 15))
        self.label1.pack(pady=15)

        self.entry1 = ctk.CTkEntry(self.root, placeholder_text="Start typing...", width=200)
        self.entry1.pack()

        self.listbox = tk.Listbox(self.root,height=6)

        self.label2 = ctk.CTkLabel(self.root, text='Select download path :\nThe game gonna be saved in flash games folder by default',font=ctk.CTkFont("arial black", 14))
        self.label2.pack(pady=20)

        self.dropbox = ctk.CTkOptionMenu(self.root,command=self.path_fun,text_color_disabled="gray",dropdown_font=("arial black", 12),font=("arial black", 14),button_hover_color='#9A4743',fg_color="#C1554F",button_color='#C1554F',width=200,corner_radius=10, values=["Default","Custom"])
        self.dropbox.pack(pady=5)

        self.entry2 = ctk.CTkEntry(self.root, placeholder_text="Start typing...",width=200)
   
        self.button1 = ctk.CTkButton(self.root,command=self.download_class.body, text='Download', corner_radius=15, fg_color='#F7494B',hover_color='#C90E0E',text_color='#171519',border_width=2,width=200,height=50,font=ctk.CTkFont("arial black", 20))
        self.button1.pack(pady=5)
        #detect keyboard keys and calling the function, detect listbox select and calling the function
        self.entry1.bind("<KeyRelease>", self.suggestion_class.on_type)
        self.listbox.bind("<<ListboxSelect>>", self.suggestion_class.on_select)
        
    #function responsible of adding and removing custom path entry and updating instance choice variable
    def path_fun(self,choice):
        if choice == 'Custom':
            self.label6.pack_forget()
            self.label4.pack_forget()
            self.label5.pack_forget()
            self.button1.pack_forget()
            self.entry2.pack(pady=5)
            self.button1.pack(pady=5)
            self.inst_choice = 1
            return
        self.label6.pack_forget()
        self.label4.pack_forget()
        self.label5.pack_forget()
        self.button1.pack_forget()
        self.entry2.pack_forget()
        self.button1.pack(pady=5)
        self.inst_choice = 0
    #img showing   
    def img_frame(self):
        self.label3 = ctk.CTkLabel(self.root,text="" ,image=ctk.CTkImage(light_image=img,dark_image=img, size=(200,200)))
        self.label3.pack(side='bottom')
    #to access entries text and packing/forgetting
    def get_entry1_text(self):
        return self.entry1.get()
    def get_entry2_text(self):
        return self.entry2.get()
    def label4_pack(self):
        self.label4.pack(pady=5)
    def label5_pack(self):
        self.label5.pack(pady=5)
    def label6_pack(self):
        self.label6.pack(pady=5)
    def label4_forget(self):
        self.label4.pack_forget()
    def label5_forget(self):
        self.label5.pack_forget()
    def label6_forget(self):
        self.label6.pack_forget()
    def entry2_pack(self):
        self.entry2.pack(pady=5)
    def label2_pack(self):
        self.label2.pack(pady=5)
    def button1_pack(self):
        self.button1.pack(pady=5)
    def button1_forget(self):
        self.button1.forget()
    def label2_forget(self):
        self.label2.forget()
    def entry2_forget(self):
        self.entry2.forget()
    def dropbox_forget(self):
        self.dropbox.forget()
    def dropbox_pack(self):
        self.dropbox.pack(pady=5)
    def entry1_clear(self):
        self.entry1.delete(0, tk.END)
    def entry1_adding_suggestion(self):
        self.entry1.insert(0, self.listbox.get(self.listbox.curselection()[0]))
    def listbox_selection_tupple(self):
        return self.listbox.curselection()
    def listbox_clear(self):
        self.listbox.delete(0,tk.END)
    def listbox_adding_suggestion(self):
        self.listbox.insert(tk.END, self.suggestion_class.item)
    def listbox_size(self):
        return self.listbox.size()
    def listbox_forget(self):
        self.listbox.forget()
    def listbox_pack(self):
        self.listbox.pack(pady=5)
    #gui mainloop    
    def run(self):
        self.root.mainloop()

#classes connections
obj_download = download()
obj_suggestion = suggestion()
obj_gui = gui(obj_download, obj_suggestion)
obj_download.gui_class = obj_gui
obj_suggestion.gui_class = obj_gui


#run
obj_gui.run()




