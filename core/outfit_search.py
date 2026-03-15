import itertools
import random


class OutfitSearcher:

    def __init__(self, graph):
        self.G = graph


    def greedy_outfit(self, start_item):
        if start_item not in self.G:
            return []

        start_type = self.G.nodes[start_item]["type"]

        outfit = [start_item]
        used_types = {start_type}

        neighbors = sorted(
            self.G[start_item].items(),
            key=lambda x: x[1]["weight"],
            reverse=True
        )

        for node, data in neighbors:

            node_type = self.G.nodes[node]["type"]

            if node_type not in used_types:

                outfit.append(node)
                used_types.add(node_type)

        return outfit


    def best_outfit(self, required_types=None):
        if required_types is None:
            required_types = ["shirt", "pants", "shoes", "watch"]

        nodes_by_type = {
            t: [
                n for n, d in self.G.nodes(data=True)
                if d["type"] == t
            ]
            for t in required_types
        }

        best_combo = None
        best_score = -1

        for combo in itertools.product(*nodes_by_type.values()):

            score = self._combo_score(combo)

            if score > best_score:
                best_score = score
                best_combo = combo

        return {
            "outfit": best_combo,
            "score": best_score
        }


    def random_outfit(self, start_item, steps=3):
        if start_item not in self.G:
            return []

        current = start_item
        outfit = [current]

        for _ in range(steps):

            neighbors = list(self.G.neighbors(current))

            if not neighbors:
                break

            current = random.choice(neighbors)

            if current not in outfit:
                outfit.append(current)

        return outfit


    def _combo_score(self, nodes):
        score = 0

        for a, b in itertools.combinations(nodes, 2):

            if self.G.has_edge(a, b):
                score += self.G[a][b]["weight"]

        return score