# LTS Quality Management

Datengestütztes Concession Management & Fahrer-Coaching Tool.

## Features

- 📊 **Action Roadmap** - Priorisierte Maßnahmen basierend auf Root Cause Analyse
- 👥 **Fahrer Watchlist** - Pareto-Analyse aller Fahrer nach Problemkategorien
- 📈 **Trend Analyse** - Wöchentliche Entwicklung und ZIP-Code Heatmap
- 🎓 **Coaching Tool** - Automatische Coaching-Skripte pro Fahrer

## Daten-Format

Unterstützt CSV und Excel (xlsx/xls) mit folgenden Spalten:
- `transporter_id` - Fahrer-ID
- `tracking_id` - Paket-Tracking-Nummer
- `year_week` - Kalenderwoche (z.B. "2025-44")
- `zip_code` - Postleitzahl
- `Concession Cost` - Kosten
- `Geo Distance > 25m` - GPS-Abweichung (0/1)
- `Delivered to Household Member / Customer` - Übergabe-Flag (0/1)
- `Delivery preferences not followed` - Präferenzen ignoriert (0/1)
- `Feedback False Scan Indicator` - False Scan (Y/N)
- `High Value Item (Y/N)` - Hochwertiges Paket

## Nutzung

1. CSV/Excel-Datei in der Sidebar hochladen
2. Navigation über die Sidebar
3. Im Coaching Tool: Fahrer auswählen → Skript wird generiert
