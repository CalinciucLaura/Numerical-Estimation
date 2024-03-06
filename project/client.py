import socket
import threading
from game import menu
import time

start_the_game = True
is_in_wait_state = False
restart_loop = False


def send_msg(client_socket, message):
    client_socket.send(message.encode('utf-8'))


def receive_msg(client_socket):
    try:
        while True:
            receive = client_socket.recv(1024)
            server_message = receive.decode('utf-8')
            if server_message is not None:
                return server_message
    except ConnectionResetError:
        print("Server disconnected!")
        exit()
    except ConnectionAbortedError:
        print("Server disconnected!")
        exit()


def handle_server_message(msg):
    global is_in_wait_state, restart_loop
    if msg.startswith("WAIT: "):
        is_in_wait_state = True
        print(msg[len("WAIT: "):])

    elif msg.startswith("STOP WAIT: "):
        is_in_wait_state = False
        print(msg[len("STOP WAIT: "):])

    elif msg.startswith("RESTART: "):
        print(msg[len("RESTART: "):])
        restart_loop = True

    else:
        print(msg)


def client_program():

    host = "127.0.0.1"
    port = 50000

    global start_the_game, is_in_wait_state, restart_loop

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server!")

    while True:
        if restart_loop == True:
            break
        try:
            if start_the_game == True:
                start_the_game = False
                print(menu())
                message = "Option:"
                message += input("Choose the game mode: ")

                if message == "Option:3":
                    print("Goodbye!")
                    send_msg(client_socket, message)
                    return

                if message != "Option:1" and message != "Option:2":
                    print("Invalid option!")
                    start_the_game = True
                    continue

                send_msg(client_socket, message)
                server_message = receive_msg(client_socket)
                handle_server_message(server_message)
            else:
                if server_message == "[Server]Set a number":
                    message = input("Enter a number: ")
                    send_msg(client_socket, message)
                    server_message = receive_msg(client_socket)
                elif server_message == "Server:Wait!":
                    message = ""
                    send_msg(client_socket, message)

                elif is_in_wait_state == True:
                    server_message = receive_msg(client_socket)
                    handle_server_message(server_message)
                    continue

                else:
                    message = input("Enter the value: ")
                    if message == "" or message.isalpha():
                        print("Invalid input!")
                        continue

                    send_msg(client_socket, message)
                    server_message = receive_msg(client_socket)

                if server_message.startswith("Server:Correct!"):
                    score = server_message[len("Server:Correct!"):]
                    print("YOU WON! SCORE:", str(score))
                    start_the_game = True
                else:
                    handle_server_message(server_message)

            server_message = None
        except ConnectionResetError:
            print("Server disconnected!")
            exit()
        except KeyboardInterrupt:
            print("Client disconnected!")
            exit()

    client_socket.close()

    if restart_loop == True:
        restart_loop = False
        start_the_game = True
        is_in_wait_state = False
        client_program()


client_program()
