import os
from pathlib import Path

# Stel de hoofddirectory in (pas dit aan indien nodig)
base_dir = Path("C:/Users/Gebruiker/Documents/dentalmanager")

# Definieer de mappenstructuur als een dictionary
structure = {
    "": ["manage.py", "requirements.txt", "README.md"],
    "dentalmanager": ["__init__.py", "urls.py", "wsgi.py", "settings/base.py", "settings/development.py", "settings/production.py"],
    "apps": {
        "boekhouding": {
            "": ["__init__.py", "urls.py"],
            "tarieven": ["__init__.py", "models.py", "views.py", "urls.py", "forms.py"],
            "crediteuren": ["__init__.py", "models.py", "views.py", "urls.py", "forms.py"],
            "debiteuren": ["__init__.py", "models.py", "views.py", "urls.py", "forms.py"],
            "facturatie": ["__init__.py", "models.py", "views.py", "urls.py", "forms.py"],
            "laboratorium": ["__init__.py", "models.py", "views.py", "urls.py"],
            "kunstgebitaanhuis": ["__init__.py", "models.py", "views.py", "urls.py"],
            "marketing": ["__init__.py", "models.py", "views.py", "urls.py", "forms.py"],
            "totaal_overzicht": ["__init__.py", "views.py", "urls.py"],
        },
        "hr": {
            "": ["__init__.py", "urls.py"],
            "werknemers": ["__init__.py", "models.py", "views.py", "urls.py", "forms.py"],
            "salarisadministratie": ["__init__.py", "views.py", "urls.py"],
            "urenoverzicht": ["__init__.py", "views.py", "urls.py"],
            "verzekeringen": ["__init__.py", "views.py", "urls.py"],
            "belastingdienst": ["__init__.py", "views.py", "urls.py"],
            "uwv": ["__init__.py", "views.py", "urls.py"],
        },
        "planning": ["__init__.py", "models.py", "views.py", "urls.py", "apps.py"],
        "klanten": {},  # Voeg bestanden toe indien nodig
        "wagenpark": {},  # Voeg bestanden toe indien nodig
        "beheerderspagina": {},
        "log_in_pagina": {},
    },
    "templates": {
        "": ["base.html"],
        "partials": ["header.html", "footer.html"],
        "boekhouding": {
            "tarieven": [],
            "crediteuren": ["dashboard.html", "form.html", "detail.html"],
            "debiteuren": ["dashboard.html", "form.html", "detail.html"],
            "facturatie": ["dashboard.html", "form.html", "detail.html"],
            "laboratorium": ["dashboard.html"],
            "kunstgebitaanhuis": ["dashboard.html"],
            "marketing": [],
        },
        "hr": {
            "werknemers": ["index.html", "form.html", "detail.html"],
        },
        "planning": {},
    },
    "static": {
        "css": ["main.css", "boekhouding_laboratorium.css", "boekhouding_kunstgebitaanhuis.css", "hr.css"],
        "js": [],
        "images": [],
    },
    "mobile": {
        "android": {
            # Dit is een placeholder voor jouw Android Studio projectbestanden
            "app": [],
            "gradle": [],
            "": ["build.gradle", "gradlew", "gradlew.bat", "settings.gradle"],
        }
    }
}

def create_structure(base, struct):
    """
    Recursieve functie om de mappenstructuur te maken.
    base: de base directory als Path-object.
    struct: een dictionary waarin keys mappen zijn en waarden:
           - een lijst van bestandsnamen (strings)
           - of een dictionary met submappen.
    """
    for key, value in struct.items():
        # Als key een lege string is, dan worden de bestanden in de base gemaakt
        if key == "":
            if isinstance(value, list):
                for filename in value:
                    file_path = base / filename
                    # Maak het bestand als het niet bestaat
                    if not file_path.exists():
                        file_path.touch()
                        print(f"Created file: {file_path}")
            continue

        # Anders, maak eerst de map
        folder_path = base / key
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {folder_path}")

        if isinstance(value, list):
            # Maak alle bestanden in deze map
            for filename in value:
                file_path = folder_path / filename
                if not file_path.exists():
                    file_path.touch()
                    print(f"Created file: {file_path}")
        elif isinstance(value, dict):
            # Roep recursief de functie aan voor de subfolder
            create_structure(folder_path, value)

def main():
    create_structure(base_dir, structure)
    print("Mappenstructuur aangemaakt.")

if __name__ == "__main__":
    main()
