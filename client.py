import socket
import threading
import tkinter
from tkinter import scrolledtext
from tkinter import simpledialog,Frame,Text,PhotoImage
import os
import time
import sys
host = '127.0.0.1'
port = 9090

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
        self.win = tkinter.Tk()
        self.win.configure(bg="black")
        self.win.title(self.nickname)
        self.personframe = Frame (self.win,bg="black")
        self.personframe.pack(side="left", anchor="nw")
        self.chat_label = tkinter.Label(self.personframe, text="People in this chat", bg="black", fg="white")
        self.chat_label.configure(font=("Arial",12))
        self.chat_label.pack(padx=20, pady=5)

        
        self.person_l = Text(self.personframe,bg="black",fg="white")
        self.person_l.config(state='disabled',height=1,width=50)
        self.person_l.pack()


        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="black", fg="white")
        self.chat_label.configure(font=("Arial",12))
        self.chat_label.pack(padx=20, pady=5)

        self.textarea = tkinter.scrolledtext.ScrolledText(self.win,bg="black", fg="white")
        self.textarea.pack(padx=20, pady=5)
        self.textarea.config(state='disabled')

        self.msglabel = tkinter.Label(self.win, text="Message:", bg="black", fg="white")
        self.msglabel.configure(font=("Arial",12))
        self.msglabel.pack(padx=20, pady=5)

        self.input_frame = Frame(self.win, bg="black")
        self.input_frame.pack(padx=20,pady=5)

        self.inputarea = tkinter.Text(self.input_frame, height=3,bg="black", fg="white",width=72)
        self.inputarea.pack(padx=20, pady=5,side="left")

        self.send_img= PhotoImage(file="images/send.png")
        self.sendbutton= tkinter.Button(self.input_frame,borderwidth=0, image=self.send_img ,bg="black", fg="white",command=self.write)
        self.sendbutton.config(font=("Arial",12))
        self.sendbutton.pack(padx=20,pady=5,side="left")

        self.gui_done = True
        self.win.mainloop()
        self.running = False
        self.sock.close()
        self.win.destroy()
        self.sock.close()
        self.win.destroy()

    def write(self):
        input_area = self.inputarea.get('1.0','end')
        input_area = input_area.rstrip("\n")
        if input_area != "\n":
            message = f"{self.nickname}: {input_area}\n"
            self.sock.send(message.encode('utf-8'))
            self.inputarea.delete('1.0','end')
        else:
            pass
    def prevoius_msg(self):
        while True:
            if self.gui_done:
                try:
                    for msg in self.premsg:
                        message = msg[0]+':'+msg[1]+'\n'
                        self.textarea.config(state='normal')
                        self.textarea.insert('end',message)
                        self.textarea.yview('end')
                        self.textarea.config(state='disabled')
                    self.premsg= []
                except Exception as e:
                    print(e)
                break
    def person_updater(self,message):
        if self.gui_done:
            self.person_l.config(height=len(message),state="normal")
            self.person_l.delete('1.0','end')
            for mess in message:
                mess = mess+"\n"
                # print(mess)
                self.person_l.insert('end',mess)
            self.person_l.config(state="disabled")
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
                        self.textarea.config(state='normal')
                        self.textarea.insert('end',message)
                        self.textarea.yview('end')
                        self.textarea.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print('error')
                self.sock.close()
                break

client = Client(host=host,port=port)
