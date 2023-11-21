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
                num_dice_1, dice_value_1 = int(input_str.split('d'))
                roll = sum([random.randint(1, dice_value_1) for _ in range(num_dice_1)])
                result = result + roll

            elif 'd' not in input_str:
                # Add the modifier
                result = result + int(input_str)

            # stop rolling dice
            rolling = False

    return result


# total_roll = roll_dice("10+6")
# print("Your total of all rolled dice = " + str(total_roll))
