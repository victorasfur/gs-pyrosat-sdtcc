import os
from flask import Flask, render_template, jsonify
from datetime import datetime
import random
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

app = Flask(__name__)

APPINSIGHTS_KEY = os.environ.get("APPINSIGHTS_INSTRUMENTATIONKEY", "")
if APPINSIGHTS_KEY:
    logger = logging.getLogger(__name__)
    logger.addHandler(AzureLogHandler(connection_string=f"InstrumentationKey={APPINSIGHTS_KEY}"))
    

# Simulated satellite fire data (INPE/NASA FIRMS style)
FIRE_DATA = [
    {"id": 1, "lat": -8.5, "lon": -45.2, "frp": 98.4, "state": "PI", "biome": "Cerrado", "confidence": "high", "timestamp": "2024-01-15T14:32:00Z"},
    {"id": 2, "lat": -9.1, "lon": -63.7, "frp": 142.1, "state": "RO", "biome": "Amazônia", "confidence": "high", "timestamp": "2024-01-15T13:55:00Z"},
    {"id": 3, "lat": -12.4, "lon": -51.8, "frp": 76.3, "state": "MT", "biome": "Cerrado", "confidence": "nominal", "timestamp": "2024-01-15T13:20:00Z"},
    {"id": 4, "lat": -15.6, "lon": -52.1, "frp": 55.7, "state": "MT", "biome": "Cerrado", "confidence": "nominal", "timestamp": "2024-01-15T12:45:00Z"},
    {"id": 5, "lat": -10.3, "lon": -67.8, "frp": 200.5, "state": "AC", "biome": "Amazônia", "confidence": "high", "timestamp": "2024-01-15T14:10:00Z"},
    {"id": 6, "lat": -6.2, "lon": -47.5, "frp": 45.2, "state": "MA", "biome": "Cerrado", "confidence": "low", "timestamp": "2024-01-15T11:30:00Z"},
    {"id": 7, "lat": -16.8, "lon": -48.9, "frp": 88.9, "state": "GO", "biome": "Cerrado", "confidence": "high", "timestamp": "2024-01-15T14:00:00Z"},
    {"id": 8, "lat": -3.5, "lon": -60.1, "frp": 165.3, "state": "AM", "biome": "Amazônia", "confidence": "high", "timestamp": "2024-01-15T13:40:00Z"},
]

ALERTS = [
    {"level": "CRÍTICO", "region": "Rondônia - Zona Rural", "risk": 95, "wind": "23 km/h NE", "humidity": "18%", "spread": "Alta probabilidade de alastramento em 6h"},
    {"level": "ALTO", "region": "Mato Grosso - Beira MT-040", "risk": 78, "wind": "17 km/h E", "humidity": "24%", "spread": "Moderada probabilidade de alastramento em 12h"},
    {"level": "MODERADO", "region": "Maranhão - Sul", "risk": 52, "wind": "12 km/h NE", "humidity": "35%", "spread": "Baixa probabilidade de alastramento em 24h"},
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/fires")
def get_fires():
    return jsonify({
        "fires": FIRE_DATA,
        "total": len(FIRE_DATA),
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "source": "INPE/NASA FIRMS (simulado)"
    })

@app.route("/api/alerts")
def get_alerts():
    return jsonify({
        "alerts": ALERTS,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    })

@app.route("/api/stats")
def get_stats():
    return jsonify({
        "active_fires": len(FIRE_DATA),
        "critical_alerts": sum(1 for a in ALERTS if a["level"] == "CRÍTICO"),
        "area_risk_km2": 2847,
        "satellites_active": 3,
        "last_pass": "14:32 UTC",
        "ods_connected": ["ODS 13", "ODS 15", "ODS 11"]
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "PyroSat", "version": "1.0.0"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
