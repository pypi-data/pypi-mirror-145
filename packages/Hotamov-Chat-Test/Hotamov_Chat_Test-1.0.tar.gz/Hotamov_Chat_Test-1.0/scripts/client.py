import socket, threading
import syslog, sys

join = False
shutdown = False
syslog.openlog(sys.argv[0])


# Функция получения сообщения пользователями
def receive_messages(name, socket_attr):
    while not shutdown:
        try:
            while True:
                message, user = socket_attr.recvfrom(1024)
                print(message.decode("utf-8"))
        except:
            pass


host = socket.gethostbyname(socket.gethostname())
port = 0
server = ("127.0.0.1", 8080)

new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
new_socket.bind((host, port))
new_socket.setblocking(0)

name = input("Name: ")
thr = threading.Thread(target=receive_messages, args=("RecvThread", new_socket))
thr.start()

# Передача сообщений
while not shutdown:
    if not join:
        new_socket.sendto(f"[{name}] joined the server".encode("utf-8"), server)
        join = True
    else:
        try:
            message = input()
            if message != '':
                try:
                    new_socket.sendto(f"[{name}]: {message}".encode("utf-8"), server)
                    print("Message delivered to client")
                    syslog.syslog(syslog.LOG_NOTICE, message)
                except:
                    print("Message delivery error")
        except:
            new_socket.sendto(f"[{name}] left the server".encode("utf-8"), server)
            shutdown = True

thr.join()
syslog.closelog()
new_socket.close()
