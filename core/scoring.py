import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from core.color_theory import color_theory_score
from core.vibe_similarity import vibe_similarity


def color_similarity(vec1, vec2):
    """
    Cosine similarity between RGB vectors
    """

    v1 = np.array(vec1).reshape(1, -1)
    v2 = np.array(vec2).reshape(1, -1)

    return cosine_similarity(v1, v2)[0][0]


def formality_score(f1, f2):
    """
    Penalize mismatched formality
    """

    diff = abs(f1 - f2)

    if diff == 0:
        return 1.0
    elif diff == 1:
        return 0.7
    elif diff == 2:
        return 0.4
    else:
        return 0.1


def compatibility_score(item1, item2):

    color_sim = color_similarity(
        item1["color_vec"],
        item2["color_vec"]
    )
    color_theory = color_theory_score(
        item1["hue"],
        item2["hue"]
    )
    vibe_sim = vibe_similarity(
        item1["vibe"],
        item2["vibe"]
    )
    form_score = formality_score(
        item1["formality"],
        item2["formality"]
    )
    score = (
        0.35 * color_sim +
        0.25 * color_theory +
        0.25 * vibe_sim +
        0.15 * form_score
    )

    return round(score, 3)