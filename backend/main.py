from flask import Flask, jsonify, request, send_from_directory
import requests

app = Flask(__name__, static_folder="../frontend")

API_BASE_URL = "https://api.altered.gg"

@app.route("/api/cards")
def get_cards():
    name = request.args.get("name", "")
    factions = request.args.getlist("factions")
    effect = request.args.get("effect", "")
    pageNumber = int(request.args.get("pageNumber", 1))

    try:
        params = {
            "query": f"{name} {effect}",
            "rarity": "Unique",
            "factions[]": ",".join(factions) if factions else None,
            "page": pageNumber,
            "inSale": True,
            "itemsPerPage": 30,
            "locale": "fr-fr"
        }
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
    app.run(debug=True)
