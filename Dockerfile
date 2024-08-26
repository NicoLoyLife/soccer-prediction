# Verwende ein offizielles Python-Runtime-Image als Basis
FROM python:3.10-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die requirements-Datei in den Container
COPY requirements.txt /app/

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Inhalt des Projekts in den Container
COPY . /app/

# Öffne den Port, auf dem die App laufen wird
EXPOSE 8000

# Führe die Anwendung aus
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]