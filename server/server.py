import json
import socket
import threading
import time
import random



from src.GameEngine import *

HOST = "0.0.0.0"
PORT = 1234


class Server:
    def __init__(self):
        self.gateway = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gateway.bind((HOST, PORT))
        self.gateway.listen()
        print(f"gateway ready on {HOST}, {PORT}!")
        self.user_queue = []
        self.user_time = []
        self.hashes = []
        self.hash_user_dict = []
        self.iterator = 0

        self.launched_games = []

        Receiver = threading.Thread(target=self.receive)
        Matchmaking = threading.Thread(target=self.matchmaking)

        Receiver.start()
        Matchmaking.start()

        Receiver.join()
        Matchmaking.join()

    def matchmaking(self):
        while True:
            if len(self.user_queue) > self.iterator:
                num_of_users = len(self.user_queue)
                curr_time = time.time()
                users = []
                hashes = []
                num = 0
                #если игроков в очереди оказалось четыре, запускаем их в одну партию при любых обстоятельствах
                if num_of_users - self.iterator >= 4:
                    num = 4

                #если игроков хотя бы два и они ждут 15 секунд, не будем больше ждать
                elif (
                    curr_time - self.user_time[self.iterator] >= 15
                    and num_of_users - self.iterator >= 2
                ):
                    num = num_of_users - self.iterator
                #если игрок один и ждёт очень долго, то пусть играет один
                elif curr_time - self.user_time[self.iterator] >= 2:
                    num = 1

                if num:
                    for i in range(num):
                        users.append(self.user_queue[i + self.iterator])
                        hashes.append(self.hashes[i + self.iterator])
                        self.hash_user_dict.append({self.hashes[i + self.iterator], len(self.launched_games)})
                    print(f"{num} users found! Creating match")
                    self.iterator += num
                    self.launched_games.append(GameEngine(users, hashes))

                #если игрок один и ждёт немного, пусть ещё подождёт, вдруг люди зайдут
            time.sleep(0.1)

    def receive(self):
        while True:
            self.connection, self.address = self.gateway.accept()
            request_payload = json.loads(self.connection.recv(1024).decode())

            response_payload = self.handle_request(request_payload)
            print(response_payload)

            sent_payload = json.dumps(response_payload)

            self.connection.sendall(sent_payload.encode())

    def handle_request(self, payload):
        request_type = payload["type"]
        match request_type:
            case "user_login":
                return self.handle_login_signup(payload)
            case "user_wait":
                return self.handle_ping_request(payload)
            case "update":
                return self.handle_ping_request(payload)
            case "press_button":
                return self.handle_press_button(payload)
            case "exit":
                return self.handle_exit(payload)
            case _:
                return {"error": f'Unknown request type "{request_type}".'}

    def handle_login_signup(self, payload):
        # генерируем уникальный хеш для игрока чтобы в дальнейшем только он мог играть от своего имени
        hash = random.randint(1, 1000000000000)
        while self.hashes.count(hash):
            hash = random.randint(1, 1000000000000)

        self.user_queue.append(payload["user"]["name"])
        self.user_time.append(time.time())
        self.hashes.append(hash)
        print(self.user_queue, self.hashes)
        return {"hash": hash}

    def handle_ping_request(self, payload):
        print(self.user_queue, self.iterator, self.user_queue.index(payload["user"]["name"]))
        if self.user_queue.index(payload["user"]["name"]) >= self.iterator:
            return {"status" : "not_ready"}
        else:
            id = self.hashes.index(payload["user"]["hash"])
            print(id)
            return {"status" : "ready", "players" : self.launched_games[id].update(payload["user"]["hash"])}



    def handle_press_button(self, payload):
            id = self.hashes.index(payload["user"]["hash"])
            name = payload["user"]["name"]
            self.launched_games[id].button_pressed[self.launched_games[id].users.index(name)] = True


Server()
