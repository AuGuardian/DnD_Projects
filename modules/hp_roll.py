import random

# class vor het bepalen van HP op basis van een sting in de vorm "**d**+**"

class Hp_roll():
    
    def __init__(self, roll):
        self.roll = roll

    def make_roll(self):
   
        f = self.roll.split('d')

        r = f[1].split('+')

        A = int(f[0])
        B = int(r[0])
        C = int(r[1])

        AV = int((((B+1)/2)*A)+C)
        result = 0

        for x in range (A):
            introll = random.randint(1,B)
            print(introll)
            result = result + introll
            print( result)
        
        result = result + C
        print (result)

        if result >= AV:
            print (result)
        
        else:
            print (AV)




t=Hp_roll("33d20+330")

t.make_roll()