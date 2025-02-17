const express = require("express");
const axios = require("axios");
require("dotenv").config();

const app = express();
const PORT = 3001;
const API_KEY = process.env.WEATHER_API_KEY;

// Middleware untuk menangani request dari frontend
const cors = require("cors");
app.use(cors());

app.get("/weather/:city", async (req, res) => {
    const { city } = req.params;
    try {
        const response = await axios.get(`http://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`);
        
        // Ambil data yang dipake
        const weatherData = {
            city: response.data.name,
            temperature: response.data.main.temp,
            humidity: response.data.main.humidity,
            description: response.data.weather[0].description,
            wind_speed: response.data.wind.speed
        };

        res.json(weatherData);
    } catch (error) {
        res.status(500).json({ error: "Gagal mengambil data cuaca" });
    }
});


app.listen(PORT, () => console.log(`Express server berjalan di http://localhost:${PORT}`));
