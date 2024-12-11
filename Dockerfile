# Verwenden Sie ein offizielles Python-Basisimage
FROM python:3.8-alpine

# Arbeitsverzeichnis im Container festlegen
WORKDIR /app

COPY . .

# Kopieren der Abhängigkeiten-Datei
COPY requirements.txt .

# Installieren von Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des Quellcodes in das Arbeitsverzeichnis im Container
COPY src/ ./src/

# Kopieren der Assets in das Arbeitsverzeichnis im Container
COPY assets/ ./assets/

# Umgebungsvariable setzen, um Flask im Produktionsmodus laufen zu lassen
ENV FLASK_ENV=production

# Port, auf dem die Anwendung läuft, freigeben
EXPOSE 5000

# Befehl zum Starten der Flask-Anwendung
CMD ["python", "src/main.py"]
