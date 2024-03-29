# Used help from the tutorial video series: https://www.youtube.com/playlist?list=PLIw91yhFTTdJ2CDjOptoF-ddXbw7wmet-
# in basic features of the server and client side.

import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 5050


# Listen server for incoming messages
def listen_server(client):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            message = json.loads(message)
            print(f"{message['sender']}: {message['message']} ({message['timestamp']})")
        else:
            print('Received empty message.')


# Send message to server
def send_message(client):
    while True:
        message = input()
        if message != '':
            client.sendall(message.encode('utf-8'))
        else:
            print('Message cannot be empty. Please try again.')


# Send information to intialize user and chat
def send_to_server(client):
    username = input('Enter your username: ')
    if username != '':
        action = input('Enter 1 to chat with a user, 2 to chat with a channel: ')
        if action == '1':
            username = username + ';' + action
            client.sendall(username.encode('utf-8'))
            select_user_to_chat(client)
        elif action == '2':
            username = username + ';' + action
            client.sendall(username.encode('utf-8'))
        else:
            print('Invalid action. Please try again.')
            exit(0)
    else:
        print('Username cannot be empty. Please try again.')
        exit(0)
    
    threading.Thread(target=listen_server, args=(client, )).start()
    send_message(client)


# Select user to chat with in private chat session
def select_user_to_chat(client):
    receiver = input('Enter the username you want to chat with: ')
    if receiver != '':
        client.sendall(receiver.encode('utf-8'))
    else:
        print('Receiver cannot be empty. Please try again.')
        exit(0)


def main():
    # Client side socket creation for TCP connection.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f'Connected to {HOST}:{PORT}')
    except socket.error as e:
        print('Error occured while trying to connect: ' + str(e))

    send_to_server(client)


if __name__ == '__main__':
    main()