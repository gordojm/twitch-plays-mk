import socket
import pyautogui
import threading
import twitch_settings
from threading import Timer


SERVER = 'irc.twitch.tv'
PORT = 6667
OAUTH_KEY = twitch_settings.OAUTH_KEY
BOT = 'JeffazosPlaysMK11'
CHANNEL = 'albastter'
OWNER = 'albastter'
irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(('PASS ' + OAUTH_KEY + '\n' + 'NICK ' + BOT +
          '\n' + 'JOIN #' + CHANNEL + '\n').encode())
message = ''
timers = {}

blocking_state = False
#### CONTROLES DEL JUEGO ####


def game_control():
    global blocking_state
    global message
    while True:
        # if 'tag' in message.lower():
        #     pyautogui.keyDown('-')
        #     message = ''
        #     pyautogui.keyUp('-')
        #### KOMBATE BASICO ####

        # if 'block' in message.lower():
        #     blocking_state = True
        #     message = ''
        #     pyautogui.keyDown('o')

        if 'throw' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('space')
            message = ''
            pyautogui.keyUp('space')

        # elif 'block' in message.lower():
        #     apretar_tecla('o', 2)
        #     message = ''

        elif '1' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('j')
            message = ''
            pyautogui.keyUp('j')

        elif '2' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('i')
            message = ''
            pyautogui.keyUp('i')

        elif '3' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('k')
            message = ''
            pyautogui.keyUp('k')

        elif '4' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('l')
            message = ''
            pyautogui.keyUp('l')

        elif 'int' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('p')
            message = ''
            pyautogui.keyUp('p')

        #### MOVIMIENTO BASICO ####
        if 'up' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('up')
            message = ''
            pyautogui.keyUp('up')

        elif 'down' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('down')
            message = ''
            pyautogui.keyUp('down')

        elif 'left' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('left')
            message = ''
            pyautogui.keyUp('left')

        elif 'right' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('right')
            message = ''
            pyautogui.keyUp('right')

        elif 'flip' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('u')
            message = ''
            pyautogui.keyUp('u')

        #### MOVIMIENTO AVANZADO ####
        elif 'rj' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('right')
            pyautogui.keyDown('up')
            message = ''
            pyautogui.keyUp('right')
            pyautogui.keyUp('up')
            # pyautogui.hotkey('up', 'right')

        elif 'lj' in message.lower():
            if blocking_state:
                cancel_block()
            pyautogui.keyDown('left')
            pyautogui.keyDown('up')
            message = ''
            pyautogui.keyUp('left')
            pyautogui.keyUp('up')
            # pyautogui.hotkey('up', 'left')

        # elif 'dr' in message.lower():
        #     pyautogui.hotkey('right', 'right')

        # elif 'dl' in message.lower():
        #     pyautogui.hotkey('left', 'left')

        #### KOMBATE AVANZADO ####
        elif 'fatal' in message.lower():
            if blocking_state:
                cancel_block()
            # pyautogui.hotkey('o', 'u')
            pyautogui.keyDown('o')
            pyautogui.keyDown('u')
            message = ''
            pyautogui.keyUp('o')
            pyautogui.keyUp('u')

        elif 'status' in message.lower():
            print(blocking_state)
            message = ''

        else:
            pass


def apretar_tecla(tecla, tiempo):
    pyautogui.keyDown(tecla)

    def soltar_tecla(tecla):
        # time.sleep(2)
        pyautogui.keyUp(tecla)

    if timers.get(tecla) is not None:
        timers[tecla].cancel()

    timers[tecla] = Timer(tiempo, soltar_tecla(tecla))


def cancel_block():
    pyautogui.keyUp('o')
    blocking_state = False

#### FUNCIONES PARA TWITCH ####


def twitch():
    def join_chat():    # Unirse al chat
        Loading = True
        while Loading:
            readbuffer_join = irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split('\n')[0:-1]:
                print(line)
                loading_complete(line)
                Loading = loading_complete(line)

    def loading_complete(line):     #
        if'End of /NAMES list' in line:
            print('Bot correctamente conectado al canal ' + CHANNEL)
            send_message(irc, 'Bot conectado al chat')
            return False
        else:
            return True

    def send_message(irc, message):
        message_temp = 'PRIVMSG #' + CHANNEL + ' :' + message
        irc.send((message_temp + '\n').encode())
        print(message_temp)

    def get_user(line):
        separate = line.split(':', 2)
        user = separate[1].split('!', 1)[0]
        # print(user)
        return user

    def get_message(line):
        global message
        try:
            message = (line.split(':', 2))[2]
            return message
            # print(message)
        except:
            message = ''

    def Console(line):
        if 'PRIVMSG' in line:
            return False
        else:
            return True

    join_chat()

    while True:
        try:
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer = ''
        for line in readbuffer.split('\n\n'):
            if line == '':
                continue
            elif 'PING' in line and Console(line):
                msgg = 'PONG tmi.twitch.tv\r\n'.encode()
                irc.send(msgg)
                print(msgg)
                continue
            else:
                print(line)
                user = get_user(line)
                message = get_message(line)
                print(user + ': ' + message)


if __name__ == "__main__":
    t1 = threading.Thread(target=twitch)
    t1.start()
    t2 = threading.Thread(target=game_control)
    t2.start()


'''
#### CONTROLES DEL JUEGO ####
def game_control():
    global message
    while True:
        # if 'tag' in message.lower():
        #     pyautogui.keyDown('-')
        #     message = ''
        #     pyautogui.keyUp('-')

        #### MOVIMIENTO BASICO ####
        if 'up' in message.lower():
            pyautogui.keyDown('up')
            message = ''
            pyautogui.keyUp('up')

        elif 'down' in message.lower():
            pyautogui.keyDown('down')
            message = ''
            pyautogui.keyUp('down')

        elif 'left' in message.lower():
            pyautogui.keyDown('left')
            message = ''
            pyautogui.keyUp('left')

        elif 'right' in message.lower():
            pyautogui.keyDown('right')
            message = ''
            pyautogui.keyUp('right')

        elif 'flip' in message.lower():
            pyautogui.keyDown('u')
            message = ''
            pyautogui.keyUp('u')

        #### KOMBATE BASICO ####
        elif 'throw' in message.lower():
            pyautogui.keyDown('space')
            message = ''
            pyautogui.keyUp('space')

        elif 'block' in message.lower():
            apretar_tecla('o', 1)
            message = ''

        elif 'fp' in message.lower():
            pyautogui.keyDown('j')
            message = ''
            pyautogui.keyUp('j')

        elif 'bp' in message.lower():
            pyautogui.keyDown('i')
            message = ''
            pyautogui.keyUp('i')

        elif 'fk' in message.lower():
            pyautogui.keyDown('k')
            message = ''
            pyautogui.keyUp('k')

        elif 'bk' in message.lower():
            pyautogui.keyDown('l')
            message = ''
            pyautogui.keyUp('l')

        elif 'interact' in message.lower():
            pyautogui.keyDown('p')
            message = ''
            pyautogui.keyUp('p')

        #### MOVIMIENTO AVANZADO ####
        elif 'rj' in message.lower():
            pyautogui.hotkey('up', 'right')
            message = ''

        elif 'lj' in message.lower():
            pyautogui.hotkey('up', 'left')
            message = ''

        #### KOMBATE AVANZADO ####
        elif 'fatal' in message.lower():
            pyautogui.hotkey('o', 'u')
            message = ''

        else:
            pass


def apretar_tecla(tecla, tiempo=0.1):
    pyautogui.keyDown(tecla)

    def soltar_tecla(tecla):
        pyautogui.keyUp(tecla)

    if timers.get(tecla) is not None:
        timers[tecla].cancel()

    timers[tecla] = Timer(tiempo, soltar_tecla(tecla))


#### FUNCIONES PARA TWITCH ####
def twitch():
    def join_chat():    # Unirse al chat
        Loading = True
        while Loading:
            readbuffer_join = irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split('\n')[0:-1]:
                print(line)
                loading_complete(line)
                Loading = loading_complete(line)

    def loading_complete(line):     #
        if'End of /NAMES list' in line:
            print('Bot correctamente conectado al canal ' + CHANNEL)
            send_message(irc, 'Bot conectado al chat')
            return False
        else:
            return True

    def send_message(irc, message):
        message_temp = 'PRIVMSG #' + CHANNEL + ' :' + message
        irc.send((message_temp + '\n').encode())
        print(message_temp)

    def get_user(line):
        separate = line.split(':', 2)
        user = separate[1].split('!', 1)[0]
        # print(user)
        return user

    def get_message(line):
        global message
        try:
            message = (line.split(':', 2))[2]
            return message
            # print(message)
        except:
            message = ''

    def Console(line):
        if 'PRIVMSG' in line:
            return False
        else:
            return True

    join_chat()

    while True:
        try:
            readbuffer = irc.recv(1024).decode()
        except:
            readbuffer = ''
        for line in readbuffer.split('\n\n'):
            if line == '':
                continue
            elif 'PING' in line and Console(line):
                msgg = 'PONG tmi.twitch.tv\r\n'.encode()
                irc.send(msgg)
                print(msgg)
                continue
            else:
                print(line)
                user = get_user(line)
                message = get_message(line)
                print(user + ': ' + message)


if __name__ == "__main__":
    t1 = threading.Thread(target=twitch)
    t1.start()
    t2 = threading.Thread(target=game_control)
    t2.start()

'''
