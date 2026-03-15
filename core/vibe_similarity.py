def vibe_similarity(v1, v2):

    if not v1 or not v2:
        return 0

    s1 = set(v1)
    s2 = set(v2)

    intersection = len(s1.intersection(s2))
    union = len(s1.union(s2))

    return intersection / union