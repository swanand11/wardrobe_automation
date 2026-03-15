import networkx as nx
from itertools import combinations
from core.scoring import compatibility_score

class WardrobeGraphBuilder:

    def __init__(self, df):
        self.df = df
        self.graph = nx.Graph()

    def build_graph(self):
        self._add_nodes()
        self._add_edges()

        return self.graph

    def _add_nodes(self):
        for _, row in self.df.iterrows():

            self.graph.add_node(
                row["item_name"],
                type=row["type"],
                data=row.to_dict()
            )

    def _add_edges(self):
        items = list(self.df.to_dict("records"))

        for item1, item2 in combinations(items, 2):
            if item1["type"] == item2["type"]:
                continue

            score = compatibility_score(item1, item2)
            if score > 0.35:

                self.graph.add_edge(
                    item1["item_name"],
                    item2["item_name"],
                    weight=score
                )

    def get_graph(self):
        return self.graph