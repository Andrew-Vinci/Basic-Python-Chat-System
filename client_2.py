
"""This Code Acts as a Client for a Chat System.

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

name = ""

# host/port information
HOST = "localhost"
SERVER_PORT = 7000
SERVER_PORT_2 = 7001

def send_message():
    """Sends the Message From the User"""

    while True:

        # print the name and incoming message on same line
        print(name + ":", end = "")
        message = input()

        # assign name and message to list
        message_list = [name, message]

        # serialize, encode, and send the json data
        json_data = json.dumps(message_list)
        json_message = json_data.encode("utf-8")
        message_length = len(json_message).to_bytes(4, "big")
        send_socket.sendall(message_length + json_message)

        # if beginning word is E, exit loop
        if message[0] == "E":
            break


def receive_message():
    """Receives the MEssage from Other Users"""

    while True:

        # receive, decode, deserialize, and print data
        message_length = receive_socket.recv(4)
        message_length = int.from_bytes(message_length, "big")
        recv_data = receive_socket.recv(message_length)

        # if there is no data, break loop
        if not recv_data:
            break

        # decode json data
        recv_json = recv_data.decode("utf-8")

        # load json data
        recv_message = json.loads(recv_json)

        # print the name and message received
        print(recv_message[0] + ":" + " " + recv_message[1])


if __name__ == '__main__':
    """Main Function Gets Username and Starts Threads"""

    # set up two sockets
    send_socket = socket.socket()
    send_socket.connect((HOST, SERVER_PORT))
    receive_socket = socket.socket()
    receive_socket.connect((HOST, SERVER_PORT_2))

    # get user name
    name = input("Please Enter Your Name: ")

    # check for spaces in name
    while " " in name:
        print("Spaces Not Allowed. Please Print Name.")
        name = input("Please Enter Your Name: ")

    # Instructions for User
    print("Type 'B' in Front of Message to Broadcast.")
    print("Type 'P' in Front of Recipient and Message "
          "to Send Private Message.")
    print("Type 'E' in front of Username to Exit.")

    # serialize, encode, and send the json data
    json_data = json.dumps(name)
    json_message = json_data.encode("utf-8")
    receive_socket.sendall(json_message)

    # create two threads
    thread = threading.Thread(target=send_message)
    thread_2 = threading.Thread(target=receive_message)

    # start threads
    thread.start()
    thread_2.start()

    # join threads
    thread.join()
    thread_2.join()
