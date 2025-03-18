from flask import Blueprint, request, send_file, jsonify, Response
from io import BytesIO
from app.my_utils2 import create_pdf_from_data
import os
import requests
from app.carte import draw_map
from dotenv import load_dotenv
from flask import abort, send_from_directory

load_dotenv()
KOBO_USERNAME = os.getenv("KOBO_USERNAME")
KOBO_PASS = os.getenv("KOBO_PASSWORD")
BASE_URL = "https://kc-eu.kobotoolbox.org/media/original"

bp = Blueprint('routes', __name__)

@bp.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        pdf_file_path = create_pdf_from_data(data)
        print("\n\n\n\n\n####################\n\n\n\n\n")
        if not os.path.exists(pdf_file_path):
            return jsonify({"error": f"File not found: {pdf_file_path}"}), 500
        print(f"PDF generated at: {pdf_file_path}")
        return send_file(pdf_file_path, download_name='output.pdf', as_attachment=True, mimetype='application/pdf')
    except Exception as e:
        print("\n\n\n\nERROR\n\n\n\n\n")
        return jsonify({"error": str(e)}), 500
    

@bp.route("/proxy_image")
def proxy_image():
    image_path = request.args.get("image")
    if not image_path:
        return "Image path missing", 400
    # Construire l'URL complète de l'image
    full_url = f"{BASE_URL}?media_file={image_path}"
    # Télécharger l'image avec authentification
    response = requests.get(full_url, auth=(KOBO_USERNAME, KOBO_PASS))
    if response.status_code == 200:
        return Response(response.content, content_type=response.headers['Content-Type'])
    else:
        return f"Erreur {response.status_code}", response.status_code

@bp.route("/vt-map/")
def serve_map():
    map_name = request.args.get("map")  
    print(">>>>>>>>>>>>>>>>: "+map_name)
    if not map_name:
        return abort(400, "Missing 'map' parameter")

    file_path = os.path.join("/var/www/vt_maps/", f"{map_name}")
    print(">>>>>>>>>>>>>>>>>: "+file_path)
    # Ensure the file exists before serving
    if os.path.exists(file_path):
        return send_from_directory("/var/www/vt_maps/", map_name)
    else:
        return abort(404, "Map file not found")
