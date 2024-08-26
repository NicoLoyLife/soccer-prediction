# Soccer Predictor

**Soccer Predictor** ist ein Backend-System zur Vorhersage von Fußballspielausgängen basierend auf historischen Daten und aktuellen Informationen von externen APIs. Es verwendet statistische Modelle, um Wahrscheinlichkeiten für verschiedene Spielausgänge zu berechnen, einschließlich Sieg, Niederlage, Unentschieden, Über-/Unter-Tore und Beide Teams treffen.

## **Inhaltsverzeichnis**

- [Features](#features)
- [Technologien](#technologien)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Projektstruktur](#projektstruktur)
- [Logging-Konfiguration](#logging-konfiguration)
- [Testing-Infrastruktur](#testing-infrastruktur)
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

- **Python 3.11**: Programmiersprache für die Entwicklung
- **Django**: Web-Framework für das Backend
- **Django REST Framework**: Framework für die Erstellung von RESTful APIs
- **PostgreSQL**: Datenbankmanagementsystem
- **Docker & Docker Compose**: Containerisierung und Orchestrierung
- **python-dotenv**: Handhabung von Umgebungsvariablen
- **pytest & pytest-django**: Test-Frameworks für Django

## **Voraussetzungen**

Stelle sicher, dass die folgenden Tools installiert sind:

- [Python 3.11](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

## **Installation**

1. **Repository klonen:**

   ```bash
   git clone https://github.com/NicoLoyLife/soccer-predictor.git
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

4. **Datenbankmigrationen anwenden**

    Bevor du eine Superuser erstellst, führe die Migrationsbefehle aus, um sicherzustellen, dass die Datenbankstruktur korrekt eingerichtet ist:

    ```bash
    docker-compose run web python manage.py makemigrations
    docker-compose run web python manage.py migrate
    ```

5. **Superuser erstellen (optional):**

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
├── pytest.ini          # pytest-Konfigurationsdatei
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
│   └── tests/          # Testverzeichnis für die App
│       ├── __init__.py
│       └── test_models.py
└── ...                 # Weitere Dateien/Verzeichnisse
```

## **Logging-Konfiguration**

Das Projekt verwendet eine einfache Logging-Konfiguration, die alle Log-Meldungen auf `DEBUG`-Level in eine Datei namens `django_debug.log` im Stammverzeichnis des Projekts speichert.

Um die Logging-Konfiguration anzupassen, öffne `settings.py` und ändere die `LOGGING`-Einstellungen entsprechend deinen Anforderungen.

Beispiel für die `LOGGING`-Konfiguration:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## **Testing-Infrastruktur**

Die Testing-Infrastruktur basiert auf `pytest` und `pytest-django`. Um die Tests auszuführen, verwende einfach den Befehl:

```bash
pytest
```

Stelle sicher, dass alle neuen Funktionen durch Tests abgedeckt werden. Beispieltests befinden sich im Verzeichnis `predictions/tests/`.

## **Nächste Schritte**

- Implementierung weiterer Datenmodelle für Teams, Spiele und Vorhersagen
- Entwicklung und Integration der statistischen Modelle zur Vorhersage
- Erstellung und Testen zusätzlicher RESTful API-Endpunkte
- Einrichtung einer CI/CD-Pipeline für automatisierte Tests und Deployments

## **Mitwirken**

Beiträge sind willkommen! Bitte erstelle einen Pull-Request oder eröffne ein Issue, um zur Entwicklung beizutragen.

## **Lizenz**

Dieses Projekt steht unter der MIT-Lizenz. Siehe die [LICENSE](LICENSE)-Datei für weitere Informationen.
