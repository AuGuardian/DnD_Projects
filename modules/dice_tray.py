import random


def dice_roll(input_str):
    result = 0
    rolling = True

    while rolling:
        if '+' in input_str:

            # Separate the first roll from the string
            first_half, second_half = input_str.split('+', 1)

            # check if the separated value is a modifier or a die roll
            if 'd' in first_half:
                # Roll the dice
                num_dice_1, dice_value_1 = map(int, first_half.split('d'))
                roll = sum([random.randint(1, dice_value_1) for _ in range(num_dice_1)])
                result = result + roll

            elif 'd' not in first_half:
                # Add the modifier
                result = int(first_half)

            # put the remaining rolls/modifiers back in the input string
            input_str = second_half

        else:
            # check if the remaining value is a modifier or a die roll
            if 'd' in input_str:
                # Roll the dice
                num_dice_1, dice_value_1 = map(int, input_str.split('d'))
                roll = sum([random.randint(1, dice_value_1) for _ in range(num_dice_1)])
                result = result + roll

            elif 'd' not in input_str:
                # Add the modifier
                result = result + int(input_str)

            # stop rolling dice
            rolling = False

    return result


def calculate_average(input_str):
    result = 0
    die_count = 0
    die_value = 0
    modifier = 0

    # Check if the input string is valid to check the average HP
    if check_string(input_str):
        # Separate the die count from the string
        die_count, second_half = input_str.split('d')

        # Separate the die value and the modifier
        die_value, modifier = second_half.split('+')

        # Calculate the average hp
        result = ((((int(die_value) + 1) / 2) * int(die_count)) + int(modifier))

    if not check_string(input_str):
        print("Value not Valid")

    return result, die_count, die_value, modifier


def check_string(input_string):
    # Count occurrences of 'd' and '+'
    count_d = input_string.count('d')
    count_plus = input_string.count('+')

    # Check if 'd' and '+' occur exactly once each
    if count_d == 1 and count_plus == 1:
        return True
    else:
        return False


def hp_roll(input_str):
    average, count, value, mod = calculate_average(input_str)
    result = 0

    # Roll all health die
    for x in range(int(count)):
        roll = random.randint(1, int(value))
        print("Roll = " + str(roll))
        result = result + roll
        print("Current HP = " + str(result))

    result = result + int(mod)
    print("HP roll = " + str(result))
    print("Average HP = " + str(average))

    # Replace rolled result with average when rolled value is lower (makes for stronger monsters)
    if result < average:
        result = average

    return result


def initiative_roll(input_str):

    roll = float(dice_roll("1d20"))
    result = roll + float(input_str) + ((float(input_str) + 10) / 100)
    # dex value is added after decimal point to break tied initiative

    return result


def roll_monster_data(health_roll, dex):
    # Roll Health and Initiative for the Monster
    health = hp_roll(health_roll)
    initiative = initiative_roll(dex)

    # Create the HP-bar in the Health tracker window
    # ...Yet to program...

    return health, initiative


if __name__ == "__main__":
    total_roll = hp_roll("4d8+8")
    print("Your total HP = " + str(total_roll))
