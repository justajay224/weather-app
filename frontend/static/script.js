async function getCityInfo() {
    const city = document.getElementById("cityInput").value.toUpperCase();
    if (!city) {
        alert("Masukkan nama kota terlebih dahulu!");
        return;
    }

    try {
        const response = await fetch(`http://localhost:8000/city-info/${city}`);
        const data = await response.json();

        // Jika API memberikan respons error
        if (!response.ok) {
            document.getElementById("result").innerHTML = `
                <p style="color:red; font-weight:bold;">❌ ${data.detail || "Kota tidak ditemukan!"}</p>
            `;
            return;
        }

        // Jika tidak ada error, tampilkan data 
        document.getElementById("result").innerHTML = `
            <h2>${data.city}</h2>
            <p><strong>🌡️ Suhu:</strong> ${data.temperature ?? "N/A"}°C</p>
            <p><strong>💧 Kelembaban:</strong> ${data.humidity ?? "N/A"}%</p>
            <p><strong>⛅ Kondisi:</strong> ${data.description ?? "N/A"}</p>
            <p><strong>💨 Kecepatan Angin:</strong> ${data.wind_speed ?? "N/A"} m/s</p>
            <p><strong>🏭 Indeks Kualitas Udara (AQI):</strong> ${data.air_quality_index ?? "N/A"}</p>
            <p><strong>📊 Kategori AQI:</strong> ${data.aqi_category ?? "N/A"}</p>
            <p><strong>🛑 CO:</strong> ${data.co ?? "N/A"} μg/m³</p>
            <p><strong>☁️ O3:</strong> ${data.o3 ?? "N/A"} μg/m³</p>
        `;
    } catch (error) {
        document.getElementById("result").innerHTML = `<p style="color:red; font-weight:bold;">❌ Gagal mengambil data!</p>`;
    }
}
