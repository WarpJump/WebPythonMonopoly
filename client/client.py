import json
import socket
import time


from src.Field import *
from src.GUI import *

HOST = ''
PORT = 12345




class Client:
    def __init__(self):
        print("Enter host adress:")
        global HOST
        HOST = input()
        print("Enter your name!")
        self.name = input()
        request = {'type': 'user_login', 'user': {'name' : self.name}}
        try:
            response = self.send_request(request)
        except:
            print("Couldn\'t connect to server, terminating")
            return None
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
        print(f'received response {game}')
        self.field = Field()

        self.GUI.draw(game["players"], self.field, [])

        self.update()


    def update(self):
        updated_time = time.time()
        while True:
            if(self.GUI.button_pressed):
                response = self.send_button()
                print(f'button pressed, {response}')
                self.GUI.button_pressed = False
            else:
                #если давно не синхронизировались с сервером, обновляемся
                if(time.time() - updated_time > 2):
                    response = self.send_update()
                    match response['status']:
                        case 'error':
                            print('sorry, internal server error, aborting')
                            return 1
                        case 'finished':
                            print('Game finished!')
                            return 0
                        case 'ready':
                            updated_time = time.time()
                            self.GUI.draw(response["players"], self.field, response["messages"])
                        case _:
                            print('unknown error, terminating')
                            return 1

            time.sleep(0.1)

    def send_button(self):
        return self.send_request({'type': 'press_button', 'user' : {"name" : self.name, 'hash': self.hash}})

    def send_update(self):
        return self.send_request({'type': 'update', 'user' : {"name" : self.name, 'hash': self.hash}})

    def send_request(self, request_data):
        self.socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        request_json = json.dumps(request_data)

        self.socket.sendall(request_json.encode())

        response_json = self.socket.recv(1024).decode()

        return json.loads(response_json)


Client()

