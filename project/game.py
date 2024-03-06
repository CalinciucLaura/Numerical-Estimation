def select_game_mode(request):

    if (str(request) == '1'):
        print("Single player")
        game_mode = 1
    elif (str(request) == '2'):
        print("Multi player")
        game_mode = 2
    else:
        print("Wrong input")
        game_mode = 3
    return str(game_mode)


def menu():
    menu_text = "Alege o optiune:" + "\n"
    menu_text += "1. Single player" + "\n"
    menu_text += "2. Multi player" + "\n"
    menu_text += "3. Exit" + "\n"
    return menu_text
