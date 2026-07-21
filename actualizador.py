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

def obtener_datos_api(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            releases = json.loads(response.read().decode())
            
            # Si devuelve una lista, cogemos el primer elemento (el más reciente de todos)
            if isinstance(releases, list) and len(releases) > 0:
                datos = releases[0]
            else:
                datos = releases

            version = datos.get("tag_name", "Desconocida")
            
            url_descarga = ""
            nombre_archivo = ""
            for asset in datos.get("assets", []):
                nombre = asset.get("name", "")
                if nombre.endswith(".elf") or nombre.endswith(".bin"):
                    url_descarga = asset.get("browser_download_url", "")
                    nombre_archivo = nombre
                    break
                    
            return version, nombre_archivo, url_descarga
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
