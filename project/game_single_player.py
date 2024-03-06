from communication_utils import send_msg, request_msg
from client_number import ClientNumber
import random


class SinglePlayerGame():
    def __init__(self, client_socket, id_client):
        self.id_client = id_client
        self.client = client_socket
        self.numer_to_be_guessed = random.randint(0, 50)
        print(f"Number to be guessed: {self.numer_to_be_guessed}")
        send_msg(self.client, "Server:Start!")
        self.player = ClientNumber(self.numer_to_be_guessed)

    def play(self):
        while True:
            request = request_msg(self.client)

            request = int(request)
            response = self.player.validation(request)

            if response == "Server:Correct!":
                score = self.player.get_step()
                print(f"Client {self.id_client} won! Score: {score}")
                send_msg(self.client, f"{response}{score}")
                return
            else:
                send_msg(self.client, response)
