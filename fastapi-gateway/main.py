from fastapi import FastAPI, HTTPException
import requests
import os
import re
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# URL dari microservices(express buat cuaca, flask buat kualitas udara)
EXPRESS_API_URL = "http://express-service:3001/weather"
FLASK_API_URL = "http://flask-service:3002/air_quality"


#gak tau apa-solusi dari AI karena sebelumnya gak bisa beriman req dari frontend, mungkin sama kaya yang ada di express cors itu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Izinkan semua domain
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua metode HTTP
    allow_headers=["*"],  # Izinkan semua header
)

# Fungsi untuk mengecek apakah input kota valid (hanya huruf dan spasi)
def is_valid_city(city):
    return bool(re.match("^[a-zA-ZÀ-ÿ ]+$", city))  # Mendukung huruf dengan aksen (misalnya São Paulo)

@app.get("/city-info/{city}")
def get_city_info(city: str):
    if not is_valid_city(city):
        raise HTTPException(status_code=400, detail="Nama kota tidak valid. Gunakan hanya huruf dan spasi.")

    try:
        # Ambil data dari microservices(express dan flask)
        weather_response = requests.get(f"{EXPRESS_API_URL}/{city}")
        air_quality_response = requests.get(f"{FLASK_API_URL}/{city}")

        #cek status yang diberikan, detail soal status bisa googling "status code"
        if weather_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Data cuaca tidak ditemukan untuk kota tersebut.")

        if air_quality_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Data kualitas udara tidak ditemukan untuk kota tersebut.")

        weather_data = weather_response.json()
        air_quality_data = air_quality_response.json()

        # Tambahan buat kategori kualitas udara
        def categorize_aqi(pm2_5):
            if pm2_5 <= 12:
                return "Good 😊 (Baik)"
            elif pm2_5 <= 35:
                return "Moderate 😐 (Sedang)"
            elif pm2_5 <= 55:
                return "Unhealthy for sensitive groups 😷 (Tidak Sehat untuk Kelompok Sensitif)"
            elif pm2_5 <= 150:
                return "Unhealthy 😵 (Tidak Sehat)"
            elif pm2_5 <= 250:
                return "Very Unhealthy ☠️ (Sangat Tidak Sehat)"
            else:
                return "Hazardous ☢️ (Berbahaya)"

        aqi_category = categorize_aqi(air_quality_data.get("air_quality_index", 0))

        combined_data = {
            "city": city,
            "temperature": weather_data.get("temperature"),
            "humidity": weather_data.get("humidity"),
            "description": weather_data.get("description"),
            "wind_speed": weather_data.get("wind_speed"),
            "air_quality_index": air_quality_data.get("air_quality_index"),
            "aqi_category": aqi_category,
            "co": air_quality_data.get("co"),
            "o3": air_quality_data.get("o3")
        }

        return combined_data

    except HTTPException as e:
        raise e  # Kirim error FastAPI
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan server: {str(e)}")
    





