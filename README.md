# Weather ETL + API

Este proyecto realiza un proceso ETL usando datos públicos del clima (Open-Meteo) y expone una API con FastAPI.

## 🧩 Instrucciones

1. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

2. Ejecuta el proyecto:
   ```
   python main.py
   ```

3. Accede a la API:
   - Todos los datos: [http://localhost:8000/weather](http://localhost:8000/weather)
   - Buscar por ciudad: [http://localhost:8000/weather/Bogotá](http://localhost:8000/weather/Bogotá)
   - Documentación Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🗂 Ciudades incluidas
- Bogotá
- Medellín
- Cali

## 🧰 Tecnologías
- Python
- FastAPI
- SQLAlchemy
- SQLite
