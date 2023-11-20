import random

class DiceRoll:

    def __init__(self, identifier, multiplier, modifier):
        self.identifier = identifier
        self.multiplier = multiplier
        self.modifier = modifier

    def dice_roll(self):

        for x in range(self.multiplier):

            roll = random.randint(self.identifier)
            print("rol nummer", x , "=",roll)
            result = result + roll

        result = result + self.modifier

        return result
