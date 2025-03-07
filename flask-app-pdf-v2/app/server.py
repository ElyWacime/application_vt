from flask import Flask, Response, request
import requests

app = Flask(__name__)
# Identifiants KoboToolbox
KOBO_USERNAME = "el_ayeb_ahmed"
KOBO_PASSWORD = "NouvelArrivant*2024"
# URL de base pour récupérer les images
BASE_URL = "https://kc-eu.kobotoolbox.org/media/original"
@app.route("/proxy_image")
def proxy_image():
    """Récupère une image protégée depuis KoboToolbox et la renvoie sans restriction"""
    image_path = request.args.get("image")
    if not image_path:
        return "Image path missing", 400
    # Construire l'URL complète de l'image
    full_url = f"{BASE_URL}?media_file={image_path}"
    # Télécharger l'image avec authentification
    response = requests.get(full_url, auth=(KOBO_USERNAME, KOBO_PASSWORD))
    if response.status_code == 200:
        return Response(response.content, content_type=response.headers['Content-Type'])
    else:
        return f"Erreur {response.status_code}", response.status_code
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)