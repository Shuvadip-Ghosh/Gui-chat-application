import socket
import threading
import tkinter
from tkinter import scrolledtext
from tkinter import simpledialog,Frame,Text,PhotoImage
import customtkinter
import time
from data import get_credentials,get_Theme 
# host = '10.0.0.5'
host = 'localhost'
# host = '127.0.0.1'
port = 9090
# host = "0.tcp.in.ngrok.io"
# port = 16976
class Client:
    def __init__(self,host,port) :
        self.persons = []
        # self.nickname = "Shuvadip Ghosh"
        file = open('username.txt','r')
        content = file.read()
        file.close()
        if content == "":
            msg = tkinter.Tk()
            msg.withdraw()
            self.nickname = simpledialog.askstring("Nickname", "Please enter a Nickname", parent=msg)
            file = open('username.txt','w')
            file.write(self.nickname)
            file.close()
        else:
            self.nickname = content
        self.gui_done = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))
        time.sleep(0.5)
        message = self.sock.recv(1024)    
        self.sock.send(self.nickname.encode('utf-8')) 
        
        persons = self.sock.recv(10240)
        persons = persons.decode('utf-8')
        persons = persons[4:]
        persons = eval(persons)

        self.premsg = self.sock.recv(65535)
        self.premsg = self.premsg.decode('utf-8')
        self.premsg = self.premsg[6:]
        self.premsg = eval(self.premsg)

        gui_thread = threading.Thread(target=self.gui_loop)
        previous_ms = threading.Thread(target=self.prevoius_msg)
        receive_thread = threading.Thread(target=self.receive)
        
        self.running = True
        gui_thread.start()
        time.sleep(1)
        self.person_updater(persons)
        previous_ms.start()
        receive_thread.start()

    def gui_loop(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.app = customtkinter.CTk()
        self.app.geometry("1000x520")
        
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self.app, width=300)
        self.frame_left.grid(row=0, column=0, sticky="nswe", pady=20)

        self.frame_right = customtkinter.CTkFrame(master=self.app)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ================left frame=============
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.person_label = customtkinter.CTkLabel(master=self.frame_left,text="People In Chat",text_font=("Roboto Medium", -16))  # font name and size in px
        self.person_label.grid(row=1, column=0, pady=10, padx=10)

        self.person_list = customtkinter.CTkTextbox(master=self.frame_left,height=400,corner_radius=6,fg_color=("white", "gray38"))
        self.person_list.grid(column=0, row=2, sticky="nswe", padx=15, pady=15)
        self.person_list.configure(state="disabled",text_font=("Roboto Medium", 12))

        # ===============right frame===============
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_msg = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_msg.grid(row=1, column=0, sticky="nswe",padx=15, pady=15)

        self.msg_container= customtkinter.CTkTextbox(master=self.frame_right,height=370,corner_radius=6,fg_color=("white", "gray38"))
        self.msg_container.grid(column=0, row=0, sticky="nswe", padx=15, pady=15)
        self.msg_container.configure(state="disabled",text_font=("Roboto Medium", 12))

        self.msg_box = customtkinter.CTkEntry(master=self.frame_msg,width=500,placeholder_text="Type Your Message")
        self.msg_box.grid(column=0, row=0, sticky="nswe",pady=12, padx=10)


        self.button_5 = customtkinter.CTkButton(master=self.frame_msg, text="Send",border_width=2,fg_color=None,command=self.write)
        self.button_5.grid(row=0, column=1,pady=12, padx=10, sticky="we")

        self.gui_done = True
        self.app.mainloop()
        self.running = False
        if self.net:
            self.sock.close()
    def write(self):
        data = self.msg_box.get()
        if len(data.replace(" ","")) !=0:
            message = f"{self.nickname}: {data}\n"
            self.msg_box.delete(0,tkinter.END)
            self.msg_box.deactivate_placeholder()
            self.sock.send(message.encode('utf-8'))
        else:
            self.msg_box.delete(0,tkinter.END)
            self.msg_box.deactivate_placeholder()
    def prevoius_msg(self):
        while True:
            if self.gui_done:
                try:
                    for msg in self.premsg:
                        message = msg[0]+':'+msg[1]+'\n'
                        self.msg_container.configure(state="normal")
                        self.msg_container.insert(tkinter.END, message)
                        self.msg_container.configure(state="disabled")
                    self.premsg= []
                except Exception as e:
                    print(e)
                break
    def person_updater(self,message):
        if self.gui_done:
            self.person_list.configure(state="normal")
            self.person_list.textbox.delete('1.0', tkinter.END)
            for mess in message:
                mess = mess+"\n"
                # print(mess)
                self.person_list.insert(tkinter.END, mess)
            self.person_list.configure(state="disabled")
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                message = message.decode('utf-8')
                if self.gui_done:
                    if message.startswith("list ["):
                        message = message[4:]
                        message = eval(message)
                        self.person_updater(message)
                    else:
                        self.msg_container.configure(state="normal")
                        self.msg_container.insert(tkinter.END, message)
                        self.msg_container.configure(state="disabled")
            except ConnectionAbortedError:
                break
            except:
                print('error')
                self.sock.close()
                break

client = Client(host=host,port=port)
