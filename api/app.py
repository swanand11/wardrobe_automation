import sys
import os
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, request
from flask_cors import CORS

from core.data_loader import WardrobeDataLoader
from core.graph_builder import WardrobeGraphBuilder
from core.outfit_search import OutfitSearcher


app = Flask(__name__)
CORS(app)

loader = WardrobeDataLoader()
df = loader.load()

builder = WardrobeGraphBuilder(df)
G = builder.build_graph()

search = OutfitSearcher(G)



@app.route("/")
def home():
    return jsonify({
        "message": "Wardrobe Graph API running"
    })


@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(loader.get_items())


@app.route("/items/<item_type>", methods=["GET"])
def get_items_by_type(item_type):
    return jsonify(loader.get_items_by_type(item_type))

@app.route("/suggest/<item_name>", methods=["GET"])
def suggest_outfit(item_name):

    outfit = search.greedy_outfit(item_name)

    return jsonify({
        "base_item": item_name,
        "outfit": outfit
    })


@app.route("/best", methods=["GET"])
def best_outfit():
    
    result = search.best_outfit()

    return jsonify(result)


@app.route("/random/<item_name>", methods=["GET"])
def random_outfit(item_name):
    
    outfit = search.random_outfit(item_name)

    return jsonify({
        "start_item": item_name,
        "outfit": outfit
    })


@app.route("/graph/stats", methods=["GET"])
def graph_stats():
    
    return jsonify({
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges()
    })

if __name__ == "__main__":
    app.run(debug=True,port=8000)