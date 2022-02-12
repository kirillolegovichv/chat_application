import socket
import threading

username = input('Enter your name: ')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating socket
sock.connect(('127.0.0.1', 9090))


def receive():
    while True:
        try:
            message = sock.recv(1024).decode('ascii')
            if message == 'name':
                sock.send(username.encode('ascii'))
            else:
                print(message)
        except:
            print('Error!')
            sock.close()
            break


def write():
    while True:
        message = '{}: {}'.format(username, input(""))
        sock.send(message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
