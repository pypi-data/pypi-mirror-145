import socket, time

# Запуск сервера
host = socket.gethostbyname(socket.gethostname())
port = 8080
new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
new_socket.bind((host, port))
print("Binding successful!")
print("Server running on IP address: ", host)
clients = []

# Алгоритм работы сервера (отправка, приём сообщений)
while True:
    try:
        message, user = new_socket.recvfrom(1024)
        if user not in clients:
            clients.append(user)

        event_time = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        print(f"{user[0]} {user[1]} {event_time}")
        print(message.decode('utf-8'))

        for client in clients:
            if user != client:
                try:
                    new_socket.sendto(message, client)
                    print("Message delivered to client")
                except:
                    print("Message delivery error")

    except:
        print("Server stopped")
        new_socket.close()
        break
