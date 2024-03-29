# Used help from the tutorial video series: https://www.youtube.com/playlist?list=PLIw91yhFTTdJ2CDjOptoF-ddXbw7wmet-
# in basic features of the server and client side.

import datetime
import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 5050
SERVER_LIMIT = 8

active_users = []
sessions = []

# Listen messages for global chat
def listen_messages_all(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                msg_object = {
                    'sender': username + '[GLOBAL]',
                    'message': message,
                    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                print(msg_object)
                send_message_to_all(json.dumps(msg_object))
            else:
                print('Message cannot be empty. Please try again.')
        except:
            print('user disconnected.')
            break


# Listen messages for private chat
def listen_messages_private(client, username, receiver):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                msg_object = {
                    'sender': username + '[PRIVATE]',
                    'message': message,
                    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                print(msg_object)
                send_message_to_user(receiver, json.dumps(msg_object))
                send_message_to_user(client, json.dumps(msg_object))
            else:
                print('Message cannot be empty. Please try again.')
        except:
            print('user disconnected.')
            break


# Send message to a single user
def send_message_to_user(client, message):
    client.sendall(message.encode('utf-8'))


# Send message to all users
def send_message_to_all(message):
    for user in active_users:
        send_message_to_user(user[1], message)


# Handle client connection and user initialization
def handle_client(client):
    while True:
        response = client.recv(2048).decode('utf-8')
        if response != '':
            response = response.split(';')

            username = response[0]
            selection = response[1]
            active_users.append((username, client))
            if selection == '1':
                private_chat(client, username)
                break
            elif selection == '2':
                new_user_message = {
                    'sender': 'SERVER',
                    'message': f'{username} has joined to the global chat.',
                    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                send_message_to_all(json.dumps(new_user_message))
                threading.Thread(target=listen_messages_all, args=(client, username)).start()
                break
        else:
            print('Username cannot be empty. Please try again.')


# Create private chat session
def private_chat(client, username):
    while True:
        receiver = client.recv(2048).decode('utf-8')
        for user in active_users:
            if (user[0] == receiver):
                client_2 = user[1] 
                sessions.append(((username, client), (receiver, client_2)))
                server_msg = {
                    'sender': 'SERVER',
                    'message': f'Private chat with {receiver} created.',
                    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                client.sendall(json.dumps(server_msg).encode('utf-8'))
                break
        break
    threading.Thread(target=listen_messages_private, args=(client, username, client_2)).start()


# Disconnect user from the server
def disconnect_user(client):
    client.close()
    active_users.remove(client)


def main():
    # Create a server socket. SOCK_STREAM means that it is a TCP socket.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind((HOST, PORT))
        print(f'Server is running on {HOST}:{PORT}')
    except socket.error as e:
        print('Error occured while trying to connect: ' + str(e))
    
    server.listen(SERVER_LIMIT)

    while True:
        client, address = server.accept()
        print(f'Connected to client: {address[0]}:{address[1]}')

        threading.Thread(target=handle_client, args=(client, )).start()


if __name__ == '__main__':
    main()