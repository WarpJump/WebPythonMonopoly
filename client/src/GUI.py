import tkinter

from .SiteTypes import *


class GUI:
    X_LEN_OF_FIELD = 1000
    Y_LEN_OF_FIELD = 1000

    X_LEN_OF_STATUS_MENU = 400
    Y_LEN_OF_STATUS_MENU = 200

    NUM_OF_CITES = 40
    SQUARE_SIZE = Y_LEN_OF_FIELD / 11

    def __init__(self):
        self.log_stack = []
        # self.d = (X - (NUM_OF_CITES/4+1) * self.SQUARE_SIZE) / (NUM_OF_CITES/4)
        self.window = tkinter.Tk()
        self.window.title("Monopoly")

        self.game_field = tkinter.Canvas(
            self.window,
            width=self.X_LEN_OF_FIELD,
            height=self.Y_LEN_OF_FIELD,
            background="#F9DFD9",
        )

        self.game_status = tkinter.Frame(self.window)

        self.button_and_userinfo = tkinter.Frame(self.game_status)

        self.userinfo = tkinter.Canvas(
            self.button_and_userinfo,
            width=self.X_LEN_OF_STATUS_MENU,
            height=self.Y_LEN_OF_STATUS_MENU,
        )

        self.button_pressed = False




        self.button = tkinter.Button(
            self.button_and_userinfo,
            width = 10,
            height = 11,
            text = "Make Move",
            command = self.press_button
        )

        self.logs = tkinter.Frame(self.game_status)
        self.listbox = tkinter.Listbox(
            self.logs, width=70, height=self.Y_LEN_OF_FIELD // 18
        )
        self.scrollbar = tkinter.Scrollbar(self.logs, command=self.listbox.yview)

        self.game_field.pack(side="left")

        self.game_status.pack(side="right")

        self.userinfo.pack(side="left")
        self.button.pack(side="right")

        self.button_and_userinfo.pack(side="top")

        self.logs.pack(side="bottom")
        self.listbox.pack(side="left", expand=False)
        self.scrollbar.pack(side="right")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.window.update()

    def press_button(self):
        self.button_pressed = True


    def draw(self, players, field, logs):
        print(players)
        # отрисовка истории игровых сообщений
        for message in logs:
            self.listbox.insert("end", message)

        # очистка поля с информацией о текущем игроке
        self.userinfo.create_rectangle(
            0,
            0,
            self.X_LEN_OF_STATUS_MENU,
            self.Y_LEN_OF_STATUS_MENU,
            fill="#F9DFD9",
        )

        # отрисовка информации об ходящем игроке

        #self.userinfo.create_text(
        #    10,
        #    10,
        #    text=f"{user.name}: {len(user.assets)} streets",
        #    anchor="nw",
        #    fill="black",
        #    width=400,
        #    font=("Arial", 15),
        #)
        #for i in range(len(user.assets)):
        #    self.userinfo.create_text(
        #        10 + 200 * (i // 8),
        #        40 + (i % 8) * 20,
        #        text=user.assets[i].name,
        #        anchor="nw",
        #        fill="black",
        #    )

        # очистка внутренней части поля
        self.game_field.create_rectangle(
            self.SQUARE_SIZE,
            self.SQUARE_SIZE,
            10 * self.SQUARE_SIZE,
            10 * self.SQUARE_SIZE,
            fill="#F9DFD9",
        )

        # отрисовка квадратиков по периметру
        for i in range(self.NUM_OF_CITES):
            (x, y) = self.get_coords(i)

            self.game_field.create_rectangle(
                x,
                y,
                x + self.SQUARE_SIZE,
                y + self.SQUARE_SIZE,
                outline="black",
                fill=field[i].color,
                width=2,
            )

            # отрисовка названий объектов
            self.game_field.create_text(
                x + 0.5 * self.SQUARE_SIZE,
                y + 0.2 * self.SQUARE_SIZE,
                text=field[i].name,
                fill="black",
                width=self.SQUARE_SIZE,
                font=("Arial", 8),
            )

            # отрисовка домиков
            if isinstance(field[i], Street):
                if field[i].houses:
                    self.game_field.create_text(
                        x + 5,
                        y + 0.7 * self.SQUARE_SIZE,
                        text="█ " * field[i].houses,
                        fill="black",
                        anchor="nw",
                        width=self.SQUARE_SIZE,
                        font=("Arial", 8),
                    )

        players_in_same_cite = [0] * 40
        counter = 0
        for player in players:
            name = player["name"]
            (x, y) = self.get_coords(player["position"])

            players_in_same_cite[player["position"]] += 1
            num = players_in_same_cite[player["position"]]

            # отрисовка имени игрока в клетке где он стоит
            self.game_field.create_text(
                x + 0.5 * self.SQUARE_SIZE,
                y + (0.125 * num + 0.3) * self.SQUARE_SIZE,
                text=name,
                fill="black",
                width=self.SQUARE_SIZE,
                font=("Arial", 8),
            )

            # отрисовка баланса игрока во внутренней области поля
            self.game_field.create_text(
                self.SQUARE_SIZE * 1.75,
                (1.2 + counter) * self.SQUARE_SIZE,
                text=f'{player["name"]} has {player["balance"]} money',
                fill="#666666",
                anchor="nw",
                width=self.SQUARE_SIZE * 1.5,
                font=("Arial", 12),
            )

            counter += 1
        self.window.update()

    def get_coords(self, position):
        if position < self.NUM_OF_CITES // 4:
            x = position * self.SQUARE_SIZE
            y = 0
        elif position < self.NUM_OF_CITES // 2:
            x = self.X_LEN_OF_FIELD - self.SQUARE_SIZE
            y = (position - self.NUM_OF_CITES // 4) * self.SQUARE_SIZE
        elif position < 3 * self.NUM_OF_CITES // 4:
            x = (
                self.X_LEN_OF_FIELD
                - (1 + position - self.NUM_OF_CITES // 2) * self.SQUARE_SIZE
            )
            y = self.Y_LEN_OF_FIELD - self.SQUARE_SIZE
        else:
            x = 0
            y = (
                self.Y_LEN_OF_FIELD
                - (1 + position - 3 * self.NUM_OF_CITES // 4) * self.SQUARE_SIZE
            )

        return (x, y)
