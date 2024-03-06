def send_msg(client_socket, message):
    client_socket.send(message.encode('utf-8'))


def request_msg(client_socket):
    request = client_socket.recv(1024)
    return request.decode('utf-8')
