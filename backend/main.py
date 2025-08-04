import os
import sys
from flask import Flask, jsonify, request, send_from_directory
import requests
import threading
import webbrowser

def get_frontend_path():
    if getattr(sys, 'frozen', False):  # si en exe
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, "frontend")

app = Flask(__name__, static_folder=get_frontend_path())

API_BASE_URL = "https://api.altered.gg"

@app.route("/api/cards")
def get_cards():
    name = request.args.get("name", "")
    factions = request.args.getlist("factions")
    pageNumber = int(request.args.get("pageNumber", 1))
    sortOrder = request.args.get("sortOrder", "")
    priceMax = request.args.get("priceMax", "")

    try:
        params = {
            "query": name,
            "rarity": "Unique",
            "factions[]": ",".join(factions) if factions else None,
            "page": pageNumber,
            "inSale": "true",
            "itemsPerPage": 30,
            "locale": "fr-fr"
        }

        if sortOrder != "":
            sortSplit = sortOrder.split("_")
            params["order[" + sortSplit[0] + "]"] = sortSplit[1]

        if priceMax != "":
            params["priceMax"] = priceMax

        print(params)
        response = requests.get(API_BASE_URL + "/public/cards", params)
        response.raise_for_status()
        data = response.json()        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/cards/price")
def get_cards_price():
    reference = request.args.get("reference", "")
    try:
        response = requests.get(API_BASE_URL + "/public/cards/" + reference + "/offers")
        response.raise_for_status()
        data = response.json()        
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    def open_browser():
        webbrowser.open("http://localhost:5000")
    
    threading.Timer(1.0, open_browser).start()
    app.run()