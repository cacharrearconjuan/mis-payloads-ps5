import json
import urllib.request
import urllib.error
import urllib.parse
import hashlib
import os
import re
import base64
import zipfile
import shutil
from datetime import datetime, timezone

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
    },
    {
        "id": "onionHEN", 
        "author": "aydencharles", 
        "api": "https://api.github.com/repos/aydencharles/onionHEN/releases",
        "source": "https://github.com/aydencharles/onionHEN/releases",
        "category": "Sistema y Jailbreak",
        "description": "Homebrew Enabler (onionHEN) para PlayStation 5."
    },
    {
        "id": "elfldr", 
        "author": "ps5-payload-dev", 
        "api": "https://api.github.com/repos/ps5-payload-dev/elfldr/releases",
        "source": "https://github.com/ps5-payload-dev/elfldr/releases",
        "category": "Sistema y Jailbreak",
        "description": "Cargador de payloads para PS5 a través del puerto 9021."
    },
    {
        "id": "ps5-pkg-manager", 
        "author": "itsPLK", 
        "api": "https://api.github.com/repos/itsPLK/ps5-pkg-manager/releases",
        "source": "https://github.com/itsPLK/ps5-pkg-manager/releases",
        "category": "Utilidades y Herramientas",
        "description": "Gestor de paquetes (PKG) para PlayStation 5."
    }
]

EXEC_EXTENSIONS = ('.elf', '.bin', '.zip')
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg')
HOSTED_FOLDER = "hosted"

# Palabras a descartar para no confundir capturas o insignias con el icono del proyecto
EXCLUDE_IMAGE_KEYWORDS = (
    'shields.io', 'badge', 'workflows', 'actions/workflows', 'ko-fi',
    'buymeacoffee', 'paypal', 'discord', 'star-history', 'contrib.rocks',
    'sponsor', 'banner', 'screenshot', 'screen', 'preview', 'capture'
)

def construir_raw_url(repo_api_url, default_branch, file_path):
    """Construye la URL directa al archivo imagen tanto para GitHub como para Gitea."""
    file_path = file_path.lstrip('/')
    if "api.github.com/repos/" in repo_api_url:
        slug = repo_api_url.split("api.github.com/repos/")[1]
        return f"https://raw.githubusercontent.com/{slug}/{default_branch}/{file_path}"
    elif "/api/v1/repos/" in repo_api_url:
        base_host, slug = repo_api_url.split("/api/v1/repos/")
        return f"{base_host}/{slug}/raw/branch/{default_branch}/{file_path}"
    return ""

def buscar_icono_en_arbol(repo_api_url, default_branch, headers):
    """Busca archivos como assets/icon0.png, icon0.png, icon.png o logo.png en el árbol del repositorio."""
    tree_url = f"{repo_api_url}/git/trees/{default_branch}?recursive=1"
    try:
        req = urllib.request.Request(tree_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode())
            tree = data.get("tree", [])

            prioridad_1 = []  # icon0.png (estándar PS5)
            prioridad_2 = []  # icon.png / logo.png exactos
            prioridad_3 = []  # cualquier imagen que contenga 'icon' o 'logo'

            for item in tree:
                if item.get("type") != "blob":
                    continue
                path = item.get("path", "")
                path_lower = path.lower()
                filename = os.path.basename(path_lower)

                if not filename.endswith(IMAGE_EXTENSIONS):
                    continue
                if any(bad in path_lower for bad in EXCLUDE_IMAGE_KEYWORDS):
                    continue

                if filename in ("icon0.png", "icon0.jpg", "icon0.webp"):
                    prioridad_1.append(path)
                elif filename in ("icon.png", "logo.png", "icon.jpg", "logo.jpg", "icon.webp", "logo.webp"):
                    prioridad_2.append(path)
                elif "icon" in filename or "logo" in filename:
                    prioridad_3.append(path)

            for lista in (prioridad_1, prioridad_2, prioridad_3):
                if lista:
                    return construir_raw_url(repo_api_url, default_branch, lista[0])
    except Exception:
        pass
    return None

def extraer_logo_de_readme(repo_api_url, default_branch, headers):
    """Analiza el README.md del proyecto para extraer su logotipo principal."""
    readme_url = f"{repo_api_url}/readme"
    try:
        req = urllib.request.Request(readme_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode())
            contenido_b64 = data.get("content", "")
            if not contenido_b64:
                return None

            texto_readme = base64.b64decode(contenido_b64).decode('utf-8', errors='ignore')

            patrones = [
                r'<img[^>]+src=["\']([^"\']+)["\']',
                r'!\[[^\]]*\]\(([^)\s]+)'
            ]

            candidatos = []
            for patron in patrones:
                candidatos.extend(re.findall(patron, texto_readme, re.IGNORECASE))

            imagenes_validas = []
            for img_url in candidatos:
                img_url = img_url.strip()
                img_lower = img_url.lower()

                if any(palabra in img_lower for palabra in EXCLUDE_IMAGE_KEYWORDS):
                    continue

                ruta_limpia = img_lower.split('?')[0].split('#')[0]
                if not ruta_limpia.endswith(IMAGE_EXTENSIONS) and 'githubusercontent.com' not in img_lower:
                    continue

                # Convertir ruta relativa o blob de GitHub en URL Raw directa
                if img_url.startswith(('http://', 'https://')):
                    if 'github.com/' in img_url and '/blob/' in img_url:
                        img_url = img_url.replace('github.com/', 'raw.githubusercontent.com/').replace('/blob/', '/')
                    url_final = img_url
                else:
                    ruta_relativa = re.sub(r'^\./', '', img_url).lstrip('/')
                    url_final = construir_raw_url(repo_api_url, default_branch, ruta_relativa)

                if url_final:
                    imagenes_validas.append(url_final)

            # Priorizar si alguna imagen del README se llama 'icon' o 'logo'
            for url_img in imagenes_validas:
                if 'icon' in url_img.lower() or 'logo' in url_img.lower():
                    return url_img

            if imagenes_validas:
                return imagenes_validas[0]
    except Exception:
        pass
    return None

def obtener_icono_repositorio(app, headers):
    """Obtiene el icono del proyecto (árbol de archivos -> README -> avatar del repo/autor)."""
    if app.get("icon"):
        return app["icon"]

    repo_api_url = re.sub(r'/releases$', '', app['api'].rstrip('/'))
    default_branch = "main"
    avatar_fallback = ""

    # 1. Consultar metadatos del repositorio (rama principal y avatares)
    try:
        req = urllib.request.Request(repo_api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            repo_data = json.loads(res.read().decode())
            default_branch = repo_data.get("default_branch", "main")
            # En Gitea el repositorio puede tener su propio avatar_url
            avatar_fallback = repo_data.get("avatar_url") or (repo_data.get("owner") or {}).get("avatar_url", "")
    except Exception:
        pass

    # 2. Buscar archivo de icono en el repositorio (ej. assets/icon0.png)
    icono_arbol = buscar_icono_en_arbol(repo_api_url, default_branch, headers)
    if icono_arbol:
        return icono_arbol

    # 3. Buscar logotipo en el README.md
    icono_readme = extraer_logo_de_readme(repo_api_url, default_branch, headers)
    if icono_readme:
        return icono_readme

    # 4. Último recurso: avatar cuando el repositorio no tiene ninguna imagen (ej. elfldr)
    if avatar_fallback:
        return avatar_fallback
    if "github.com" in app.get("source", ""):
        return f"https://github.com/{app['author']}.png"

    return ""

def convertir_icono_a_base64(icon_url):
    """Descarga el icono y lo convierte a Data URI Base64 para el archivo icons.json."""
    if not icon_url:
        return ""
    if icon_url.startswith("data:image/"):
        return icon_url
    try:
        req = urllib.request.Request(icon_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as res:
            raw_bytes = res.read()
            content_type = res.headers.get_content_type()

            if not content_type or not content_type.startswith("image/"):
                url_lower = icon_url.lower().split('?')[0]
                if url_lower.endswith(('.jpg', '.jpeg')):
                    content_type = "image/jpeg"
                elif url_lower.endswith('.webp'):
                    content_type = "image/webp"
                elif url_lower.endswith('.gif'):
                    content_type = "image/gif"
                elif url_lower.endswith('.svg'):
                    content_type = "image/svg+xml"
                else:
                    content_type = "image/png"

            b64_str = base64.b64encode(raw_bytes).decode('utf-8')
            return f"data:{content_type};base64,{b64_str}"
    except Exception as e:
        print(f"  [!] No se pudo codificar en Base64 el icono {icon_url}: {e}")
        return icon_url

def es_version_valida(tag_name):
    return "alpha" not in tag_name.lower()

def extraer_ejecutables_validos(release):
    if release.get("draft", False):
        return []
    
    tag_name = release.get("tag_name", "")
    if not es_version_valida(tag_name):
        return []
        
    ejecutables = []
    for asset in release.get("assets", []):
        nombre = asset.get("name", "")
        nombre_lower = nombre.lower()

        if not nombre_lower.endswith(EXEC_EXTENSIONS): 
            continue
        if "install" in nombre_lower and "installer_" not in nombre_lower: 
            continue
        
        ejecutables.append({
            "nombre": nombre,
            "url": asset.get("browser_download_url", "")
        })
    return ejecutables

def obtener_datos_api(app):
    url = app['api']
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        token = os.environ.get('GITHUB_TOKEN')
        if token and "github.com" in url:
            headers['Authorization'] = f'Bearer {token}'

        latest_tag = None
        if "github.com" in url:
            try:
                url_latest = url.rstrip('/') + "/latest"
                req_latest = urllib.request.Request(url_latest, headers=headers)
                with urllib.request.urlopen(req_latest) as res_latest:
                    latest_data = json.loads(res_latest.read().decode())
                    latest_tag = latest_data.get("tag_name")
            except urllib.error.HTTPError:
                pass 

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            releases = json.loads(response.read().decode())
            
            if not isinstance(releases, list):
                releases = [releases]

            target_release = None
            ejecutables_finales = []

            if latest_tag:
                for r in releases:
                    if r.get("tag_name") == latest_tag:
                        exe = extraer_ejecutables_validos(r)
                        if exe:
                            target_release = r
                            ejecutables_finales = exe
                        break

            if not target_release:
                for r in releases:
                    if r.get("prerelease", False):
                        continue
                    exe = extraer_ejecutables_validos(r)
                    if exe:
                        target_release = r
                        ejecutables_finales = exe
                        break

            if not target_release:
                for r in releases:
                    exe = extraer_ejecutables_validos(r)
                    if exe:
                        target_release = r
                        ejecutables_finales = exe
                        break

            if not target_release:
                return None, None, None, None, None, None

            version = target_release.get("tag_name", "Desconocida")
            last_update = target_release.get("published_at", "2026-01-01T")[:10] 
            
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

            nombre_archivo = elegido["nombre"]
            url_descarga = elegido["url"]
            checksum = ""

            if nombre_archivo.lower().endswith('.zip'):
                print(f"  [+] ZIP detectado. Descargando y procesando en memoria...")
                os.makedirs(HOSTED_FOLDER, exist_ok=True)
                zip_path = "temp.zip"
                
                try:
                    req_zip = urllib.request.Request(url_descarga, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req_zip) as resp_zip, open(zip_path, 'wb') as out_file:
                        shutil.copyfileobj(resp_zip, out_file)
                        
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        elf_in_zip = next((f for f in zip_ref.namelist() if f.lower().endswith(('.elf', '.bin'))), None)
                        
                        if elf_in_zip:
                            nuevo_nombre = os.path.basename(elf_in_zip)
                            ruta_final = os.path.join(HOSTED_FOLDER, nuevo_nombre)
                            
                            with zip_ref.open(elf_in_zip) as source, open(ruta_final, 'wb') as target:
                                shutil.copyfileobj(source, target)
                                
                            nombre_archivo = nuevo_nombre
                            url_descarga = f"https://cacharrearconjuan.github.io/mis-payloads-ps5/{HOSTED_FOLDER}/{nuevo_nombre}"
                            
                            with open(ruta_final, 'rb') as f_elf:
                                checksum = hashlib.sha256(f_elf.read()).hexdigest()
                                
                    if os.path.exists(zip_path):
                        os.remove(zip_path)
                        
                except Exception as e:
                    print(f"  [!] Error crítico procesando el ZIP: {e}")
                    if os.path.exists(zip_path):
                        os.remove(zip_path)
            else:
                try:
                    req_file = urllib.request.Request(url_descarga, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req_file) as r_file:
                        checksum = hashlib.sha256(r_file.read()).hexdigest()
                except Exception as e:
                    print(f"  [!] Error calculando checksum estándar: {e}")

            icono_url = obtener_icono_repositorio(app, headers)
                    
            return version, nombre_archivo, url_descarga, last_update, checksum, icono_url
            
    except urllib.error.HTTPError as e:
        print(f"  [!] Error HTTP {e.code} consultando {url}: {e.reason}")
        return None, None, None, None, None, None
    except Exception as e:
        print(f"  [!] Error general consultando {url}: {e}")
        return None, None, None, None, None, None

def main():
    repo_data = []
    icons_catalog = {}

    for app in APPS:
        print(f"Procesando {app['id']}...")
        version, nombre_archivo, url_descarga, last_update, checksum, icono_url = obtener_datos_api(app)
        
        if version and url_descarga:
            icono_b64 = convertir_icono_a_base64(icono_url)
            if icono_b64:
                icons_catalog[app['id']] = icono_b64

            payload = {
                "name": app['id'],
                "filename": nombre_archivo,
                "url": url_descarga,
                "source": app['source'],
                "source_direct": url_descarga,
                "author": app.get('author', ''),
                "description": app.get('description', ''),
                "last_update": last_update,
                "version": version,
                "category": app.get('category', 'Utilidades y Herramientas'),
                "checksum": checksum,
                "icon": icono_url
            }
            
            if nombre_archivo.lower().endswith('.zip') and 'extract_file' in app:
                payload["extract_file"] = app['extract_file']

            repo_data.append(payload)
            print(f" -> OK: {version} ({nombre_archivo}) | Icono: {icono_url}")
        else:
            print(f" -> ERROR: No se encontró versión válida o falló la conexión.")

    # 1. Guardar payloads.json
    with open("payloads.json", "w", encoding="utf-8") as f:
        json.dump(repo_data, f, indent=4, ensure_ascii=False)

    # 2. Guardar payloads_v2.json
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    repo_v2 = {
        "last_updated": ahora,
        "payloads": repo_data
    }
    with open("payloads_v2.json", "w", encoding="utf-8") as f:
        json.dump(repo_v2, f, indent=4, ensure_ascii=False)

    # 3. Guardar icons.json (Catálogo separado de iconos para PS5 Payload Manager)
    with open("icons.json", "w", encoding="utf-8") as f:
        json.dump(icons_catalog, f, indent=4, ensure_ascii=False)

    print("\nArchivos 'payloads.json', 'payloads_v2.json' e 'icons.json' generados correctamente.")

if __name__ == "__main__":
    main()
