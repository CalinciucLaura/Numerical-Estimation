class ClientNumber:

    def __init__(self, guess):
        self.numer_to_be_guessed = guess
        self.step = 1

    def validation(self, given_number):

        if given_number < 0 or given_number > 50:
            return "Server:Number must be between 0 and 50!"
        try:
            if self.numer_to_be_guessed > given_number:
                self.step += 1
                return "Server:Higher"
            elif self.numer_to_be_guessed < given_number:
                self.step += 1
                return "Server:Lower"
            else:
                return "Server:Correct!"
        except TypeError:
            return "Missing arguments"
        except ValueError:
            return "You must send an integer!"

    def get_step(self):
        return self.step
