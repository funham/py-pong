def sign(x):
    return 1 if x >= 0 else -1


def constrain(x, min_x, max_x):
    return x if (min_x < x < max_x) else (min_x if x < min_x else max_x)


def approach(x, target, speed):
    dir = sign(target - x)
    t = x + speed * dir
    return constrain(t, min(x, target), max(x, target))
