import json
import urllib.request

# Aquí están todos tus enlaces traducidos a su versión de lectura automática (API)
APPS = [
    {"name": "PS5 Payload Manager", "author": "itsPLK", "api": "https://api.github.com/repos/itsPLK/ps5-payload-manager/releases/latest"},
    {"name": "ShadowMountPlus", "author": "drakmor", "api": "https://api.github.com/repos/drakmor/ShadowMountPlus/releases/latest"},
    {"name": "FTP Server", "author": "ps5-payload-dev", "api": "https://api.github.com/repos/ps5-payload-dev/ftpsrv/releases/latest"},
    {"name": "Kstuff Lite", "author": "EchoStretch", "api": "https://api.github.com/repos/EchoStretch/kstuff-lite/releases/latest"},
    {"name": "Elf Arsenal", "author": "soniciso", "api": "https://git.etawen.dev/api/v1/repos/soniciso/elf-arsenal/releases/latest"},
    {"name": "PS5 Game Compressor", "author": "juma-sayeh", "api": "https://api.github.com/repos/juma-sayeh/PS5-Game-Compressor/releases/latest"},
    {"name": "nanoDNS", "author": "drakmor", "api": "https://api.github.com/repos/drakmor/nanoDNS/releases/latest"},
    {"name": "Garlic Save Manager", "author": "earthonion", "api": "https://git.etawen.dev/api/v1/repos/earthonion/garlic-savemgr/releases/latest"}
]

def obtener_datos_api(url):
    try:
        # Nos hacemos pasar por un navegador para que no nos bloqueen
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            datos = json.loads(response.read().decode())
            version = datos.get("tag_name", "Desconocida")
            
            # Buscar específicamente archivos .elf o .bin
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
    # Esta es la base obligatoria que lee el PS5 Payload Manager
    repo_data = {
        "name": "Mi Repositorio Automático",
        "description": "Actualizado automáticamente mediante GitHub Actions",
        "version": "1.0",
        "payloads": []
    }

    for app in APPS:
        print(f"Buscando actualizaciones para {app['name']}...")
        version, nombre_archivo, url = obtener_datos_api(app['api'])
        
        # Si encuentra el archivo, lo añade a la lista
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

    # Guardar todo en el archivo final
    with open("repo.json", "w", encoding="utf-8") as f:
        json.dump(repo_data, f, indent=4)
    print("El archivo repo.json se ha generado correctamente.")

if __name__ == "__main__":
    m
  ain()
