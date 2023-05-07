import json
import socket
import time
import threading


from src.Field import *
from src.GUI import *

HOST = '127.0.0.1'
PORT = 1234

def send_request(request_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        request_json = json.dumps(request_data)

        s.sendall(request_json.encode())

        response_json = s.recv(1024).decode()

        return json.loads(response_json)

def main():
    # Example JSON request:
    json_request = {'type': 'json', 'data': {'key': 'value'}}
    json_response = send_request(json_request)
    print(f'JSON response: {json_response}')

    # Example ping request:
    ping_request = {'type': 'ping'}
    ping_response = send_request(ping_request)
    print(f'Ping response: {ping_response}')

    # Example "Hello, world!" request:
    hello_request = {'type': 'hello', 'data': {'name': 'world'}}
    hello_response = send_request(hello_request)
    print(f'Hello response: {hello_response}')

class Client:
    def __init__(self):
        print("Enter your name!")
        self.name = input()
        request = {'type': 'user_login', 'user': {'name' : self.name}}
        response = send_request(request)
        self.hash = response["hash"]
        begin = time.time()
        print("Succesfully connected to server, waiting matchamking system to start a game! 0/20 seconds")

        request = {'type': 'user_wait', 'user': {'name' : self.name, 'hash' : self.hash}}


        counter = 0

        while True:
            response = send_request(request)
            if response["status"] == "not_ready":
                print(f"Waiting matchmaking system {counter}/20")
                counter += 1
            else:
                break
            time.sleep(1)
        self.GUI = GUI()

        game = send_request({'type': 'update', 'user' : {"name" : self.name, 'hash': self.hash}})

        self.field = Field()

        self.GUI.draw(game["players"], self.field, [])

        Updating = threading.Thread(target=self.update)
        Button = threading.Thread(target=self.button)

        Updating.start()
        Button.start()

        Updating.join()
        Button.join()

    def button(self):
        while True:
            if(self.GUI.button_pressed):
                send_request({'type': 'press_button', 'user' : {"name" : self.name, 'hash': self.hash}})
                self.GUI.button_pressed = False
            time.sleep(0.1)

    def update(self):
        while True:
            response = send_request({'type': 'update', 'user' : {"name" : self.name, 'hash': self.hash}})

            self.GUI.draw(response["players"], self.field, [])

            time.sleep(0.1)


if __name__ == '__main__':
    Client()

