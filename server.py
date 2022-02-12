import socket
import threading

host = '127.0.0.1'  # localhost
port = 9090  # free port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating socket
server.bind((host, port))  # connecting
server.listen()

clients = []  # use to store clients
usernames = []  # use to store nicknames


def display(mess):
    for each in clients:
        each.send(mess)  # sending for each client


def treatment(client):  # treatment messages
    while True:
        try:
            mess = client.recv(1024)  # receive message
            display(mess)  # displaying message
        except:
            username = usernames[clients.index(client)]  # returning value of nickname for the client
            clients.remove(client)  # deleting client
            client.close()  # close session for the client
            display('{} left this chat'.format(username).encode("ascii"))  # displaying message
            usernames.remove(username)  # deleting nickname
            break


def get_message():
    while True:
        connection, address = server.accept()  # accept a connection
        print('Connected: {}'.format(str(address)))  # connecting message
        connection.send('name'.encode('ascii'))  # request username
        username = connection.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(connection)  # add client
        print('Username is {}'.format(username))
        display('{} joined this chat'.format(username).encode("ascii"))  # displaying 'join' message
        connection.send('Connected to chat!'.encode('ascii'))
        thread = threading.Thread(target=treatment, args=(connection,))  # generating thread
        thread.start()


get_message()
