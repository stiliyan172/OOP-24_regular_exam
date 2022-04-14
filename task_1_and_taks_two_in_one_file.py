from abc import ABC, abstractmethod


class Supply(ABC):
    def __init__(self, name, energy):
        self.name = name
        self.energy = energy

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value == '':
            raise ValueError("Name cannot be an empty string.")
        self.__name = value

    @property
    def energy(self):
        return self.__energy

    @energy.setter
    def energy(self, value):
        if value < 0:
            raise ValueError("Energy cannot be less than zero.")
        self.__energy = value

    @abstractmethod
    def details(self):
        pass


class Food(Supply):
    type = "Food"
    # ENERGY = 25  # A food has 25 units of energy as an optional parameter.

    def __init__(self, name, energy=25):
        super().__init__(name, energy)

    def details(self):
        return f"{self.__class__.type}: {self.name}, {self.energy}"


class Drink(Supply):
    type = "Drink"
    INITIAL_ENERGY = 15

    def __init__(self, name):
        super().__init__(name, self.INITIAL_ENERGY)

    def details(self):
        return f"{self.__class__.type}: {self.name}, {self.energy}"


class Player:
    _names = set()

    def __init__(self, name, age, stamina=100):
        self.name = name
        self.age = age
        self.stamina = stamina  # Stamina's max value is 100, and its min value is 0
        if self.name in Player._names:
            raise Exception(f"Name {self.name} is already used!")
        else:
            Player._names.add(self.name)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if value == '':
            raise ValueError("Name not valid!")
        self.__name = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if value < 12:
            raise ValueError("The player cannot be under 12 years old!")
        self.__age = value

    @property
    def stamina(self):
        return self.__stamina

    @stamina.setter
    def stamina(self, value):
        if value < 0 or value > 100:
            raise ValueError("Stamina not valid!")
        self.__stamina = value

    @property
    def need_sustenance(self):
        if self.stamina < 100:
            return True
        else:
            return False

    def __str__(self):
        return f"Player: {self.name}, {self.age}, {self.stamina}, {self.need_sustenance}"


class Controller:
    def __init__(self):
        self.players = []  # An empty list that will contain all the players (objects)
        self.supplies = []  # An empty list that will contain all the supplies (objects)

    def add_player(self, *players_objects):
        added_players_list = []
        for pl in players_objects:
            if pl not in self.players:
                self.players.append(pl)
                added_players_list.append(pl)
        return f"Successfully added: {', '.join(str(x.name) for x in added_players_list)}"

    def add_supply(self, *supplies_objects):
        for x in supplies_objects:
            self.supplies.append(x)

    def sustain(self, player_name: str, sustenance_type: str):
        is_food_supply = any(x for x in self.supplies if x.type == "Food")
        is_drink_supply = any(x for x in self.supplies if x.type == "Drink")

        if not is_food_supply and sustenance_type == "Food":
            return "There are no food supplies left!"
        elif not is_drink_supply and sustenance_type == "Drink":
            return "There are no drink supplies left!"
        elif (is_food_supply and sustenance_type == "Food") or (is_drink_supply and sustenance_type == "Drink"):
            last_supply = [x for x in self.supplies if x.type == sustenance_type][-1]
            current_player = [x for x in self.players if x.name == player_name][0]
            if current_player.stamina >= 100:
                return f"{player_name} have enough stamina."
            else:
                try:
                    current_player.stamina += last_supply.energy
                except ValueError:
                    # if current_player.stamina > 100:
                    current_player.stamina = 100

                self.supplies.remove(last_supply)
                return f"{player_name} sustained successfully with {last_supply.name}."

    def duel(self, first_player_name: str, second_player_name: str):
        first_player = [x for x in self.players if x.name == first_player_name][0]
        second_player = [x for x in self.players if x.name == second_player_name][0]

        if first_player.stamina > 0 and second_player.stamina > 0:
            if first_player.stamina < second_player.stamina:
                first_stamina_to_be_reduced = first_player.stamina / 2
                second_player.stamina -= first_stamina_to_be_reduced
                if second_player.stamina < 0:
                    second_player.stamina = 0
                    return f"Winner: {first_player_name}"
                second_stamina_to_be_reduced = second_player.stamina / 2
                first_player.stamina -= second_stamina_to_be_reduced
                return f"Winner: {first_player_name}"

            elif second_player.stamina < first_player.stamina:
                second_stamina_to_be_reduced = second_player.stamina / 2
                first_player.stamina -= second_stamina_to_be_reduced
                if first_player.stamina < 0:
                    first_player.stamina = 0
                    return f"Winner: {second_player_name}"
                first_stamina_to_be_reduced = first_player.stamina / 2
                second_player.stamina -= first_stamina_to_be_reduced
                return f"Winner: {second_player_name}"
        else:
            if first_player.stamina == 0 and second_player.stamina == 0:
                return f"Player {first_player_name} does not have enough stamina.\nPlayer {second_player_name} does not have enough stamina."
            elif first_player.stamina == 0 and second_player.stamina != 0:
                return f"Player {first_player_name} does not have enough stamina."
            elif second_player.stamina == 0 and first_player.stamina != 0:
                return f"Player {second_player_name} does not have enough stamina."

    def next_day(self):
        for plr in self.players:
            try:
                plr.stamina -= int(plr.age * 2)
            except:
                if plr.stamina < 0:
                    plr.stamina = 0

        for p in self.players:
            self.sustain(p.name, "Food")
            self.sustain(p.name, "Drink")

    def __str__(self):
        players_str = ''
        supplies_str = ''
        for x in self.players:
            players_str += f"{str(x)}\n"

        for y in self.supplies:
            supplies_str += f"{y.details()}\n"

        return players_str + supplies_str


controller = Controller()
apple = Food("apple", 22)
cheese = Food("cheese")
juice = Drink("orange juice")
water = Drink("water")
first_player = Player('Peter', 15)
second_player = Player('Lilly', 12, 94)
print(controller.add_supply(cheese, apple, cheese, apple, juice, water, water))
print(controller.add_player(first_player, second_player))
print(controller.duel("Peter", "Lilly"))
print(controller.add_player(first_player))
print(controller.sustain("Lilly", "Drink"))
first_player.stamina = 0
print(controller.duel("Peter", "Lilly"))
print(first_player)
print(second_player)
controller.next_day()
print(controller)