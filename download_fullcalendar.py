import os
import requests

# Definieer de URLs van de bestanden die we willen downloaden
FILES = {
    'css/main.min.css': 'https://cdn.jsdelivr.net/npm/fullcalendar@5.11.0/main.min.css',
    'js/main.min.js': 'https://cdn.jsdelivr.net/npm/fullcalendar@5.11.0/main.min.js',
    'js/interaction.min.js': 'https://cdn.jsdelivr.net/npm/@fullcalendar/interaction@5.11.0/main.min.js',
}

# Basis directory: neem aan dat dit de projectroot is, waar manage.py staat.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Doelmap binnen de static folder voor FullCalendar
DEST_DIR = os.path.join(BASE_DIR, 'static', 'fullcalendar')

def download_file(url, dest_path):
    print(f"Downloading {url} ...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            f.write(response.content)
        print(f"Saved to {dest_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    # Maak de doelmappen aan: css en js
    css_dir = os.path.join(DEST_DIR, 'css')
    js_dir = os.path.join(DEST_DIR, 'js')
    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(js_dir, exist_ok=True)
    
    # Download alle bestanden
    for relative_path, url in FILES.items():
        dest_path = os.path.join(DEST_DIR, relative_path)
        download_file(url, dest_path)
        
if __name__ == "__main__":
    main()
