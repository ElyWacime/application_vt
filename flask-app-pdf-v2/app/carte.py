import json
import requests
from requests.auth import HTTPBasicAuth
import folium
import base64
import os
from dotenv import load_dotenv

load_dotenv()

KOBO_USERNAME = os.getenv("KOBO_USERNAME")
KOBO_PASS = os.getenv("KOBO_PASSWORD")
KOBO_AUTH = (KOBO_USERNAME, KOBO_PASS)

BASE_URL = "https://kc-eu.kobotoolbox.org/media/original"



def draw_map(data):
    dict_geopoint_image_url={}
    s=0
    for key in data: 
        if "/g" in key:    
            geoloc=data[key]
            coordinates = tuple(map(float, geoloc.split()[:2]))
            image_url=data["_attachments"][s]["download_url"]
            dict_geopoint_image_url[coordinates]=image_url
            s+=1

    map_center = [list(dict_geopoint_image_url.keys())[0][0], list(dict_geopoint_image_url)[0][1]]
    m = folium.Map(location=map_center, zoom_start=15)
    for point , url in dict_geopoint_image_url.items():
        PROXY_IMAGE_URL=url.replace("https://kc-eu.kobotoolbox.org/media/original?media_file=","http://127.0.0.1:8080/proxy_image?image=")
        popup_html = f"""
    <div style="width:200px">
        <b>Image KoboToolbox</b><br>
        <img src="{PROXY_IMAGE_URL}" style="width:100%; max-height:150px;"><br>
        <a href="{PROXY_IMAGE_URL}">Cliquer pour afficher l\'image</a><br>
        Cliquez à l'extérieur pour fermer
    </div>
    """     
        folium.Marker(
            location=list(point),
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(icon="info-sign", color="blue")
        ).add_to(m)

    m.save("/var/www/vt_maps/"+data["projet"]+".html")
    return f"{data["projet"]}.html"
