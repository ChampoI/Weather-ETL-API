# Proyecto: ETL + API con datos del clima

import requests
from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

Base = declarative_base()

class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    temperature = Column(Float)
    humidity = Column(Integer)
    condition = Column(String)

engine = create_engine('sqlite:///weather.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def extract_weather(city_lat, city_lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": city_lat,
        "longitude": city_lon,
        "current_weather": True
    }
    response = requests.get(url, params=params)
    return response.json()

def transform_weather(data, city_name):
    current = data.get("current_weather", {})
    return {
        "city": city_name,
        "temperature": current.get("temperature"),
        "humidity": current.get("relative_humidity", 0),
        "condition": current.get("weathercode", "Unknown")
    }

def load_weather(entry):
    session = Session()
    weather = Weather(**entry)
    session.add(weather)
    session.commit()
    session.close()

def run_etl():
    cities = [
        {"name": "Bogotá", "lat": 4.61, "lon": -74.08},
        {"name": "Medellín", "lat": 6.25, "lon": -75.57},
        {"name": "Cali", "lat": 3.44, "lon": -76.52}
    ]
    for city in cities:
        raw = extract_weather(city["lat"], city["lon"])
        transformed = transform_weather(raw, city["name"])
        load_weather(transformed)

app = FastAPI()

@app.get("/weather")
def get_weather():
    session = Session()
    data = session.query(Weather).all()
    session.close()
    return JSONResponse([
        {"city": w.city, "temperature": w.temperature, "humidity": w.humidity, "condition": w.condition}
        for w in data
    ])

@app.get("/weather/{city_name}")
def get_city_weather(city_name: str):
    session = Session()
    result = session.query(Weather).filter(Weather.city == city_name.title()).first()
    session.close()
    if result:
        return {
            "city": result.city,
            "temperature": result.temperature,
            "humidity": result.humidity,
            "condition": result.condition
        }
    return JSONResponse({"error": "City not found"}, status_code=404)

if __name__ == "__main__":
    run_etl()
    uvicorn.run(app, host="0.0.0.0", port=8000)
