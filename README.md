# Wardrobe Automation

A lightweight wardrobe outfit suggestion app that recommends style combinations based on item attributes, color theory, and a graph-based compatibility engine.

## 🚀 Project Overview

The project has three main layers:

1. **Data Loader** (`core/data_loader.py`) - loads item data from `data/wadrobe.csv` and extracts structured item features.
2. **Graph Builder** (`core/graph_builder.py`) - constructs a weighted compatibility graph where nodes are wardrobe items and edges represent stylistic similarity.
3. **Outfit Searcher** (`core/outfit_search.py`) - finds outfit suggestions using greedy, best, and random path search methods over the graph.

The backend API is in `api/app.py`, and a simple static frontend is in `ui/`.

## 🧠 Core Concepts

### Color Theory Engine

The app uses color attributes in each item to compute similarity:
- Parse color and vibe fields from the raw CSV
- Compute compatibility using color distance and vibe overlap
- Score item pairs so that similar/correct-color outfits are preferred

This is primarily implemented in `core/color_theory.py` and integrated during graph edge construction.

### Graph Engine

`core/graph_builder.py` builds an undirected weighted graph (networkx) where:
- Nodes = wardrobe items
- Edge weight = compatibility score (higher means more compatible)

This graph enables outfit search algorithms to traverse nearest neighbors and produce combinations that are stylistically coherent.

### Outfit Search Strategies

`core/outfit_search.py` supports:
- `greedy_outfit(item)` – picks top-connected neighbors from a base item
- `best_outfit()` – finds best outfit by scoring candidate sets using overall compatibility
- `random_outfit(item)` – picks random item chains for variety

## 🧩 Folder Structure

- `api/` – Flask API server
- `core/` – main logic modules (data loader, color theory, graph builder, search, scoring)
- `data/` – input dataset CSV
- `ui/` – static frontend HTML/CSS/JS

## ▶️ Run Locally

1. Create and activate your venv:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run backend API:
   ```bash
   python3 api/app.py
   ```
3. Serve UI (or open directly):
   ```bash
   cd ui
   python3 -m http.server 8000
   ```
4. Open frontend at `http://127.0.0.1:8000` and use the dropdown to get outfit suggestions.

## 🔧 API Endpoints

- `GET /` – health message
- `GET /items` – all items
- `GET /items/<type>` – items filtered by type
- `GET /suggest/<item_name>` – suggest outfit starting from item
- `GET /best` – best outfit suggestion
- `GET /random/<item_name>` – random outfit chain
- `GET /graph/stats` – nodes and edges counts

## ✅ Quick Troubleshooting

- If UI dropdown is empty:
  1) Ensure backend is running on `http://127.0.0.1:5000`
  2) Ensure CORS is enabled in `api/app.py` (`flask-cors` installed)
  3) Serve UI from `http://127.0.0.1:8000` and open browser console for errors.

## 📌 Notes

- The system is designed for experimentation. Add new item rows in `data/wadrobe.csv` (with `item_name`, `type`, `color`, `vibe`, etc.) and the graph will adapt.
- For better outfits, tune scoring logic in `core/scoring.py` and similarity rules in `core/color_theory.py`.

---

Built for quick wardrobe automation and outfit recommendation demos.