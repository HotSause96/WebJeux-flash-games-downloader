import requests
from bs4 import BeautifulSoup
from PIL import Image
import customtkinter as ctk
import os

ctk.set_appearance_mode("dark")
img = Image.open('flipline_studio.png')

class gui:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("WebJeux.com flash games downloader")
        self.root.geometry("480x550")
        self.root.resizable(False,False)
        self.inst_choice = 0

        self.user_com()
        self.img_frame()

    def body(self):
        self.un_gm_nm = self.entry1.get()
        self.un_gm_nm = self.un_gm_nm.lower()
        self.un_gm_nm = self.un_gm_nm.replace(" ","-")
        self.game_name = self.un_gm_nm
        print("game name : ",self.game_name)

        if self.inst_choice:
            self.custom_path = self.entry2.get()
            self.path = os.path.join(self.custom_path, self.game_name)
        else:
            self.path = 'C:\\Users\\HP\\Downloads\\flash games\\'+self.game_name
            
        r = requests.get("https://www.webjeux.com/jouer/"+self.game_name+".html")
        print("WebJeux status code : ",r.status_code)
        soup = BeautifulSoup(r.text, "html.parser")
        swfs = soup.find(attrs={"data":True})
        swf = swfs["data"]
        r2 = requests.get(swf)
        print("swf status code : ",r2.status_code)
        headers = r2.headers
        print("Content type : ",headers["Content-Type"])
        with open(self.path+'.swf','wb') as f:
            f.write(r2.content)
            print("Success")

    def user_com(self):
        self.label1 = ctk.CTkLabel(self.root, text='Welcome to WebJeux flash games.\nEnter game name :',font=ctk.CTkFont("arial black", 15))
        self.label1.pack(pady=15)

        self.entry1 = ctk.CTkEntry(self.root, placeholder_text="Start typing...", width=200)
        self.entry1.pack()

        self.label2 = ctk.CTkLabel(self.root, text='Select download path :\nThe game gonna be saved in flash games folder by default',font=ctk.CTkFont("arial black", 14))
        self.label2.pack(pady=20)

        self.dropbox = ctk.CTkOptionMenu(self.root,command=self.path_fun,text_color_disabled="gray",dropdown_font=("arial black", 12),font=("arial black", 14),button_hover_color='#9A4743',fg_color="#C1554F",button_color='#C1554F',width=200,corner_radius=10, values=["Default","Custom"])
        self.dropbox.pack()

        self.entry2 = ctk.CTkEntry(self.root, placeholder_text="Start typing...",width=200)
   
        self.button1 = ctk.CTkButton(self.root,command=self.body, text='Download', corner_radius=15, fg_color='#F7494B',hover_color='#C90E0E',text_color='#171519',border_width=2,width=200,height=50,font=ctk.CTkFont("arial black", 20))
        self.button1.pack(pady=20)
        
    
    def path_fun(self,choice):
        if choice == 'Custom':
            self.button1.pack_forget()
            self.entry2.pack(pady=15)
            self.button1.pack()
            self.inst_choice = 1
            return
        self.button1.pack_forget()
        self.entry2.pack_forget()
        self.button1.pack(pady=20)
        self.inst_choice = 0
        
    def img_frame(self):
        self.label3 = ctk.CTkLabel(self.root,text="" ,image=ctk.CTkImage(light_image=img,dark_image=img, size=(200,200)))
        self.label3.pack(side='bottom')
        
        
if __name__ == "__main__":
    app = gui()
    app.root.mainloop()
