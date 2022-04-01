import random
import socket
from datetime import datetime
from threading import Thread

from colorama import Fore, init

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
          ]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002  # server's port
separator_token = "<SEP>"  # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# prompt the client for a name
name = input("Welcome! Here you can chat with another client. When you are done, type 'close'. Choose a user name: ")


def listen_for_messages():
    while True:
        msg = s.recv(1024).decode()
        print("\n" + msg)


# make a thread that listens for messages to this client & print them
thread = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
thread.daemon = True
# start the thread
thread.start()

while True:
    # input message we want to send to the server
    message = input()

    # a way to exit the program
    if message.lower() == 'close':
        break

    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
    message = f"{client_color}[{date_now}] {name}{separator_token}{message}{Fore.RESET}"

    # finally, send the message
    s.send(message.encode())

# close the socket
s.close()
