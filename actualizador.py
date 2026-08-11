import json
import urllib.request
import hashlib

APPS = [
    {
        "id": "pldmgr", 
        "author": "itsPLK", 
        "api": "https://api.github.com/repos/itsPLK/ps5-payload-manager/releases",
        "source": "https://github.com/itsPLK/ps5-payload-manager/releases",
        "category": "Utilidades y Herramientas",
        "description": "Un panel moderno basado en web para administrar, importar y cargar automáticamente payloads en tu PS5."
    },
    {
        "id": "ShadowMountPlus", 
        "author": "drakmor", 
        "api": "https://api.github.com/repos/drakmor/ShadowMountPlus/releases",
        "source": "https://github.com/drakmor/ShadowMountPlus/releases",
        "category": "Utilidades y Herramientas",
        "description": "Un payload de 'Auto-Montaje' en segundo plano y totalmente automatizado para consolas PlayStation 5 con Jailbreak.",
        "extract_file": "shadowmountplus.elf"
    },
    {
        "id": "ftpsrv", 
        "author": "ps5-payload-dev", 
        "api": "https://api.github.com/repos/ps5-payload-dev/ftpsrv/releases",
        "source": "https://github.com/ps5-payload-dev/ftpsrv/releases",
        "category": "Redes y Servidores",
        "description": "Un servidor FTP sencillo para la PS5."
    },
    {
        "id": "kstuff-lite", 
        "author": "EchoStretch", 
        "api": "https://api.github.com/repos/EchoStretch/kstuff-lite/releases",
        "source": "https://github.com/EchoStretch/kstuff-lite/releases",
        "category": "Sistema y Jailbreak",
        "description": "Versión ligera (Lite) de kstuff."
    },
    {
        "id": "elf-arsenal", 
        "author": "soniciso", 
        "api": "https://git.etawen.dev/api/v1/repos/soniciso/elf-arsenal/releases",
        "source": "https://git.etawen.dev/soniciso/elf-arsenal/releases",
        "category": "Utilidades y Herramientas",
        "description": "Varios payloads ELF empaquetados juntos."
    },
    {
        "id": "garlic-savemgr", 
        "author": "earthonion", 
        "api": "https://git.etawen.dev/api/v1/repos/earthonion/garlic-savemgr/releases",
        "source": "https://git.etawen.dev/earthonion/garlic-savemgr/releases",
        "category": "Utilidades y Herramientas",
        "description": "Descifrado/cifrado/exploración de partidas guardadas de PS5 con interfaz web integrada."
    },
    {
        "id": "Lapy-JB-Daemon", 
        "author": "itsPLK", 
        "api": "https://api.github.com/repos/itsPLK/PS5-Lapy-JB-Daemon/releases",
        "source": "https://github.com/itsPLK/PS5-Lapy-JB-Daemon/releases",
        "category": "Sistema y Jailbreak",
        "description": "Demonio de jailbreak homebrew independiente para PS5. Imita la API de jailbreak bajo demanda de etaHEN."
    },
    {
        "id": "game-compressor", 
        "author": "juma-sayeh", 
        "api": "https://api.github.com/repos/juma-sayeh/PS5-Game-Compressor/releases",
        "source": "https://github.com/juma-sayeh/PS5-Game-Compressor/releases",
        "category": "Utilidades y Herramientas",
        "description": "Comprime juegos de PS5 fácilmente."
    },
    {
        "id": "nanoDNS", 
        "author": "drakmor", 
        "api": "https://api.github.com/repos/drakmor/nanoDNS/releases",
        "source": "https://github.com/drakmor/nanoDNS/releases",
        "category": "Redes y Servidores",
        "description": "Un servidor DNS diminuto, rápido y seguro."
    },
    {
        "id": "PS5-AutoupdaterPM", 
        "author": "cacharrearconjuan", 
        "api": "https://api.github.com/repos/cacharrearconjuan/PS5-AutoupdaterPM/releases",
        "source": "https://github.com/cacharrearconjuan/PS5-AutoupdaterPM/releases",
        "category": "Utilidades y Herramientas",
        "description": "Payload para la descarga y actualización automática del Payload Manager en PS5."
    },
    {
        "id": "pegasus-dl", 
        "author": "pegasus-ps5", 
        "api": "https://api.github.com/repos/pegasus-ps5/pegasus-dl/releases",
        "source": "https://github.com/pegasus-ps5/pegasus-dl/releases",
        "category": "Utilidades y Herramientas",
        "description": "Herramienta de descarga pegasus-dl para PS5."
    },
    {
        "id": "ps5-webkit-autoloader", 
        "author": "itsPLK", 
        "api": "https://api.github.com/repos/itsPLK/ps5-webkit-autoloader/releases",
        "source": "https://github.com/itsPLK/ps5-webkit-autoloader/releases",
        "category": "Sistema y Jailbreak",
        "description": "Cargador automático para PS5 basado en el exploit WebKit."
    }
]

EXEC_EXTENSIONS = ('.elf', '.bin', '.zip')

def es_version_valida(tag_name):
    """ Filtra únicamente versiones Alpha. Permite versiones Beta y Estables. """
    return "alpha" not in tag_name.lower()

def obtener_datos_api(app):
    url = app['api']
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            releases = json.loads(response.read().decode())
            
            if not isinstance(releases, list):
                releases = [releases]

            for datos in releases:
                if datos.get("draft", False):
                    continue

                version = datos.get("tag_name", "Desconocida")
                if not es_version_valida(version):
                    continue

                last_update = datos.get("published_at", "2026-01-01T")[:10] 
                assets = datos.get("assets", [])

                ejecutables = []
                for asset in assets:
                    nombre = asset.get("name", "")
                    if nombre.lower().endswith(EXEC_EXTENSIONS):
                        # OMITIR los archivos que contengan "install" en el nombre
                        if "install" in nombre.lower():
                            continue
                            
                        ejecutables.append({
                            "nombre": nombre,
                            "url": asset.get("browser_download_url", "")
                        })
                
                if ejecutables:
                    elegido = None
                    for exe in ejecutables:
                        if "ps5" in exe["nombre"].lower():
                            elegido = exe
                            break
                    if not elegido:
                        for exe in ejecutables:
                            if "ps4" not in exe["nombre"].lower():
                                elegido = exe
                                break
                    if not elegido:
                        elegido = ejecutables[0]

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
                "name": app['id'],
                "filename": nombre_archivo,
                "url": url_descarga,
                "source": app['source'],
                "source_direct": url_descarga,
                "description": app.get('description', ''),
                "last_update": last_update,
                "version": version,
                "category": app.get('category', 'Utilidades y Herramientas'),
                "checksum": checksum
            }
            
            if nombre_archivo.lower().endswith('.zip') and 'extract_file' in app:
                payload["extract_file"] = app['extract_file']

            repo_data.append(payload)
            print(f" -> OK: {version} ({nombre_archivo})")
        else:
            print(f" -> ERROR: No se encontró versión válida.")

    with open("payloads.json", "w", encoding="utf-8") as f:
        json.dump(repo_data, f, indent=4, ensure_ascii=False)
    print("\nArchivo 'payloads.json' generado correctamente.")

if __name__ == "__main__":
    main()
    
