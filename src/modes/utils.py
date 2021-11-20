def sign(x):
    return 1 if x >= 0 else -1


def constrain(x, min, max):
    return min if x < min else max if x > max else x


def approach(x, target, speed):
    dir = sign(target - x)
    next = x + dir * speed

    return constrain(next, min(x, target), max(x, target))
