# Roland Assistance SAV – Tooling und Dokumentation

Dieses Repository enthält ein leichtgewichtiges Kommandozeilenwerkzeug, mit dem
Support-Teams Servicefälle (Service Après-Vente, kurz SAV) für Roland Geräte
verwalten können. Das Skript `scripts/roland_sav.py` nutzt eine einfache
JSON-Datei als Datenspeicher und eignet sich damit für kleine Teams oder als
Ausgangspunkt für weitere Automatisierungen.

## Funktionsübersicht

- **Init** – legt eine neue, leere Datenbankdatei an.
- **Add** – erfasst einen neuen Supportfall mit Kundendaten, Produkt und Fehlerbild.
- **List** – listet vorhandene Fälle (optional nach Status gefiltert).
- **Update** – aktualisiert den Status und die Notizen eines bestehenden Falls.

## Voraussetzungen

- Python 3.9 oder neuer (für `dataclasses` und `typing` Features).
- Keine zusätzlichen Bibliotheken erforderlich.

## Schnellstart

1. Erstelle eine virtuelle Umgebung (optional, aber empfohlen):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Initialisiere die Datenbankdatei (Standard: `sav_cases.json` im Repository-Wurzelverzeichnis):

   ```bash
   python scripts/roland_sav.py init
   ```

3. Lege einen neuen Servicefall an:

   ```bash
   python scripts/roland_sav.py add \
       "Max Mustermann" \
       "support@example.com" \
       "Roland FP-30X" \
       "Z3L210045" \
       "Tasten reagieren unregelmäßig"
   ```

4. Liste alle offenen Fälle auf:

   ```bash
   python scripts/roland_sav.py list --status open
   ```

5. Aktualisiere den Status eines Falls, sobald eine Lösung vorliegt:

   ```bash
   python scripts/roland_sav.py update 1 closed --resolution-notes "Kontakte gereinigt, Funktion wiederhergestellt"
   ```

## Erweiterungsmöglichkeiten

- Export der Daten in CSV zur Weitergabe an externe Systeme.
- Anbindung an ein Ticketsystem oder CRM über REST-APIs.
- Automatisierte Benachrichtigungen (E-Mail/Slack) bei Statusänderungen.
- Ergänzung um Geräte-spezifische Prüfprotokolle für Roland Produkte.

## Support

Für Fragen zur Erweiterung oder Integration in bestehende Abläufe kann dieses
Repository als Ausgangspunkt dienen. Pull Requests mit Verbesserungen sind
willkommen.
