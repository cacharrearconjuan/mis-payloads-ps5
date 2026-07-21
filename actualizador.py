import json
import urllib.request

APPS = [
    {"name": "PS5 Payload Manager", "author": "itsPLK", "api": "https://api.github.com/repos/itsPLK/ps5-payload-manager/releases"},
    {"name": "ShadowMountPlus", "author": "drakmor", "api": "https://api.github.com/repos/drakmor/ShadowMountPlus/releases"},
    {"name": "FTP Server", "author": "ps5-payload-dev", "api": "https://api.github.com/repos/ps5-payload-dev/ftpsrv/releases"},
    {"name": "Kstuff Lite", "author": "EchoStretch", "api": "https://api.github.com/repos/EchoStretch/kstuff-lite/releases"},
    {"name": "Elf Arsenal", "author": "soniciso", "api": "https://git.etawen.dev/api/v1/repos/soniciso/elf-arsenal/releases"},
    {"name": "PS5 Game Compressor", "author": "juma-sayeh", "api": "https://api.github.com/repos/juma-sayeh/PS5-Game-Compressor/releases"},
    {"name": "nanoDNS", "author": "drakmor", "api": "https://api.github.com/repos/drakmor/nanoDNS/releases"},
    {"name": "Garlic Save Manager", "author": "earthonion", "api": "https://git.etawen.dev/api/v1/repos/earthonion/garlic-savemgr/releases"}
]

# Exclusivamente ejecutables directos
EXEC_EXTENSIONS = ('.elf', '.bin')

def obtener_datos_api(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            releases = json.loads(response.read().decode())
            
            if not isinstance(releases, list):
                releases = [releases]

            # Recorre las releases ordenadas por fecha
            for datos in releases:
                version = datos.get("tag_name", "Desconocida")
                assets = datos.get("assets", [])

                # Recopilar todos los ejecutables de esta versión
                ejecutables = []
                for asset in assets:
                    nombre = asset.get("name", "")
                    if nombre.lower().endswith(EXEC_EXTENSIONS):
                        ejecutables.append({
                            "nombre": nombre,
                            "url": asset.get("browser_download_url", "")
                        })
                
                # Si hemos encontrado ejecutables en esta versión
                if ejecutables:
                    # Por defecto, cogemos el primero
                    elegido = ejecutables[0]
                    
                    # Pero si hay varios, priorizamos el que tenga "ps5" en el nombre
                    for exe in ejecutables:
                        if "ps5" in exe["nombre"].lower():
                            elegido = exe
                            break
                            
                    return version, elegido["nombre"], elegido["url"]
                    
            return None, None, None
    except Exception as e:
        print(f"Error consultando {url}: {e}")
        return None, None, None

def main():
    repo_data = {
        "name": "Mi Repositorio Automático",
        "description": "Actualizado automáticamente mediante GitHub Actions",
        "version": "1.0",
        "payloads": []
    }

    for app in APPS:
        print(f"Buscando actualizaciones para {app['name']}...")
        version, nombre_archivo, url = obtener_datos_api(app['api'])
        
        if version and url:
            repo_data["payloads"].append({
                "name": app['name'],
                "author": app['author'],
                "version": version,
                "filename": nombre_archivo,
                "url": url
            })
            print(f" -> Encontrada versión {version}: {nombre_archivo}")
        else:
            print(f" -> ERROR: No se encontró ningún .elf/.bin directo en {app['name']}")

    with open("repo.json", "w", encoding="utf-8") as f:
        json.dump(repo_data, f, indent=4)
    print("El archivo repo.json se ha generado correctamente.")

if __name__ == "__main__":
    main()
