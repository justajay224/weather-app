from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# API buat layanan kualitas udara
API_KEY = os.getenv("AIR_QUALITY_API_KEY")
API_URL = "https://api.weatherapi.com/v1/current.json"

@app.route("/air_quality/<city>", methods=["GET"])
def get_air_quality(city):
    try:
        # Ambil data kualitas udara dari API
        response = requests.get(f"{API_URL}?key={API_KEY}&q={city}&aqi=yes")
        data = response.json()

        # Ambil data yang dipake
        air_quality_data = {
            "city": city,
            "air_quality_index": data["current"]["air_quality"]["pm2_5"],  # Partikel PM2.5
            "co": data["current"]["air_quality"]["co"],  # Karbon monoksida
            "o3": data["current"]["air_quality"]["o3"],  # Ozon
        }

        return jsonify(air_quality_data)
    except Exception as e:
        return jsonify({"error": "Gagal mengambil data kualitas udara", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002, debug=True)
