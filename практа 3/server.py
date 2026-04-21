import threading
import socket

clients = []
nicknames = []
lock = threading.Lock()

def broadcast(message, sender_socket=None):
    """Отправить сообщение всем клиентам, кроме отправителя"""
    with lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    if client in clients:
                        clients.remove(client)

def handle_client(client_socket, client_addr):
    """Обработка сообщений от одного клиента"""
    # Получаем никнейм
    try:
        nickname = client_socket.recv(1024).decode('utf-8')
    except:
        client_socket.close()
        return

    with lock:
        nicknames.append(nickname)
        clients.append(client_socket)

    # Приветствие новому клиенту
    welcome = f"Добро пожаловать в чат, {nickname}!"
    client_socket.send(welcome.encode('utf-8'))
    
    # Оповещаем всех остальных о новом участнике
    broadcast(f"{nickname} присоединился к чату!", client_socket)
    print(f"{nickname} ({client_addr}) присоединился к чату")

    # Приём сообщений от клиента
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message or message.lower() == '/exit':
                break
            
            print(f"{nickname}: {message}")
            # Рассылаем сообщение всем остальным клиентам
            broadcast(f"{nickname}: {message}", client_socket)
            
        except:
            break

    # Клиент отключается
    with lock:
        if client_socket in clients:
            clients.remove(client_socket)
        if nickname in nicknames:
            nicknames.remove(nickname)
    
    client_socket.close()
    broadcast(f"{nickname} покинул чат!")
    print(f"{nickname} ({client_addr}) отключился")

# Настройка сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("127.0.0.1", 5000))
server_socket.listen()

print("Сервер запущен на 127.0.0.1:5000")
print("Ожидание подключений...")

# Приём клиентов
while True:
    client_socket, client_addr = server_socket.accept()
    print(f"Новое подключение от {client_addr}")
    
    # Запускаем поток для клиента
    thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
    thread.daemon = True
    thread.start()