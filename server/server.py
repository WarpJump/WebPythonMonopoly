import json
import socket
import threading
import time
import random



from src.GameEngine import *

HOST = '0.0.0.0'
PORT = 12345


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


        #цикл, принимающий запросы
        Receiver = threading.Thread(target=self.receive)

        #цикл, распределяющий игроков по партиям
        Matchmaking = threading.Thread(target=self.matchmaking)

        #цикл, просчитывающий всю логику всех партий
        GameComputing = threading.Thread(target=self.computing)

        Receiver.start()
        Matchmaking.start()
        GameComputing.start()

        Receiver.join()
        Matchmaking.join()
        GameComputing.join()

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
                    print(f"users hashes {hashes}")
                    self.iterator += num
                    self.launched_games.append(GameEngine(users, hashes))

                    #если игрок один и ждёт немного, пусть ещё подождёт, вдруг люди зайдут
                time.sleep(0.01)

    def computing(self):
        while True:
            for game in self.launched_games:
                game.play()

    def receive(self):
        self.connection  = None
        while True:
            try:
                self.connection, self.address = self.gateway.accept()
                request_payload = json.loads(self.connection.recv(1024).decode())

                response_payload = self.handle_request(request_payload)
                print(f'succesfully finished {request_payload["type"]} request')

                sent_payload = json.dumps(response_payload)

                self.connection.sendall(sent_payload.encode())

            except:
                if self.connection:
                    sent_payload = json.dumps({"status" : "error"})
                    self.connection.sendall(sent_payload.encode())
                else:
                    print("Error")


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
            game = self.launched_games[id]
            if len(game.users + game.npcs) == 1:
                self.launched_games.pop(id)
                return {"status" : "finished"}
            else:
                return {"status" : "ready", "players" : self.launched_games[id].update(payload["user"]["hash"]), "messages" : []}



    def handle_press_button(self, payload):
        #по хешу игрока ищем в массиве в какой партии он участвует
        user_hash = payload["user"]["hash"]
        party_id = self.hashes.index(user_hash)

        #сохраняем ссылку на нужную партию
        curr_users_game = self.launched_games[party_id]

        #зная в какой партии участвует игрок, получаем его номер внутри игры
        internal_user_number = curr_users_game.hashes.index(user_hash)

        #записываем нажатие на кнопку
        curr_users_game.button_pressed[internal_user_number] = True
        print(f'button press received on game {curr_users_game} on user {internal_user_number}')
        print(curr_users_game.button_pressed)

Server()
