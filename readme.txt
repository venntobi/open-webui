Die wichtigsten Konfigurationen zum Bludau:

Bludau Bilder: (Bennung der Bilder beachten)
    favicon.png: Hauptlogo.
        Größe wird bearbeitet in: src\lib\components\chat\Placeholder.svelte, Zeile: 128.
        Verzeichnisse:
            static
            static\static
            backend\open_webui\static
            backend\open_webui\static\swagger-ui

    logo.png: wie favicon.png, Größe: 500*500.
        Verzeichnisse:
            backend\open_webui\static
            backend\open_webui\utils

    apple-touch-icon.png: wie favicon.png, Größe: 180*180.
        Verzeichnis: static\favicon

    favicon-96x96.png: wie favicon.png, Größe: 96*96.
        Verzeichnis: static\favicon

    web-app-manifest-192x192.png: wie favicon.png, Größe: 192*192.
        Verzeichnis: static\favicon

    web-app-manifest-512x512.png: wie favicon.png, Größe: 512*512. 
        Verzeichnis: static\favicon

    favicon.ico: wie favicon.png, Größe: 32*32.
        Verzeichnis: static\favicon

    splash.png: Logo beim Seitenaktualisierung.
        Größe wird bearbeitet in: src\app.html, Zeile: 89,90.
        Verzeichnisse:
            backend\open_webui\static
            static\static

    splash-dark.png: Logo beim Seitenaktualisierung im Dark Modus.
        Größe wird bearbeitet in: src\app.html, Zeile: 89,90.
        Verzeichnis: static\static

    custom-background.png: Hintergrundbild.
        Opazität bearbeiten in: src\lib\config.ts
        Verzeichnis: static\static

Bludau Tabs:
    Ein Variable named WEB_NAME mit Wert Bludau wird angelegt in Verzeichnis: src\lib\stores\index.ts, Zeile: 11.
    Das Wort Bludau wird angelegt in Verzeichnis: src\app.html, Zeile: 72.

Dark Modus wird als Standardmodus gesetzt in in Verzeichnis: src\lib\components\chat\Settings\General.svelte, Zeile: 18, 79.
