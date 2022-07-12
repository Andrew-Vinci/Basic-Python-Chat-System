
"""This Code Acts as a Server for a Chat System.

Author: Andrew Vinci
Class: CSI-275-01
Assignment: Final Project -- Chat System.

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""


import threading, socket, random, json
from threading import Thread

global_message = []

HOST = "localhost"
SERVER_PORT = 7000
SERVER_PORT_2 = 7001

send_socket = socket.socket()
receive_socket = socket.socket()

def receive_message(socket):
    """Receives Message from Socket"""

    while True:

            # get the message length
            message_length = socket.recv(4)
            message_length = int.from_bytes(message_length, "big")
            message = socket.recv(message_length).decode("utf-8")

            # if message is blank, break loop
            if not message:
                break

            # load json message
            message_2 = json.loads(message)

            # get the message
            get_message = message_2[1]

            # split message up to check which chat to use
            # B for Broadcast, P for Private, E for Exit
            check_message = get_message.split()[0]

            # check if message is private
            if check_message == "P":

                # get the name of the person to send the message to
                get_name = get_message.split()
                get_name = get_name[1]
                get_name = get_name.strip()
                #print(get_name)

                # loop through the global message
                for i in global_message:

                    # get the name associated with the socket
                    check_name = i[1]
                    check_name = check_name[:-1]
                    check_name = check_name [1:]

                    # compare name from socket above to name from message
                    if check_name == get_name:

                        # get the socket assigned to name
                        snd_socket = i[0]

                        # encode message, get message length
                        json_dump = json.dumps(message_2).encode("utf-8")
                        json_length = len(json_dump).to_bytes(4, "big")

                        # send message with length in front
                        snd_socket.sendall(json_length + json_dump)

            # check if message is a broadcast
            if check_message == "B":

                # loop through global variable
                for i in global_message:

                    # get the socket from each tuple in global variable
                    snd_socket = i[0]

                    # encode message, get length of message
                    json_dump = json.dumps(message_2).encode("utf-8")
                    json_length = len(json_dump).to_bytes(4, "big")

                    # send message with length in front
                    snd_socket.sendall(json_length + json_dump)

            # check if message is Exit
            if check_message == "E":

                # get the name of user
                get_name = get_message.split()
                get_name = get_name[1]
                get_name = get_name.strip()

                # loop through global message
                for i in global_message:

                    # get the name of user
                    check_name = i[1]

                    # get the socket of user
                    close_socket = i[0]

                    # remove quotations from name
                    check_name = check_name[:-1]
                    check_name = check_name[1:]

                    # if the name matches the user in message
                    if check_name == get_name:

                        # remove user from the list
                        global_message.pop()

                        # close users socket
                        close_socket.close()


def writing_thread(socket):
    """Recives Message From Socket and Adds to Global Variable"""

    while True:

        # accept socket
        accept_sock, address = socket.accept()

        # get name and decode
        name = accept_sock.recv(4096).decode()

        # add socket and name to global message
        global_message.append((accept_sock, name))


def reading_thread(socket):
    """Recieves Messages from Socket and Starts New Threads"""

    while True:

        # accept socket
        accept_sock, address = socket.accept()

        # create new thread
        thread = Thread(target=receive_message, args=(accept_sock,))

        # start the thread
        thread.start()

if __name__ == '__main__':
    """Main Function Begins """

    # create two sockets
    send_socket = socket.socket()
    send_socket.bind((HOST, SERVER_PORT))
    send_socket.listen(20)

    # bind and listen using two sockets created
    receive_socket = socket.socket()
    receive_socket.bind((HOST, SERVER_PORT_2))
    receive_socket.listen(20)

    # create two threads
    thread = threading.Thread(target=writing_thread, args=(receive_socket,))
    thread_2 = threading.Thread(target=reading_thread, args=(send_socket,))

    # start threads
    thread.start()
    thread_2.start()

    # join threads
    thread.join()
    thread_2.join()