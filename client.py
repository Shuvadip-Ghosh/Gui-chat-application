import socket
import threading
import tkinter
from tkinter import scrolledtext
from tkinter import simpledialog
import os
import time

host = '127.0.0.1'
port = 9090

class Client:
    def __init__(self,host,port) :
        
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

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        
        self.running = True
        gui_thread.start()  
        receive_thread.start()
                                                      
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg = "black")
        self.win.title(self.nickname)
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="black")
        self.chat_label.configure(font=("Arial",12))
        self.chat_label.pack(padx=20, pady=5)


        self.textarea = tkinter.scrolledtext.ScrolledText(self.win)
        self.textarea.pack(padx=20, pady=5)
        self.textarea.config(state='disabled')

        self.msglabel = tkinter.Label(self.win, text="Message:", bg="black")
        self.msglabel.configure(font=("Arial",12))
        self.msglabel.pack(padx=20, pady=5)

        self.inputarea = tkinter.Text(self.win, height=3)
        self.inputarea.pack(padx=20, pady=5)

        self.sendbutton= tkinter.Button(self.win, text="send", command=self.write)
        self.sendbutton.config(font=("Arial",12))
        self.sendbutton.pack(padx=20,pady=5)

        self.gui_done = True

        self.win.protocol("WN_DELETE_WINDOW", self.stop)
        self.win.mainloop()


    def write(self):
        input_area = self.inputarea.get('1.0','end')
        input_area = input_area.rstrip("\n")
        if input_area != "\n":
            message = f"{self.nickname}: {input_area}\n"
            self.sock.send(message.encode('utf-8'))
            self.inputarea.delete('1.0','end')
        else:
            pass
    
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        print("stopped")
        os._exit(0)
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if self.gui_done:
                    self.textarea.config(state='normal')
                    self.textarea.insert('end',message.decode('utf-8'))
                    self.textarea.yview('end')
                    self.textarea.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print('error')
                self.sock.close()
                break

client = Client(host=host,port=port)
