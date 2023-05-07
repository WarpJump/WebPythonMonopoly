import random


class Place:
    def __init__():
        raise NotImplemented


class SystemPlaces(Place):
    color = "grey"


class Spawn(SystemPlaces):
    def __init__(self):
        self.name = "2ka"

    def UserInteraction(self, User, num_of_purchased_property):
        User.AddMoney(200)

        return f"User {User.name} is staying in 2ka and gets scholarship 200 money!"


class Jail(SystemPlaces):
    def __init__(self):
        self.name = "Foreign Lang Dep."

    def UserInteraction(self, User, num_of_purchased_property):
        return f"User {User.name} is on excursion in Foreign Lang. Department. Nothing happens."


class Parking(SystemPlaces):
    def __init__(self):
        self.name = "KSP"

    def UserInteraction(self, User, num_of_purchased_property):
        return f"User {User.name} is in KSP. Nothing happens."


class GoToJail(SystemPlaces):
    def __init__(self):
        self.name = "B2 english Language testing"

    def UserInteraction(self, User, num_of_purchased_property):
        return f"User {User.name} is forced to learn chinese."


class PublicTreasury(SystemPlaces):
    MIN_TREASURE = 100
    MAX_TREASURE = 200

    def __init__(self):
        self.name = "Public Treasury"

    def UserInteraction(self, User, num_of_purchased_property):
        treasure = random.randint(self.MIN_TREASURE, self.MAX_TREASURE)
        User.AddMoney(treasure)

        return f"User {User.name} won {treasure} money!"


class Chance(SystemPlaces):
    def __init__(self, min_chance, max_chance):
        self.name = "Chance"
        self.min_chance = min_chance
        self.max_chance = max_chance

    def UserInteraction(self, User, num_of_purchased_property):
        chance = random.randint(self.min_chance, self.max_chance)
        if chance < 0:
            User.CollectMoney(-chance)
            return f"User {User.name} lost {-chance} money!"

        else:
            User.AddMoney(chance)
            return f"User {User.name} won {chance} money!"


class OverTax(SystemPlaces):
    OVERTAX_VALUE = 200

    def __init__(self, name):
        self.name = name

    def UserInteraction(self, User, num_of_purchased_property):
        User.CollectMoney(self.OVERTAX_VALUE)

        return f"User {User.name} paid 200 money!"


class Asset(Place):
    owner = ""


class Street(Asset):
    HOUSE_PRICE = 200

    def __init__(self, name, price, color):
        self.name = name
        self.price = price
        self.rent = self.price / 2
        self.color = color
        self.houses = 0

    def UserInteraction(self, User, num_of_purchased_property):
        if self.owner == "":
            if User.balance > self.price:
                self.owner = User
                User.assets.append(self)
                User.CollectMoney(self.price)
                num_of_purchased_property.size += 1
                return f"User {User.name} can buy {self.name} and do so!"

            else:
                return f"User {User.name} cannot buy {self.name}! Nothing happens"

        elif self.owner == User:
            return f"User {User.name} is on his own street. Nothing happens."

        else:
            money = int(self.price / 2)
            if money > User.balance:
                money = User.balance
                User.CollectMoney(1)

            User.CollectMoney(money)
            self.owner.AddMoney(money)
            return f"User {User.name} pays {money} to {self.owner.name} for rent!"

    def PlaceHouse(self):
        self.rent += self.price / 2
        self.houses += 1
        self.owner.CollectMoney(self.HOUSE_PRICE)
        return f"User {self.owner.name} place a one more house on {self.name}"

    def Destruct(self):
        self.rent = self.price / 2
        self.houses = 0
        self.owner = ""


class Railway(Asset):
    def __init__(self, name, price, color):
        self.name = name
        self.price = price
        self.color = color

    def UserInteraction(self, User, num_of_purchased_property):
        return f"User {User.name} is on some railway"


class Supply(Asset):
    def __init__(self, name, price, color):
        self.name = name
        self.price = price
        self.color = color

    def UserInteraction(self, User, num_of_purchased_property):
        return f"User{User.name} is on some supply"
