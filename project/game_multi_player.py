from communication_utils import send_msg, request_msg
from client_number import ClientNumber


class MultiPlayerGame():
    def __init__(self, client_socket_1, client_socket_2):
        self.client_1 = client_socket_1
        self.client_2 = client_socket_2

        send_msg(self.client_1, "STOP WAIT: Set a number")
        send_msg(self.client_2, "WAIT: Wait for the other player to set a number")

    def play(self):
        request = request_msg(self.client_1)
        number_to_be_guessed = int(request)
        print(f"Number to be guessed: {number_to_be_guessed}")
        player_2 = ClientNumber(number_to_be_guessed)
        send_msg(self.client_2, "STOP WAIT: Client 1 set a number")
        while True:
            c2guess = request_msg(self.client_2)
            c2guess = int(c2guess)
            print(f"Client 2 guessed: {c2guess}")
            response = player_2.validation(c2guess)

            if response == "Server:Correct!":
                score = player_2.get_step()
                send_msg(self.client_2, f"{response}{score}")
                send_msg(self.client_1, f"RESTART: {response} Score: {score}")
                return
            else:
                send_msg(self.client_2, response)
                send_msg(self.client_1,
                         f"WAIT: Client 2 guessed {c2guess} -> {response}")
