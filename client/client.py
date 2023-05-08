import json
import socket
import time
import threading


from src.Field import *
from src.GUI import *

HOST = ''
PORT = 1234




class Client:
    def __init__(self):
        print("Enter host adress:")
        global HOST
        HOST = input()
        print("Enter your name!")
        self.name = input()
        request = {'type': 'user_login', 'user': {'name' : self.name}}
        response = self.send_request(request)
        self.hash = response["hash"]
        begin = time.time()
        print("Succesfully connected to server, waiting matchamking system to start a game! 0/20 seconds")

        request = {'type': 'user_wait', 'user': {'name' : self.name, 'hash' : self.hash}}


        counter = 0

        while True:
            response = self.send_request(request)
            if response["status"] == "not_ready":
                print(f"Waiting matchmaking system {counter}/20")
                counter += 1
            else:
                break
            time.sleep(1)
        self.GUI = GUI()

        game = self.send_request({'type': 'update', 'user' : {"name" : self.name, 'hash': self.hash}})

        self.field = Field()

        self.GUI.draw(game["players"], self.field, [])

        Updating = threading.Thread(target=self.update)
        Button = threading.Thread(target=self.button)

        Updating.start()
        Button.start()

        Updating.join()
        Button.join()

    def send_request(request_data):
        socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM):
        socket.connect((HOST, PORT))
        request_json = json.dumps(request_data)

        socket.sendall(request_json.encode())

        response_json = socket.recv(1024).decode()

        return json.loads(response_json)

    def button(self):
        while True:
            if(self.GUI.button_pressed):
                self.send_request({'type': 'press_button', 'user' : {"name" : self.name, 'hash': self.hash}})
                self.GUI.button_pressed = False
            time.sleep(0.1)

    def update(self):
        while True:
            response = self.send_request({'type': 'update', 'user' : {"name" : self.name, 'hash': self.hash}})

            self.GUI.draw(response["players"], self.field, [])

            time.sleep(0.1)


Client()

