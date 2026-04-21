import socket
import threading

def receive_messages(client_socket):
    """Поток для получения сообщений от сервера"""
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"\n{data}")
            print("Вы: ", end="", flush=True)
        except:
            print("\nСоединение с сервером потеряно")
            break

def send_messages(client_socket):
    """Поток для отправки сообщений на сервер"""
    while True:
        message = input("Вы: ")
        if message.lower() == '/exit':
            client_socket.send(message.encode('utf-8'))
            break
        if message:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                print("Не удалось отправить сообщение")
                break

# Подключение к серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 5000))

# Получение ника
nickname = input("Введите ваш ник: ")
client_socket.send(nickname.encode('utf-8'))

print("Подключено к чату!")
print("Для выхода введите /exit\n")

# Запуск потоков
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.daemon = True
receive_thread.start()

send_messages(client_socket)

# Закрытие соединения
client_socket.close()
print("Вы вышли из чата")