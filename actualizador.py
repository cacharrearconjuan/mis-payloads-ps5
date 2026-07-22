import json
import urllib.request
import hashlib

# Configuración con los IDs cortos exactos que espera el manager oficial
APPS = [
    {
        "id": "pldmgr", 
        "author": "itsPLK", 
        "api": "https://api.github.com/repos/itsPLK/ps5-payload-manager/releases",
        "source": "https://github.com/itsPLK/ps5-payload-manager/releases",
        "category": "Utilities & Tools",
        "description": "A modern, web-based dashboard to easily manage, import, and automatically load payloads on your PS5."
    },
    {
        "id": "ShadowMountPlus", 
        "author": "drakmor", 
        "api": "https://api.github.com/repos/drakmor/ShadowMountPlus/releases",
        "source": "https://github.com/drakmor/ShadowMountPlus/releases",
        "category": "Utilities & Tools",
        "description": "A fully automated, background 'Auto-Mounter' payload for Jailbroken PlayStation 5 consoles.",
        "extract_file": "shadowmountplus.elf"
    },
    {
        "id": "ftpsrv", 
        "author": "ps5-payload-dev", 
        "api": "https://api.github.com/repos/ps5-payload-dev/ftpsrv/releases",
        "source": "https://github.com/ps5-payload-dev/ftpsrv/releases",
        "category": "Networking & Servers",
        "description": "A simple FTP server for the PS5."
    },
    {
        "id": "kstuff-lite", 
        "author": "EchoStretch", 
        "api": "https://api.github.com/repos/EchoStretch/kstuff-lite/releases",
        "source": "https://github.com/EchoStretch/kstuff-lite/releases",
        "category": "System & Jailbreak",
        "description": "Lite version of kstuff."
    },
    {
        "id": "elf-arsenal", 
        "author": "soniciso", 
        "api": "https://git.etawen.dev/api/v1/repos/soniciso/elf-arsenal/releases",
        "source": "https://git.etawen.dev/soniciso/elf-arsenal/releases",
        "category": "Utilities & Tools",
        "description": "Various ELF payloads packed together."
    },
    {
        "id": "garlic-savemgr", 
        "author": "earthonion", 
        "api": "https://git.etawen.dev/api/v1/repos/earthonion/garlic-savemgr/releases",
        "source": "https://git.etawen.dev/earthonion/garlic-savemgr/releases",
        "category": "Utilities & Tools",
        "description": "PS5 save decrypt/encrypt/browse with embedded web UI."
    },
    {
        "id": "game-compressor", 
        "author": "juma-sayeh", 
        "api": "https://api.github.com/repos/juma-sayeh/PS5-Game-Compressor/releases",
        "source": "https://github.com/juma-sayeh/PS5-Game-Compressor/releases",
        "category": "Utilities & Tools",
        "description": "Compress PS5 games easily."
    },
    {
        "id": "nanoDNS", 
        "author": "drakmor", 
        "api": "https://api.github.com/repos/drakmor/nanoDNS/releases",
        "source": "https://github.com/drakmor/nanoDNS/releases",
        "category": "Networking & Servers",
        "description": "A tiny, fast, and secure DNS server."
    }
]

EXEC_EXTENSIONS = ('.elf', '.bin', '.zip')

def es_version_valida(tag_name):
    """ Filtra versiones alpha para quedarse solo con Beta o Estables """
    tag_lower = tag_name.lower()
    if "alpha" in tag_lower:
        return False
    return True

def obtener_datos_api(app):
    url = app['api']
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            releases = json.loads(response.read().decode())
            
            if not isinstance(releases, list):
                releases = [releases]

            for datos in releases:
                # Omitir borradores
                if datos.get("draft", False):
                    continue

                version = datos.get("tag_name", "Desconocida")
                
                # OMITIR ALPHAS: Si la versión contiene 'alpha', pasa a la siguiente release
                if not es_version_valida(version):
                    print(f"  [-] Omitiendo versión alpha: {version}")
                    continue

                last_update = datos.get("published_at", "2026-01-01T")[:10] 
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
                    
                    # 1. Prioridad PS5
                    for exe in ejecutables:
                        if "ps5" in exe["nombre"].lower():
                            elegido = exe
                            break
                            
                    # 2. Prioridad No-PS4
                    if not elegido:
                        for exe in ejecutables:
                            if "ps4" not in exe["nombre"].lower():
                                elegido = exe
                                break
                                
                    # 3. Primer ejecutable disponible
                    if not elegido:
                        elegido = ejecutables[0]

                    # Calcular Checksum SHA-256
                    checksum = ""
                    try:
                        req_file = urllib.request.Request(elegido["url"], headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req_file) as r:
                            checksum = hashlib.sha256(r.read()).hexdigest()
                    except Exception as e:
                        print(f"  [!] Error calculando checksum: {e}")
                        checksum = ""
                            
                    return version, elegido["nombre"], elegido["url"], last_update, checksum
                    
            return None, None, None, None, None
    except Exception as e:
        print(f"Error consultando {url}: {e}")
        return None, None, None, None, None

def main():
    repo_data = []

    for app in APPS:
        print(f"Procesando {app['id']}...")
        version, nombre_archivo, url_descarga, last_update, checksum = obtener_datos_api(app)
        
        if version and url_descarga:
            payload = {
                "name": app['id'],  # Nombre corto / ID nativo
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
            
            if 'extract_file' in app:
                payload["extract_file"] = app['extract_file']

            repo_data.append(payload)
            print(f" -> OK: {version} ({nombre_archivo})")
        else:
            print(f" -> ERROR: No se encontró versión válida (Beta/Estable).")

    with open("repo.json", "w", encoding="utf-8") as f:
        json.dump(repo_data, f, indent=4)
    print("\nEl archivo repo.json ha sido generado correctamente.")

if __name__ == "__main__":
    main()
