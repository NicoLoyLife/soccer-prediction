# Soccer Predictor

**Soccer Predictor** ist ein Backend-System zur Vorhersage von Fußballspielausgängen basierend auf historischen Daten und aktuellen Informationen von externen APIs. Es verwendet statistische Modelle, um Wahrscheinlichkeiten für verschiedene Spielausgänge zu berechnen, einschließlich Sieg, Niederlage, Unentschieden, Über-/Unter-Tore und Beide Teams treffen.

## **Inhaltsverzeichnis**

- [Features](#features)
- [Technologien](#technologien)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Projektstruktur](#projektstruktur)
- [Nächste Schritte](#nächste-schritte)
- [Mitwirken](#mitwirken)
- [Lizenz](#lizenz)

## **Features**

- Abruf und Speicherung von Fußballspieldaten von externen APIs
- Berechnung und Speicherung von statistischen Features für Vorhersagen
- Vorhersagemodul zur Berechnung von Spielausgangswahrscheinlichkeiten
- RESTful API für den internen Gebrauch zur Integration in Frontend-Anwendungen
- Docker-Containerisierung für konsistente Entwicklungs- und Produktionsumgebungen

## **Technologien**

- **Python 3.10**: Programmiersprache für die Entwicklung
- **Django**: Web-Framework für das Backend
- **Django REST Framework**: Framework für die Erstellung von RESTful APIs
- **PostgreSQL**: Datenbankmanagementsystem
- **Docker & Docker Compose**: Containerisierung und Orchestrierung
- **python-dotenv**: Handhabung von Umgebungsvariablen
- **Poisson-Verteilung und andere statistische Modelle**: Für die Vorhersage von Spielergebnissen

## **Voraussetzungen**

Stelle sicher, dass die folgenden Tools installiert sind:

- [Python 3.10](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

## **Installation**

1. **Repository klonen:**

   ```bash
   git clone https://github.com/DEIN_BENUTZERNAME/soccer-predictor.git
   cd soccer-predictor
   ```

2. **.env-Datei erstellen:**

   Erstelle eine `.env`-Datei im Stammverzeichnis mit den notwendigen Umgebungsvariablen. Beispiel:

   ```plaintext
   DJANGO_SECRET_KEY='dein-geheimer-schlüssel'
   POSTGRES_DB='soccer_predictor_db'
   POSTGRES_USER='user'
   POSTGRES_PASSWORD='password'
   DB_HOST='db'
   DB_PORT='5432'
   ```

3. **Docker-Container erstellen und starten:**

   ```bash
   docker-compose up --build
   ```

   Dies erstellt und startet die Anwendung in einem Docker-Container.

4. **Superuser erstellen (optional):**

   ```bash
   docker-compose run web python manage.py createsuperuser
   ```

   Folge den Anweisungen, um einen Admin-Benutzer zu erstellen.

## **Verwendung**

- Die Anwendung ist unter `http://localhost:8000` verfügbar.
- Verwende die Django-Admin-Oberfläche unter `http://localhost:8000/admin` für Verwaltungsaufgaben.

## **Projektstruktur**

```plaintext
soccer_predictor/       # Hauptverzeichnis des Projekts
├── Dockerfile          # Docker-Konfigurationsdatei
├── docker-compose.yml  # Docker Compose-Konfigurationsdatei
├── manage.py           # Django's Management-Skript
├── requirements.txt    # Python-Abhängigkeiten
├── .env.example        # Beispiel für Umgebungsvariablen (sollte erstellt und angepasst werden)
├── soccer_predictor/   # Django-Projektverzeichnis
│   ├── __init__.py
│   ├── settings.py     # Django-Einstellungen (verwenden Umgebungsvariablen aus .env)
│   ├── urls.py
│   └── wsgi.py
├── predictions/        # Django-App für Vorhersagen
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py       # Datenmodelle
│   ├── views.py        # API-Views
│   └── ...             # Weitere App-Dateien
└── ...                 # Weitere Dateien/Verzeichnisse
```

## **Nächste Schritte**

- Implementierung von Datenmodellen für Teams, Spiele und Vorhersagen
- Entwicklung und Integration der statistischen Modelle zur Vorhersage
- Erstellung und Testen von RESTful API-Endpunkten
- Deployment des Projekts in einer Produktionsumgebung

## **Mitwirken**

Beiträge sind willkommen! Bitte erstelle einen Pull-Request oder eröffne ein Issue, um zur Entwicklung beizutragen.

## **Lizenz**

Dieses Projekt steht unter der MIT-Lizenz. Siehe die [LICENSE](LICENSE)-Datei für weitere Informationen.
