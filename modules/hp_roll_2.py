import random

# function to determine HP from a string in the form of **d**+** (eg: 5d10+50). This function will be called with a roll variable (the string) and a roll limit variable to determine wheter it is a full radom roll, a limited roll or just the max HP

def make_roll(roll, limit_type=("fullrandom"), limit=("min")):
           # Splitting the string to determine the identifier (type of dice), the multiplier (number of dice) and modifier (added value) 

        first_split = roll.split('d')
        second_split = first_split[1].split('+')

        multiplier = int(first_split[0])
        identifier = int(second_split[0])
        modifier = int(second_split[1])

        average = int((((identifier+1)/2)*multiplier)+modifier)
        maximum = int((identifier*multiplier)+modifier)
        minimum = int((1*multiplier)+modifier)
        
        random_roll = 0

        for x in range(multiplier):
                introll = random.randint(1,identifier)
                random_roll = random_roll + introll
        random_roll = random_roll + modifier

        if (limit_type != "fullrandom") and (limit_type != "upper") and (limit_type != "lower") and (limit_type != "between") and (limit_type != "max") and (limit_type != "min"):
                
                raise TypeError("expected value for limit_type = fullrandom, upper, lower, between, max or min")
        else:
                if limit_type == "fullrandom":
                        return(random_roll)
                
                elif limit_type == "upper":
                        if (isinstance(limit,int)):
                                if random_roll <= limit:
                                        return (random_roll)
                                else:
                                        return (limit)

                        elif limit == "average":
                                 if random_roll <= average:
                                        return (random_roll)
                                else:
                                        return (average)
                
                elif limit_type == "lower":
                        if (isinstance(limit,int)):
                                if random_roll >= limit:
                                        return (random_roll)
                                else:
                                        return (limit)

                        elif limit == "average":
                                 if random_roll >= average:
                                        return (random_roll)
                                else:
                                        return (average)
                        
                                        
                        
                                



  