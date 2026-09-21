import json
import urllib.request
import urllib.error
import hashlib
import os
import zipfile
import shutil

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
        "description": "Un payload de 'Auto-Montaje' en segundo plano y totalmente automatizado para consolas PlayStation 5 con Jailbreak."
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
    },
    {
        "id": "Spectrum-Library", 
        "author": "Phoenixx1202", 
        "api": "https://api.github.com/repos/Phoenixx1202/Spectrum-Library/releases",
        "source": "https://github.com/Phoenixx1202/Spectrum-Library/releases",
        "category": "Utilidades y Herramientas",
        "description": "Librería y utilidades Spectrum para PS5."
    },
    {
        "id": "Common-FPS-for-PS5", 
        "author": "porhe911", 
        "api": "https://api.github.com/repos/porhe911/Common-FPS-for-PS5/releases",
        "source": "https://github.com/porhe911/Common-FPS-for-PS5/releases",
        "category": "Utilidades y Herramientas",
        "description": "Parches y utilidades de desbloqueo de tasa de frames (FPS) para PS5."
    }
]

EXEC_EXTENSIONS = ('.elf', '.bin', '.zip')
HOSTED_FOLDER = "hosted"

def obtener_datos_api(app):
    url = app['api']
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        token = os.environ.get('GITHUB_TOKEN')
        if token and "github.com" in url:
            headers['Authorization'] = f'Bearer {token}'

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            releases = json.loads(response.read().decode())
            
            if not isinstance(releases, list):
                releases = [releases]

            for r in releases:
                if r.get("draft", False):
                    continue
                
                version = r.get("tag_name", "Desconocida")
                if "alpha" in version.lower():
                    continue

                ejecutables_finales = []
                for asset in r.get("assets", []):
                    nombre = asset.get("name", "")
                    nombre_lower = nombre.lower()

                    if not nombre_lower.endswith(EXEC_EXTENSIONS): 
                        continue
                    if "install" in nombre_lower and "installer_" not in nombre_lower: 
                        continue
                    
                    ejecutables_finales.append({
                        "nombre": nombre,
                        "url": asset.get("browser_download_url", "")
                    })
                
                if ejecutables_finales:
                    elegido = None
                    for exe in ejecutables_finales:
                        if "ps5" in exe["nombre"].lower():
                            elegido = exe
                            break
                    if not elegido:
                        for exe in ejecutables_finales:
                            if "ps4" not in exe["nombre"].lower():
                                elegido = exe
                                break
                    if not elegido:
                        elegido = ejecutables_finales[0]

                    last_update = r.get("published_at", "2026-01-01T")[:10] 
                    nombre_archivo = elegido["nombre"]
                    url_descarga = elegido["url"]
                    checksum = ""

                    # LOGICA DE EXTRACCION DE ZIP
                    if nombre_archivo.lower().endswith('.zip'):
                        print(f"  [+] Detectado ZIP. Descargando y extrayendo {nombre_archivo}...")
                        os.makedirs(HOSTED_FOLDER, exist_ok=True)
                        zip_path = "temp.zip"
                        
                        try:
                            req_zip = urllib.request.Request(url_descarga, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(req_zip) as resp_zip, open(zip_path, 'wb') as out_file:
                                shutil.copyfileobj(resp_zip, out_file)
                                
                            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                                elf_in_zip = next((f for f in zip_ref.namelist() if f.lower().endswith(('.elf', '.bin'))), None)
                                
                                if elf_in_zip:
                                    zip_ref.extract(elf_in_zip, HOSTED_FOLDER)
                                    # Limpiar la ruta por si estaba dentro de una subcarpeta
                                    ruta_extraida = os.path.join(HOSTED_FOLDER, elf_in_zip)
                                    nuevo_nombre = os.path.basename(elf_in_zip)
                                    ruta_final = os.path.join(HOSTED_FOLDER, nuevo_nombre)
                                    
                                    if ruta_extraida != ruta_final:
                                        os.rename(ruta_extraida, ruta_final)
                                        # Eliminar directorios vacios dejados por el ZIP
                                        dir_to_clean = os.path.dirname(ruta_extraida)
                                        if dir_to_clean != HOSTED_FOLDER:
                                            shutil.rmtree(dir_to_clean, ignore_errors=True)
                                            
                                    # Reasignar variables para el JSON apuntando a tu repositorio
                                    nombre_archivo = nuevo_nombre
                                    url_descarga = f"https://cacharrearconjuan.github.io/mis-payloads-ps5/{HOSTED_FOLDER}/{nuevo_nombre}"
                                    
                                    # Calcular checksum del ELF extraído, no del ZIP
                                    with open(ruta_final, 'rb') as f_elf:
                                        checksum = hashlib.sha256(f_elf.read()).hexdigest()
                                        
                                    print(f"  [+] Extraído con éxito: {nuevo_nombre}")
                            
                            os.remove(zip_path) # Borrar el ZIP temporal
                            
                        except Exception as e:
                            print(f"  [!] Error procesando el ZIP: {e}")
                            if os.path.exists(zip_path):
                                os.remove(zip_path)
                    else:
                        # Si es un .elf normal, calculamos checksum directamente de internet
                        try:
                            req_file = urllib.request.Request(url_descarga, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(req_file) as r_file:
                                checksum = hashlib.sha256(r_file.read()).hexdigest()
                        except Exception as e:
                            print(f"  [!] Error calculando checksum: {e}")
                            
                    return version, nombre_archivo, url_descarga, last_update, checksum
                    
            return None, None, None, None, None
            
    except urllib.error.HTTPError as e:
        print(f"  [!] Error HTTP {e.code} consultando {url}: {e.reason}")
        return None, None, None, None, None
    except Exception as e:
        print(f"  [!] Error general consultando {url}: {e}")
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
            repo_data.append(payload)
            print(f" -> OK: {version} ({nombre_archivo})")
        else:
            print(f" -> ERROR: No se encontró versión válida.")

    with open("payloads.json", "w", encoding="utf-8") as f:
        json.dump(repo_data, f, indent=4, ensure_ascii=False)
    print("\nArchivo 'payloads.json' generado correctamente.")

if __name__ == "__main__":
    main()
