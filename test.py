self.win = tkinter.Tk()
self.win.configure(bg="black")
self.win.title("tits")
self.personframe = Frame (self.win,bg="black")
self.personframe.pack(side="left", anchor="nw")
self.chat_label = tkinter.Label(self.personframe, text="People in this chat", bg="black", fg="white")
self.chat_label.configure(font=("Arial",12))
self.chat_label.pack(padx=20, pady=5)

for self.person in self.persons:
    self.person_l = Text(self.personframe,bg="black",fg="white")
    self.person_l.insert('end',self.person)
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

self.inputarea = tkinter.Text(self.win, height=3,bg="black", fg="white")
self.inputarea.pack(padx=20, pady=5)

self.sendbutton= tkinter.Button(self.win, text="send",bg="black", fg="white")
self.sendbutton.config(font=("Arial",12))
self.sendbutton.pack(padx=20,pady=5)
                
self.gui_done = True

self.win.protocol("WN_DELETE_WINDOW", self.stop)
self.win.mainloop()      
