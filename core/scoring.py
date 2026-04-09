import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from core.color_theory import color_theory_score
from core.vibe_similarity import vibe_similarity


def color_similarity(vec1, vec2):
    """Cosine similarity between two RGB vectors."""
    v1 = np.array(vec1).reshape(1, -1)
    v2 = np.array(vec2).reshape(1, -1)
    return cosine_similarity(v1, v2)[0][0]


def formality_score(f1, f2):
    """Penalize mismatched formality levels."""
    diff = abs(f1 - f2)
    if diff == 0:   return 1.0
    if diff == 1:   return 0.7
    if diff == 2:   return 0.4
    return 0.1


def _watch_representative_vec(item):
    """
    For watches, return strap_color_vec as the primary compatibility vector
    (the strap is what's visually prominent against clothing).
    Falls back to the main color_vec if strap not available.
    """
    strap = item.get("strap_color_vec")
    if strap:
        return strap
    return item["color_vec"]


def _watch_hue(item):
    """Return strap hue for watches if available, else main hue."""
    if item.get("type") == "watch":
        h = item.get("strap_hue")
        if h is not None and str(h).strip() != "":
            return float(h)
    return item["hue"]


def compatibility_score(item1, item2):
    """
    Score compatibility between two wardrobe items.
    Watches use strap colour for clothing compatibility checks.
    """
    vec1 = _watch_representative_vec(item1) if item1.get("type") == "watch" else item1["color_vec"]
    vec2 = _watch_representative_vec(item2) if item2.get("type") == "watch" else item2["color_vec"]

    hue1 = _watch_hue(item1)
    hue2 = _watch_hue(item2)

    color_sim    = color_similarity(vec1, vec2)
    color_theory = color_theory_score(hue1, hue2)
    vibe_sim     = vibe_similarity(item1["vibe"], item2["vibe"])
    form_score   = formality_score(item1["formality"], item2["formality"])

    score = (
        0.35 * color_sim +
        0.25 * color_theory +
        0.25 * vibe_sim +
        0.15 * form_score
    )
    return round(score, 3)