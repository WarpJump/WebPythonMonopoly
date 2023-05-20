class User:
    BASE_BALANCE = 400
    BASE_COORD = 0

    def __init__(self, Username):
        self.name = Username
        self.assets = []
        self.balance = self.BASE_BALANCE
        self.position = self.BASE_COORD

    def AddMoney(self, money):
        self.balance += money

    def CollectMoney(self, money):
        self.balance -= money

    def form_json(self):
        assets = [site.name for site in self.assets]
        return {"name" : self.name, "assets" : assets, "balance" : self.balance,
            "position" : self.position}

