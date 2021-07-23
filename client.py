#coding:utf-8
from tkinter.constants import X
from functions import addMessage, getMessages
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = 'localhost'
PORT = 9090

class Client:

    
    def __init__(self, host, port, nickname):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))

        self.nickname = nickname
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        reveive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        reveive_thread.start()
    
    def gui_loop(self):
        if self.nickname:
            self.win = tkinter.Tk()
            self.win.config(bg='lightblue')
            self.win.title(self.nickname)
            
            self.chat_label = tkinter.Label(self.win, text='Chat:', bg='lightblue')
            self.chat_label.config(font=("Arial", 12))
            self.chat_label.pack(padx=20, pady=5)

            self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
            self.text_area.insert(tkinter.INSERT, getMessages())
            self.text_area.pack(padx=20, pady=5)
            self.text_area.config(state='disabled')
            


            self.msg_label = tkinter.Label(self.win, text='Message:', bg='lightblue')
            self.msg_label.config(font=("Arial", 12))
            self.msg_label.pack(padx=20, pady=5)

            self.input_area = tkinter.Entry(self.win)
            self.input_area.pack(padx=20, pady=5)

            self.send_button = tkinter.Button(self.win, text='Envoyer', command=self.write)
            self.send_button.config(font=('Arial',12))
            self.send_button.pack(padx=20, pady=5)

            self.gui_done = True

            self.win.protocol('WM_DELETE_WINDOW', self.stop)
            
            self.win.mainloop()
        

    def write(self):
        if self.input_area.get() != '':
            message = f"{self.nickname}: {self.input_area.get()}\n"
            addMessage(f"{self.nickname}: {self.input_area.get()}\n")
            self.sock.send(message.encode('utf-8'))
            self.input_area.delete(0, tkinter.END)
            self.input_area.insert(0, '')
      
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)


    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        from config import nicknames
                        self.text_area.config(state='normal')
                        for nickname in nicknames:
                            if nickname == self.nickname:
                                messages = message.split(':')
                                message = ':'.join('moi',messages[1])
                                break
                        print(message)
                        
                        self.text_area.insert('end', message)
                        
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
                    
            except ConnectionAbortedError:
                break
            except:
                print('Erreur')
                self.sock.close()
                break

msg = tkinter.Tk()
msg.withdraw()
nickname = simpledialog.askstring("Pseudo","Donner votre pseudo svp",parent=msg)
if nickname:
    client = Client(HOST, PORT, nickname)
else:
    msg.destroy()