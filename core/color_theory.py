import math


def _hue_distance(h1, h2):
    diff = abs(h1 - h2) % 360
    return min(diff, 360 - diff)

def complementary(h1, h2):
    return abs(_hue_distance(h1, h2) - 180) <= 25


def analogous(h1, h2):
    
    return _hue_distance(h1, h2) <= 30


def triadic(h1, h2):
    
    return abs(_hue_distance(h1, h2) - 120) <= 25


def color_theory_score(h1, h2):

    if complementary(h1, h2):
        return 1.0

    if analogous(h1, h2):
        return 0.8

    if triadic(h1, h2):
        return 0.7

    return 0.3