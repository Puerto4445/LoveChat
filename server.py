#!/usr/bin/python
import socket
import threading

def client_thread(client_socket,client,usernames):

    username = client_socket.recv(1024).decode()
    usernames[client_socket]=username
    
    print(f"\n[+] El usuario {username} se ha conectado al chat\n\n")

    for i in client:
        if i is not client_socket:
            i.sendall(f"\n[+] El usuario {username} ha entrado al chat\n\n".encode())

    while True:
        try:
            message= client_socket.recv(1024).decode()

            if not message:
                break

            if message == "usuarios!":
                client_socket.sendall(f"\n[!]Lista de Usuarios conectados: {', '.join(usernames.values())}\n\n".encode())
                continue

            for i in client:
                if i is not client_socket:
                    i.sendall(f"{message}\n".encode())

        except:
            break
    client_socket.close()
    client.remove(client_socket)
    del usernames[client_socket]

def server_program():
    host = 'localhost'
    port = 5555
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) #TIME WAIT
    server.bind((host,port))
    server.listen()

    client =[]
    usernames={}

    while True:
        client_socket,addr = server.accept()
        client.append(client_socket)
        print(f"Se ha conectado un nuevo cliente: {addr}")

        thread = threading.Thread(target=client_thread, args=(client_socket,client,usernames))
        thread.deamon = True
        thread.start()
        


if __name__ == '__main__':
    server_program()
