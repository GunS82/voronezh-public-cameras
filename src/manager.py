import json
import csv
import os
import requests
from datetime import datetime
from src.scrapers import VrntubeScraper, GeocamScraper, KvantScraper
from src.db import init_db, save_camera, get_all_cameras
from src.geocoder import enhance_with_coords

def check_status(url):
    try:
        r = requests.head(url, timeout=5, allow_redirects=True, verify=False)
        if r.status_code < 400:
            return 'works'
        return 'not working'
    except Exception:
        return 'not working'

def run():
    init_db()
    
    scrapers = [VrntubeScraper(), GeocamScraper(), KvantScraper()]
    report = ["# Отчёт по источникам веб-камер Воронежа\n"]
    
    all_cameras = []
    
    for scraper in scrapers:
        print(f"Running {scraper.name}...")
        cams, result_msg = scraper.scrape()
        report.append(f"## {scraper.name}")
        report.append(f"Результат: {result_msg}")
        
        for cam in cams:
            print(f"Checking status for {cam['title']}...")
            cam['status'] = check_status(cam['url'])
            cam['last_checked'] = datetime.now().isoformat()
            
            # Using Geocoder strictly per request if coordinate extraction from site didn't yield anything
            print(f"Geocoding {cam['title']}...")
            cam = enhance_with_coords(cam)
            save_camera(cam)
            all_cameras.append(cam)
            
    db_cameras = get_all_cameras()
    
    unique_cameras = len(db_cameras)
    working_cameras = len([c for c in db_cameras if c['status'] == 'works'])
    
    report.append("\n## Сводка")
    report.append(f"- **Количество уникальных камер**: {unique_cameras}")
    report.append(f"- **Количество проверенных рабочих трансляций**: {working_cameras}")
    
    with open('REPORT.md', 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    export_data(db_cameras)

def export_data(cameras):
    with open('cameras.json', 'w', encoding='utf-8') as f:
        json.dump(cameras, f, ensure_ascii=False, indent=2)
        
    if cameras:
        keys = cameras[0].keys()
        with open('cameras.csv', 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(cameras)

if __name__ == '__main__':
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    run()
