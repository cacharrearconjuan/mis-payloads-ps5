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
import io
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

# --- Formato de catálogo que entiende PS5 Payload Manager (ver CUSTOM_REPOSITORIES.md) ---
NOMBRE_REPO = "Cacharrear con Juan"
BASE_URL = "https://cacharrearconjuan.github.io/mis-payloads-ps5"
# Límites del Payload Manager: data URI PNG/JPEG/SVG, máx. 12.288 caracteres, sin WebP ni URLs
MAX_ICON_LEN = 12000

EXEC_EXTENSIONS = ('.elf', '.bin', '.zip')
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg')
HOSTED_FOLDER = "hosted"

# Palabras que delatan que una imagen NO es el icono (badges, capturas, donaciones...)
EXCLUDE_IMAGE_KEYWORDS = (
    'shields.io', 'badge', 'workflows', 'ko-fi', 'buymeacoffee', 'paypal', 'discord',
    'star-history', 'contrib.rocks', 'sponsor', 'banner', 'screenshot', 'screen',
    'preview', 'capture', 'demo', 'donat', 'alipay', 'wechat', 'flag-', 'favicon',
    'node_modules', 'mock', 'emoji', 'sprite'
)
# Carpetas habituales de iconos además de la raíz (el icono de un subproyecto no vale)
CARPETAS_ICONO = ('assets', 'assets-app', 'asset', 'images', 'image', 'img', 'icons', 'icon',
                  'res', 'resources', 'media', 'logo', 'art', 'sce_sys', '.github', 'docs')

def _api_json(url, headers, timeout=15):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode())

def construir_raw_url(repo_api_url, default_branch, file_path):
    file_path = urllib.parse.quote(file_path.lstrip('/'))
    if "api.github.com/repos/" in repo_api_url:
        slug_repo = repo_api_url.split("api.github.com/repos/")[1]
        return f"https://raw.githubusercontent.com/{slug_repo}/{default_branch}/{file_path}"
    elif "/api/v1/repos/" in repo_api_url:  # Gitea / Forgejo
        base_host, slug_repo = repo_api_url.split("/api/v1/repos/")
        return f"{base_host}/{slug_repo}/raw/branch/{default_branch}/{file_path}"
    return ""

def _prioridad_icono(path):
    """0 = icon0 (estándar PS5), 1 = icon/logo, 2 = contiene icon/logo; None = no es icono."""
    path_lower = path.lower()
    nombre, ext = os.path.splitext(os.path.basename(path_lower))
    if ext not in IMAGE_EXTENSIONS or any(k in path_lower for k in EXCLUDE_IMAGE_KEYWORDS):
        return None
    if nombre == "icon0":
        return 0
    if nombre in ("icon", "logo", "app_icon", "appicon", "app-icon"):
        return 1
    if "icon" in nombre or "logo" in nombre:
        return 2
    return None

def listar_arbol(repo_api_url, default_branch, headers):
    """Rutas de todos los ficheros del repo (GitHub o Gitea)."""
    ref = default_branch
    if "/api/v1/repos/" in repo_api_url:
        # Gitea pide el SHA del commit, no el nombre de la rama
        rama = _api_json(f"{repo_api_url}/branches/{urllib.parse.quote(default_branch)}", headers)
        ref = rama["commit"]["id"]
        url = f"{repo_api_url}/git/trees/{ref}?recursive=true&per_page=10000"
    else:
        url = f"{repo_api_url}/git/trees/{urllib.parse.quote(ref)}?recursive=1"
    data = _api_json(url, headers)
    return [i["path"] for i in data.get("tree", []) if i.get("type") == "blob"]

def iconos_del_arbol(rutas):
    """Iconos del repo, mejor primero. Solo raíz o una carpeta típica (assets/, img/...):
    así no se cuela el icono de un subproyecto (p. ej. elf-arsenal/ftpsrv-src/assets/icon0.png)."""
    candidatos = []
    for path in rutas:
        prio = _prioridad_icono(path)
        if prio is None:
            continue
        carpetas = path.lower().split("/")[:-1]
        if len(carpetas) > 1 or (carpetas and carpetas[0] not in CARPETAS_ICONO):
            continue
        candidatos.append((prio, len(carpetas), path))
    return [p for _, _, p in sorted(candidatos)]

def imagenes_del_readme(texto, repo_api_url, default_branch):
    """Imágenes del README: primero las que se llaman icon/logo, luego el resto (máx. 3).
    Luego se exige que sean casi cuadradas, así una captura o un banner no cuela."""
    etiquetas = re.findall(r'<img[^>]*>', texto, re.I) + re.findall(r'!\[[^\]]*\]\([^)\s]+[^)]*\)', texto)
    con_nombre, resto = [], []
    for tag in etiquetas:
        m = re.search(r'src=["\']([^"\']+)', tag, re.I) or re.search(r'\]\(([^)\s]+)', tag)
        if not m:
            continue
        url = m.group(1).strip()
        url_lower = url.lower()
        if any(k in url_lower for k in EXCLUDE_IMAGE_KEYWORDS) or url_lower.startswith("data:"):
            continue
        if url.startswith(("http://", "https://")):
            if "github.com/" in url and "/blob/" in url:
                url = url.replace("github.com/", "raw.githubusercontent.com/").replace("/blob/", "/")
        else:
            url = construir_raw_url(repo_api_url, default_branch, re.sub(r'^\./', '', url))
        if not url:
            continue
        (con_nombre if re.search(r'icon|logo', tag, re.I) else resto).append(url)
    vistos, salida = set(), []
    for u in con_nombre + resto[:3]:
        if u not in vistos:
            vistos.add(u); salida.append(u)
    return salida

def candidatos_icono(app, headers, release=None):
    """Lista ordenada de (url, exigir_cuadrado). Orden:
       0) "icon" manual en APPS  1) imagen icon0/icon/logo subida a la release
       2) icono en el propio repo  3) logo del README  4) avatar del autor/organización."""
    if app.get("icon"):
        return [(app["icon"], False)]
    salida = []

    for asset in (release or {}).get("assets", []):
        if _prioridad_icono(asset.get("name", "")) is not None:
            salida.append((asset.get("browser_download_url", ""), True))

    repo_api_url = re.sub(r'/releases$', '', app['api'].rstrip('/'))
    default_branch, avatar = "main", ""
    try:
        repo_data = _api_json(repo_api_url, headers)
        default_branch = repo_data.get("default_branch") or "main"
        avatar = (repo_data.get("owner") or {}).get("avatar_url") or repo_data.get("avatar_url") or ""
    except Exception as e:
        print(f"    (sin datos del repo: {e})")

    rutas = []
    try:
        rutas = listar_arbol(repo_api_url, default_branch, headers)
        salida += [(construir_raw_url(repo_api_url, default_branch, p), True) for p in iconos_del_arbol(rutas)]
    except Exception as e:
        print(f"    (no se pudo listar el repo: {e})")

    readme = next((p for p in rutas if "/" not in p and p.lower().startswith("readme")
                   and p.lower().endswith((".md", ".markdown"))), None)
    if readme:
        try:
            texto = _leer(construir_raw_url(repo_api_url, default_branch, readme))[0].decode("utf-8", "ignore")
            salida += [(u, True) for u in imagenes_del_readme(texto, repo_api_url, default_branch)]
        except Exception as e:
            print(f"    (no se pudo leer el README: {e})")

    # Lo de siempre como último recurso: avatar (o identicon generado por GitHub/Gitea)
    if avatar:
        salida.append((avatar, False))
    if "github.com" in app.get("source", ""):
        salida.append((f"https://github.com/{app['author']}.png", False))
    return salida

def _leer(url_o_ruta, timeout=20):
    if url_o_ruta.startswith(("http://", "https://")):
        req = urllib.request.Request(url_o_ruta, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return res.read(), res.headers.get("Content-Type", "")
    with open(url_o_ruta, "rb") as f:
        return f.read(), ""

def _pillow():
    """Pillow hace falta para redimensionar PNG/JPEG/WebP. Si no está, se instala sola."""
    try:
        from PIL import Image, ImageOps
    except ImportError:
        import subprocess, sys
        print("    Pillow no está instalado: instalándolo...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pillow"])
        from PIL import Image, ImageOps
    return Image, ImageOps

def _es_casi_cuadrada(ancho, alto):
    return ancho > 0 and alto > 0 and 0.75 <= ancho / alto <= 1.33

def convertir_icono_a_data_uri(icon_url, exigir_cuadrado=False):
    """Descarga una imagen y la deja como data URI PNG/JPEG/SVG <= MAX_ICON_LEN (128 px máx)."""
    if not icon_url:
        return ""
    raw, mime = (base64.b64decode(icon_url.split(",", 1)[1]), icon_url.split(";")[0][5:]) \
        if icon_url.startswith("data:image/") else _leer(icon_url)

    # SVG: se deja tal cual si cabe (no se rasteriza)
    cabeza = raw.lstrip()[:300]
    if "svg" in mime.lower() or cabeza.startswith(b"<svg") or (cabeza.startswith(b"<?xml") and b"<svg" in cabeza):
        texto = re.sub(r"\s+", " ", re.sub(r"<!--.*?-->", "", raw.decode("utf-8", "ignore"), flags=re.S)).strip()
        vb = re.search(r'viewBox=["\'][\d.\-]+[\s,]+[\d.\-]+[\s,]+([\d.]+)[\s,]+([\d.]+)', texto)
        if exigir_cuadrado and vb and not _es_casi_cuadrada(float(vb.group(1)), float(vb.group(2))):
            raise ValueError("SVG no cuadrado (banner/captura)")
        uri = "data:image/svg+xml;base64," + base64.b64encode(texto.encode()).decode()
        if len(uri) <= MAX_ICON_LEN:
            return uri
        raise ValueError("SVG demasiado grande")

    Image, ImageOps = _pillow()
    img = Image.open(io.BytesIO(raw))
    img.seek(0)  # GIF/WebP animados: primer fotograma
    if exigir_cuadrado and not _es_casi_cuadrada(*img.size):
        raise ValueError(f"no es cuadrada {img.size} (banner/captura)")
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    img = img.convert("RGBA")
    transparente = img.getchannel("A").getextrema()[0] < 250
    if not transparente:
        img = img.convert("RGB")

    for lado in (128, 96, 80, 64, 48):
        peque = img.copy()
        peque.thumbnail((lado, lado), Image.Resampling.LANCZOS)
        intentos = [("PNG", peque, {})]
        intentos += [("PNG", peque.quantize(colors=c, method=Image.Quantize.FASTOCTREE), {}) for c in (128, 64, 32)]
        if not transparente:
            intentos += [("JPEG", peque, {"quality": q}) for q in (85, 75)]
        for formato, im, extra in intentos:
            buf = io.BytesIO()
            im.save(buf, format=formato, optimize=True, **extra)
            uri = f"data:image/{formato.lower()};base64," + base64.b64encode(buf.getvalue()).decode()
            if len(uri) <= MAX_ICON_LEN:
                return uri
    raise ValueError("no cabe en el límite de tamaño")

def slug(texto):
    """Mismo algoritmo que slot_slug() del Payload Manager, para que el id no cambie."""
    out, ultimo_guion = [], True
    for c in texto:
        if c.isascii() and c.isalnum():
            out.append(c.lower()); ultimo_guion = False
        elif c in "._" and out and out[-1] != ".":
            out.append(c); ultimo_guion = False
        elif not ultimo_guion:
            out.append("-"); ultimo_guion = True
    return "".join(out).rstrip("-")

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
                    if os.path.exists(zip_path):
                        os.remove(zip_path)
            else:
                try:
                    req_file = urllib.request.Request(url_descarga, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req_file) as r_file:
                        checksum = hashlib.sha256(r_file.read()).hexdigest()
                except Exception as e:
                    pass

            icono_urls = candidatos_icono(app, headers, target_release)
            return version, nombre_archivo, url_descarga, last_update, checksum, icono_urls
    except Exception:
        return None, None, None, None, None, None

def main():
    repo_data = []
    icons_catalog = {}

    for app in APPS:
        print(f"Procesando {app['id']}...")
        version, nombre_archivo, url_descarga, last_update, checksum, icono_urls = obtener_datos_api(app)

        if version and url_descarga:
            # Icono sacado del propio repositorio del payload; si no hay, el avatar de siempre.
            # Si todo falla, no se pone icon_key y el Payload Manager genera el suyo.
            icono = ""
            for cand, cuadrado in icono_urls:
                if not cand:
                    continue
                try:
                    icono = convertir_icono_a_data_uri(cand, exigir_cuadrado=cuadrado)
                    print(f"    icono: {cand}")
                    break
                except Exception as e:
                    print(f"    icono descartado ({cand}): {e}")

            payload = {
                "id": slug(app['id']),
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
            }
            if icono:
                clave = hashlib.sha256(icono.encode()).hexdigest()
                icons_catalog[clave] = icono
                payload["icon_key"] = clave

            if nombre_archivo.lower().endswith('.zip') and 'extract_file' in app:
                payload["extract_file"] = app['extract_file']

            repo_data.append(payload)
            print(f" -> OK: {version} ({nombre_archivo}) {'con icono' if icono else 'SIN ICONO'}")
        else:
            print(f" -> ERROR: No se encontró versión válida.")

    catalogo = {
        "name": NOMBRE_REPO,
        "icons_url": "icons.json",
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "payloads": repo_data,
    }
    with open("payloads.json", "w", encoding="utf-8") as f:
        json.dump(catalogo, f, indent=4, ensure_ascii=False)
    # payloads_v2.json ya no se usa: si queda alguno viejo, se borra
    if os.path.exists("payloads_v2.json"):
        os.remove("payloads_v2.json")

    # icons.json con la forma {"icons": {clave: data URI}} que exige el Payload Manager
    with open("icons.json", "w", encoding="utf-8") as f:
        json.dump({"icons": icons_catalog}, f, indent=1, ensure_ascii=False)

    sin_icono = [p["name"] for p in repo_data if "icon_key" not in p]
    print(f"\nGenerados payloads.json e icons.json ({len(icons_catalog)} iconos).")
    if sin_icono:
        print(f"AVISO: {len(sin_icono)} payloads sin icono: {', '.join(sin_icono)}")

if __name__ == "__main__":
    main()
