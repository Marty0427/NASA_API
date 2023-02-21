# NASA NEO API
REST API for near-earth objects

## Usage
- set the apikey in *app.py*
- uvicorn app:app --host 0.0.0.0 --port 8000

### Docker
**docker build -t nasa-app .**
**docker run -p 8000:8000 nasa-app**

## Description
- returns data of near earth objects from NASA api: https://api.nasa.gov/ sorted from nearest