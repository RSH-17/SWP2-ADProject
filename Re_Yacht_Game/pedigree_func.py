"""

주사위 족보 함수 모음

"""


def aces(dice_dict):
    val = dice_dict[1]
    return val * 1


def deuces(dice_dict):
    val = dice_dict[2]
    return val * 2


def threes(dice_dict):
    val = dice_dict[3]
    return val * 3


def fours(dice_dict):
    val = dice_dict[4]
    return val * 4


def fives(dice_dict):
    val = dice_dict[5]
    return val * 5


def sixes(dice_dict):
    val = dice_dict[6]
    return val * 6


def choice(dice_dict):
    score = 0

    for key, value in dice_dict.items():
        score += key * value

    return score


def four_of_kind(dice_dict):
    score = 0

    for key, value in dice_dict.items():
        if value >= 4:
            score = key * 4             # 만약 동일한 주사위 5개라도 4개만 인정
            break

    return score


def full_house(dice_dict):
    score = 0
    a = 0

    for key, value in dice_dict.items():
        if value == 3:
            a += 3

        if value == 2:
            a += 2

        if value == 5:
            a += 5

    if a == 5:
        for key, value in dice_dict.items():
            score += key * value

    return score


def s_straight(dice_dict):
    if (dice_dict[3] and dice_dict[4]) >= 1:

        if (dice_dict[1] and dice_dict[2]) >= 1:
            return 15

        if (dice_dict[2] and dice_dict[5]) >= 1:
            return 15

        if (dice_dict[5] and dice_dict[6]) >= 1:
            return 15

    return 0


def l_straight(dice_dict):
    if (dice_dict[2] and dice_dict[3] and dice_dict[4] and dice_dict[5]) >= 1:
        if dice_dict[1] >= 1:
            return 30

        if dice_dict[6] >= 1:
            return 30

    return 0


def yacht(dice_dict):
    for key, value in dice_dict.items():
        if value == 5:
            return 50

    return 0


if __name__ == "__main__":
    dice = {1: 1, 2: 0, 3: 1, 4: 1, 5: 1, 6: 1}
    print(l_straight(dice))
