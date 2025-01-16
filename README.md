# Claude MCP Data Analysis Example

Dieses Repository demonstriert die Verwendung von Claude MCP für Data Analysis Projekte.

## Weitere MCP Ressourcen

- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers/tree/main) - Hier findest du alle verfügbaren MCP Server und ihre Implementierungen
- [MCP Filesystem Dokumentation](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) - Detaillierte Dokumentation zur Verwendung des MCP Filesystem Servers

Diese Ressourcen sind besonders hilfreich, wenn du:
- Mehr über die verschiedenen MCP Server-Typen lernen möchtest
- Die technischen Details des Filesystem-Servers verstehen willst
- Eigene MCP Server implementieren möchtest
- Nach fortgeschrittenen Konfigurationsoptionen suchst

## Projekt Setup

### Claude Desktop App Konfiguration

1. Öffne folgende Datei auf deinem Mac:
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

2. Füge folgende Konfiguration hinzu:
```json
{
  "mcp": {
    "servers": [
      {
        "type": "filesystem",
        "allowed_paths": [
          "/Users/[DeinUsername]/Data Science/Data Science Projekte/AI/claude_mcp_example"
        ]
      }
    ]
  }
}
```

## Projektstruktur

```
claude_mcp_example/
├── README.md
├── data/
│   └── example_data.csv
├── src/
│   ├── data_analyzer.py
│   └── example_analysis.ipynb
```

## Verwendung

1. Stelle sicher, dass deine Claude Desktop App läuft
2. Öffne die App und frage Claude, die Dateien zu analysieren:

```
"Kannst du bitte die Datei data_analyzer.py analysieren und verbessern?"
```

## Beispiel Workflows

1. Code Review und Verbesserungen:
   - Lass Claude den Code auf Best Practices prüfen
   - Bitte um Optimierungsvorschläge
   - Lass dir neue Features vorschlagen

2. Datenanalyse:
   - Lass Claude die Daten explorieren
   - Bitte um statistische Auswertungen
   - Lass dir Visualisierungen vorschlagen

## Fehlersuche

Bei Problemen:
1. Prüfe die Pfade in der `claude_desktop_config.json`
2. Stelle sicher, dass die Claude Desktop App läuft
3. Versuche die App neu zu starten

### Alternative MCP Server

Dieses Beispiel nutzt den Filesystem-Server, aber es gibt noch weitere MCP Server-Typen:

- **HTTP Server**: Für Web-basierte Interaktionen
- **WebSocket Server**: Für Echtzeit-Kommunikation
- **Custom Server**: Für spezialisierte Anwendungsfälle

Mehr Informationen zu den verschiedenen Server-Typen findest du im [MCP Servers Repository](https://github.com/modelcontextprotocol/servers/tree/main).

### Fortgeschrittene Filesystem-Konfiguration

Für fortgeschrittene Anwendungsfälle bietet der Filesystem-Server weitere Konfigurationsmöglichkeiten:

- Komplexe Pfadkonfigurationen
- Berechtigungssteuerung
- Ereignisprotokollierung

Details dazu findest du in der [Filesystem Server Dokumentation](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem).
