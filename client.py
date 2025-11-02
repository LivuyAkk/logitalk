from customtkinter import *
from PIL import Image
from socket import socket
import threading

window = CTk()
window.geometry("500x400")
window.title("LogiTalk")



menu_frame = CTkFrame(window, fg_color="blue", width=200)
menu_frame.pack_propagate(False)
menu_frame.pack(side=LEFT, fill="y")

username_label = CTkLabel(menu_frame,text="Ім'я",text_color="white")
username_label.pack(pady=10)

username = CTkEntry(menu_frame)
username.pack(pady=20)
username.insert(0, "Kostya")

image_label = CTkLabel(menu_frame, text="")
image_label.pack()

chat_frame = CTkFrame(window, fg_color="blue")
chat_frame.pack(side=LEFT, fill="both", expand=True)

chat_history = CTkScrollableFrame(chat_frame)
chat_history.pack(fill="both",expand=True)

chat_entry = CTkEntry(chat_frame, font=("Comic Sans MS",24))
chat_entry.pack(side=LEFT, fill="x", expand=True)

chat_button = CTkButton(chat_frame, text="Відправити", height=40)
chat_button.pack(side=LEFT)

def add_message(message):
    message_frame = CTkFrame(chat_history, fg_color="grey",
                             corner_radius=12)
    message_frame.pack(pady=5, fill="x")

    label = CTkLabel(message_frame, text=message, justify="left", font=("Arial",22),
                     text_color="white")
    label.pack(padx=10, fill="x", anchor="w")

def recv_message():
    while True:
        data = socket.recv(4096)
        if not data:
            break
        msg = data.decode()
        add_message(msg)
    socket.close()

def send_message():
    msg = username.get() + ": " + chat_entry.get()
    msg = msg.encode()
    socket.send(msg)
    chat_entry.delete(0, END)

    #ctk2 = CTk()
    #ctk2.title("Посхалка")
    #image = Image.open("s.jpg")
    #ctk_image = CTkImage(light_image=image,size=(100,100))
    #label = CTkLabel(ctk2, text="", image=ctk_image)
    #label.pack()
    

chat_button.configure(command=send_message)

try:
    socket = socket()
    socket.connect(("2.tcp.eu.ngrok.io", 17100))
    threading.Thread(target=recv_message, daemon=True).start()
except:
    add_message("Не вдалося під'єднатися до серверу")

window.mainloop()