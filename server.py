import socket
import threading
host = '127.0.0.1'
port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            print(message.decode('utf-8'))
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            print("{} left the chat".format(nickname))
            nick = "list "+str(nicknames)
            broadcast(nick.encode('utf-8'))
            print(f"{nick}\nsent")
            break
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        print("asked nickname")
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        nick = "list "+str(nicknames)
        client.send(nick.encode('utf-8'))
        broadcast(nick.encode('utf-8'))
        print(f"{nick}\nsent")

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()

