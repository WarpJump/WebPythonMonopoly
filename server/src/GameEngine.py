from src.Field import *

from src.User import *

import time

class num_of_purchased_property:
    size = 0


class GameEngine:
    BASE_VERDICT_PLACEHOUSE_PRICE = 300

    npc_namelist = [
            "Ivan Kalinin",
            "Yura Konstantinov",
            "Alexander Gerasimov",
            "Alexander Gunin",
            "Stepa Karpov",
            "Maxim Ivanov",
            "Egor Zuev",
            "Arslan Khalilov",
            "Ksenia Karpluk",
            "Shestakov Vladimir",
            "Syrov Artyom",
            "Anton Kopanov",
            "Tanya Pechnikova",
            "Darya Solodova",
        ]

    def __init__(self, users, hashes):
        self.users = [User(username) for username in users]
        self.button_pressed = [False] * len(users)
        self.hashes = hashes
        self.npcs =  [User(self.npc_namelist[i]) for i in range(8 - len(users))]
        self.user_pressed_button = [False for i in range(8)]

        self.field = Field()
        self.log_stack = []
        self.agression = 10
        self.num_of_purchased_property = num_of_purchased_property()



    def move_player(self, player):
        steps = random.randint(1, 6) + random.randint(1, 6)
        self.log_stack.append(f"Player {player.name} goes {steps} steps forward!")
        player.position += steps
        if player.position > 40:
            player.position -= 40
            self.log_stack.append(
                f"Player {player.name} has reached 2ka and got 200 money!"
            )
            player.AddMoney(200)
        player.position %= 40

    async def play(self):
        for id in range(self.players):
            while(not self.button_pressed[id]):
                continue
            self.button_pressed[id] = False

            player = self.players[id]
            messages = []

            self.move_player(player)
            message = self.field[player.position].UserInteraction(
                player, self.num_of_purchased_property
            )
            messages.append(message)

            if player.balance < 0:
                messages.append(
                    f"Player {player.name} has lost all money and went bankrupt!"
                )
                self.num_of_purchased_property.size -= len(player.assets)
                if player == self.user:
                    messages.append(
                        f"You went bankrupt, no delays anymore, finding winner as soon as possible"
                    )
                    print(
                        "You went bankrupt, no delays anymore, finding winner as soon as possible"
                    )
                    self.user_alive = False
                for site in player.assets:
                    site.Destruct()
                self.players.pop(id)

            # ищем кандидата куда можно поставить домик
            boundary_house_place_price = (
                self.BASE_VERDICT_PLACEHOUSE_PRICE
                + self.num_of_purchased_property.size * (10 - self.agression)
            )
            if player.balance > boundary_house_place_price and len(player.assets):
                min_num_of_houses = 1000000
                candidate_for_house = 123
                for site in player.assets:
                    if isinstance(site, Street):
                        if site.houses < min_num_of_houses:
                            candidate_for_house = site
                            min_num_of_houses = site.houses

                candidate_for_house.PlaceHouse()


        for player in self.npcs:
            messages = []

            self.move_player(player)
            message = self.field[player.position].UserInteraction(
                player, self.num_of_purchased_property
            )
            messages.append(message)

            if player.balance < 0:
                messages.append(
                    f"Player {player.name} has lost all money and went bankrupt!"
                )
                self.num_of_purchased_property.size -= len(player.assets)
                if player == self.user:
                    messages.append(
                        f"You went bankrupt, no delays anymore, finding winner as soon as possible"
                    )
                    print(
                        "You went bankrupt, no delays anymore, finding winner as soon as possible"
                    )
                    self.user_alive = False
                for site in player.assets:
                    site.Destruct()
                self.players.remove(player)

            # ищем кандидата куда можно поставить домик
            boundary_house_place_price = (
                self.BASE_VERDICT_PLACEHOUSE_PRICE
                + self.num_of_purchased_property.size * (10 - self.agression)
            )
            if player.balance > boundary_house_place_price and len(player.assets):
                min_num_of_houses = 1000000
                candidate_for_house = 123
                for site in player.assets:
                    if isinstance(site, Street):
                        if site.houses < min_num_of_houses:
                            candidate_for_house = site
                            min_num_of_houses = site.houses

                candidate_for_house.PlaceHouse()

            #self.GUI.draw(self.players, self.field, messages, player)

        if len(self.players) == 1:
            messages = []

            messages.append(
                f"Player {self.players[0].name} remains the last player and wins the game!"
            )

            messages.append("Close the window to exit")
            print("Press and enter any key to exit")
            a = input()
            return a



        time.sleep(0.1)

    def update(self, hash):
        if hash in self.hashes:
            users = [user.form_json() for user in self.users]
            return users
        else:
            return []
