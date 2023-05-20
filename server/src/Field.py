from .SiteTypes import *
import json


class Field:
    NUM_OF_CITES = 40
    field = [None] * NUM_OF_CITES

    def __init__(self):
        sites = open("src/field.json")
        field = json.load(sites)
        for i in range(self.NUM_OF_CITES):
            match field[i]["type"]:
                case "Street":
                    self.field[i] = Street(
                        field[i]["name"], field[i]["price"], field[i]["color"]
                    )
                case "OverTax":
                    self.field[i] = OverTax(field[i]["name"])
                case "Railway":
                    self.field[i] = Railway(
                        field[i]["name"], field[i]["price"], field[i]["color"]
                    )
                case "Supply":
                    self.field[i] = Supply(
                        field[i]["name"], field[i]["price"], field[i]["color"]
                    )
                case "Parking":
                    self.field[i] = Parking()
                case "Chance":
                    self.field[i] = Chance(
                        field[i]["min_chance"], field[i]["max_chance"]
                    )
                case "PublicTreasury":
                    self.field[i] = PublicTreasury()
                case "Jail":
                    self.field[i] = Jail()
                case "GoToJail":
                    self.field[i] = GoToJail()
                case "Spawn":
                    self.field[i] = Spawn()

        sites.close()

    def __getitem__(self, id):
        return Field.field[id]
