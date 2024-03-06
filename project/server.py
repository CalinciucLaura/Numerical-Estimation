import socket
import threading
from client_number import ClientNumber
from game import select_game_mode
import random
import time
import uuid
from game_single_player import SinglePlayerGame
from game_multi_player import MultiPlayerGame


def send_msg(client_socket, message):
    client_socket.send(message.encode('utf-8'))


def request_msg(client_socket):
    request = client_socket.recv(1024)
    return request.decode('utf-8')


client_list = []


def handle_client(client_socket, addr, id_client):
    global client_list
    x = None
    client_in_game = True

    while True:
        request = request_msg(client_socket)

        if request == "Option:1":
            game_mode = select_game_mode(request.split(":")[1])
            print("Game mode: " + game_mode)
            if game_mode == "1":
                game = SinglePlayerGame(client_socket, id_client)
                game.play()
            continue

        if request == "Option:2":
            client_list.append(client_socket)
            game_mode = select_game_mode(request.split(":")[1])
            print("Game mode: " + game_mode)
            if len(client_list) < 2:
                send_msg(client_socket, "WAIT: Waiting for another player!")
                return
            if game_mode == "2":
                game = MultiPlayerGame(
                    client_list[0], client_list[1])
                client_list.pop(0)
                client_list.pop(0)
                game.play()
            continue

        if request == "Option:3":
            print("Client " + str(id_client) + " disconnected!")
            client_socket.close()
            return

    client_socket.close()


def server_program():
    host = "127.0.0.1"
    port = 50000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    server.settimeout(1)

    print("Server started!")
    print("Waiting for clients...")

    game_mode = None
    number = None

    try:
        while True:
            try:
                client, addr = server.accept()
                id_client = uuid.uuid1()
                print(f"Client {id_client} connected!")
                client_handler = threading.Thread(
                    target=handle_client, args=(client, addr, id_client))
                client_handler.start()
            except socket.timeout:
                pass
    except KeyboardInterrupt:
        print("Stopping server...")
        client_number = 0
        server.close()


server_program()
