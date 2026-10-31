# Voronezh Public Cameras

This project provides a comprehensive catalog of officially published, open-to-public online web cameras in Voronezh, displayed on an interactive web map.

## Project Structure
- `src/scrapers/`: Adapters to scrape data from various sources (vrntube, geocam, etc.)
- `src/db.py`: SQLite database management.
- `src/geocoder.py`: Geocoding logic via OpenStreetMap Nominatim.
- `src/manager.py`: Main script to scrape, verify status, geocode, update DB, and export data.
- `src/app.py`: Flask web application for the interactive map interface.
- `data/`: Contains `cameras.db`.
- `cameras.json` / `cameras.csv`: Exported datasets.

## Requirements
- Python 3.8+

## Setup & Running on Windows 11
1. **Clone the repository:**
   ```powershell
   git clone <repo-url>
   cd <repo-name>
   ```
2. **Set up a virtual environment (recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Scrape data and generate datasets:**
   ```powershell
   $env:PYTHONPATH="."
   python src\manager.py
   ```
   This will create `cameras.db`, `cameras.json`, `cameras.csv`, and `REPORT.md`.
5. **Run the Web Application:**
   ```powershell
   $env:PYTHONPATH="."
   python src\app.py
   ```
   Open `http://localhost:3000` in your web browser.

## Testing
Run automated tests with pytest:
```powershell
$env:PYTHONPATH="."
pytest
```
