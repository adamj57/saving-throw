from math import floor


class Skill:
    def __init__(self, name, ability_data, prof, expert):
        self.name = name
        self.ability_data = ability_data
        self.prof = prof
        self.expert = expert

    def real_value(self):
        return self.ability_data.value + (2 if self.prof else 0) + (2 if self.expert else 0)

    def modifier(self):
        return floor((self.real_value() - 10) / 2)

    def base_ability(self):
        return self.ability_data.ability
