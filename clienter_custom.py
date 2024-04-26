#!/usr/bin/python
import socket
import threading
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as tb
from tkinter import ttk


def recive_message(text_scroll, client_socket):
    """
    Function to receive and display messages from the server
    """
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            text_scroll.configure(state="normal")
            text_scroll.insert(END, message)
            text_scroll.configure(state="disabled")

        except:
            break


def send_message(event, client_socket, username, text_scroll, text_box):
    """
    Function to send messages to the server
    """
    message = text_box.get()
    client_socket.sendall(f"<{username}> {message}".encode())

    text_box.delete(0, END)
    text_scroll.configure(state="normal")
    text_scroll.insert(END, f"<{username}> {message}\n")
    text_scroll.configure(state="disabled")


def list_user_request(client_socket):
    """
    Function to request the list of users from the server
    """
    client_socket.sendall(f"usuarios!".encode())


def exit_chat(client_socket, username, root):
    """
    Function to exit the chat room
    """
    client_socket.sendall(
        f"\n[!] El usuario '{username}' ha abandonado la sala\n".encode()
    )
    client_socket.close()

    root.quit()
    root.destroy()


def client_program():
    host = "localhost"
    port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    username = input(f"[+] Ingresar un usuario: ")
    client_socket.sendall(username.encode())
    
    root = tb.Window(themename = "solar")
    root.title("LoveChat")
    root.resizable(True,True)
    text_scroll = ScrolledText(root,state="disabled")
    text_scroll.pack(fill=BOTH,padx=5, pady=5)


    frame_box = Frame(root)
    frame_box.pack(fill=BOTH, padx=5, pady=5,expand=True)

    button_send = Button(
        frame_box,
        text="Enviar",
        command=lambda: send_message(
            None, client_socket, username, text_scroll, text_box
        ),
    )
    button_send.pack(side=RIGHT, padx=5)

    button_list = Button(
        frame_box, text="Usuarios", command=lambda: list_user_request(client_socket)
    )
    button_list.pack(side=RIGHT)

    text_box = Entry(frame_box, font=("Arial", 14))
    text_box.bind(
        "<Return>",
        lambda event: send_message(
            event, client_socket, username, text_scroll, text_box
        ),
    )
    text_box.pack(side=LEFT, fill=BOTH, pady=5, expand=True)

    button_exit = Button(
        root, text="Quit", command=lambda: exit_chat(client_socket, username, root)
    )
    button_exit.pack(pady=5, padx=5)

    thread = threading.Thread(target=recive_message, args=(text_scroll, client_socket))
    thread.daemon = True
    thread.start()

    root.mainloop()
    client_socket.close()


if __name__ == "__main__":
    client_program()
