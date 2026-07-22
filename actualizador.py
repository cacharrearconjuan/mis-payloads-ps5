import json
import urllib.request
import hashlib

# Configuracion exacta simulando la base de datos de itsPLK
APPS = [
    {
        "name": "PS5 Payload Manager", 
        "author": "itsPLK", 
        "api": "https://api.github.com/repos/itsPLK/ps5-payload-manager/releases",
        "source": "https://github.com/itsPLK/ps5-payload-manager/releases",
        "category": "Utilities & Tools",
        "description": "A modern, web-based dashboard to easily manage, import, and automatically load payloads on your PS5."
    },
    {
        "name": "ShadowMountPlus", 
        "author": "drakmor", 
        "api": "https://api.github.com/repos/drakmor/ShadowMountPlus/releases",
        "source": "https://github.com/drakmor/ShadowMountPlus/releases",
        "category": "Utilities & Tools",
        "description": "A fully automated, background 'Auto-Mounter' payload for Jailbroken PlayStation 5 consoles.",
        "extract_file": "shadowmountplus.elf" # Fundamental para que extraiga el ZIP
    },
    {
        "name": "FTP Server", 
        "author": "ps5-payload-dev", 
        "api": "https://api.github.com/repos/ps5-payload-dev/ftpsrv/releases",
        "source": "https://github.com/ps5-payload-dev/ftpsrv/releases",
        "category": "Networking & Servers",
        "description": "A simple FTP server for the PS5."
    },
    {
        "name": "Kstuff Lite", 
        "author": "EchoStretch", 
        "api": "https://api.github.com/repos/EchoStretch/kstuff-lite/releases",
        "source": "https://github.com/EchoStretch/kstuff-lite/releases",
        "category": "System & Jailbreak",
        "description": "Lite version of kstuff."
    },
    {
        "name": "Elf Arsenal", 
        "author": "soniciso", 
        "api": "https://git.etawen.dev/api/v1/repos/soniciso/elf-arsenal/releases",
        "source": "https://git.etawen.dev/soniciso/elf-arsenal/releases",
        "category": "Utilities & Tools",
        "description": "Various ELF payloads packed together."
    },
    {
        "name": "Garlic Save Manager", 
        "author": "earthonion", 
        "api": "https://git.etawen.dev/api/v1/repos/earthonion/garlic-savemgr/releases",
        "source": "https://git.etawen.dev/earthonion/garlic-savemgr/releases",
        "category": "Utilities & Tools",
        "description": "PS5 save decrypt/encrypt/browse with embedded web UI."
    },
    {
        "name": "PS5 Game Compressor", 
        "author": "juma-sayeh", 
        "api": "https://api.github.com/repos/juma-sayeh/PS5-Game-Compressor/releases",
        "source": "https://github.com/juma-sayeh/PS5-Game-Compressor/releases",
        "category": "Utilities & Tools",
        "description": "Compress PS5 games easily."
    },
    {
        "name": "nanoDNS", 
        "author": "drakmor", 
        "api": "https://api.github.com/repos/drakmor/nanoDNS/releases",
        "source": "https://github.com/drakmor/nanoDNS/releases",
        "category": "Networking & Servers",
        "description": "A tiny, fast, and secure DNS server."
    }
]

# Añadimos .zip para que ShadowMountPlus funcione
EXEC_EXTENSIONS = ('.elf', '.bin', '.zip')

def obtener_datos_api(app):
    url = app['api']
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            releases = json.loads(response.read().decode())
            
            if not isinstance(releases, list):
                releases = [releases]

            for datos in releases:
                version = datos.get("tag_name", "Desconocida")
                
                # Extraemos la fecha real de la release (formato YYYY-MM-DD)
                last_update = datos.get("published_at", "2024-01-01T")[:10] 
                assets = datos.get("assets", [])

                ejecutables = []
                for asset in assets:
                    nombre = asset.get("name", "")
                    if nombre.lower().endswith(EXEC_EXTENSIONS):
                        ejecutables.append({
                            "nombre": nombre,
                            "url": asset.get("browser_download_url", "")
                        })
                
                if ejecutables:
                    elegido = None
                    
                    # Prioridad 1: PS5 explícito
                    for exe in ejecutables:
                        if "ps5" in exe["nombre"].lower():
                            elegido = exe
                            break
                            
                    # Prioridad 2: Genérico (sin PS4)
                    if not elegido:
                        for exe in ejecutables:
                            if "ps4" not in exe["nombre"].lower():
                                elegido = exe
                                break
                                
                    # Prioridad 3: El primero
                    if not elegido:
                        elegido = ejecutables[0]

                    # Calculamos el SHA256 real descargando el archivo (requerido por la app)
                    checksum = ""
                    try:
                        req_file = urllib.request.Request(elegido["url"], headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req_file) as r:
                            checksum = hashlib.sha256(r.read()).hexdigest()
                    except Exception as e:
                        print(f"  [!] Error calculando checksum: {e}")
                        checksum = "0000000000000000000000000000000000000000000000000000000000000000"
                            
                    return version, elegido["nombre"], elegido["url"], last_update, checksum
                    
            return None, None, None, None, None
    except Exception as e:
        print(f"Error consultando {url}: {e}")
        return None, None, None, None, None

def main():
    repo_data = []

    for app in APPS:
        print(f"Procesando {app['name']}...")
        version, nombre_archivo, url_descarga, last_update, checksum = obtener_datos_api(app)
        
        if version and url_descarga:
            # Construimos el objeto exacto que requiere el manager
            payload = {
                "name": app['name'],
                "filename": nombre_archivo,
                "url": url_descarga,
                "source": app['source'],
                "source_direct": url_descarga,
                "description": app.get('description', ''),
                "last_update": last_update,
                "version": version,
                "category": app.get('category', 'Utilities & Tools'),
                "checksum": checksum
            }
            
            # Solo añadimos extract_file si la aplicación lo requiere (ej. ZIPs)
            if 'extract_file' in app:
                payload["extract_file"] = app['extract_file']

            repo_data.append(payload)
            print(f" -> OK: {version} ({nombre_archivo}) | Checksum: {checksum[:8]}...")
        else:
            print(f" -> ERROR: No se encontró ningún archivo válido.")

    with open("repo.json", "w", encoding="utf-8") as f:
        json.dump(repo_data, f, indent=4)
    print("\nEl archivo repo.json se ha generado con la estructura completa.")

if __name__ == "__main__":
    main()
