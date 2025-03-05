from app.office365_api import SharePoint
from app.graph_api import get_access_token, get_site_id, get_drive_id, get_folder_id
import os
from dotenv import load_dotenv

load_dotenv()

SHAREPOINT_SITE = os.getenv('SHAREPOINT_SITE')
SHAREPOINT_SITE_NAME = os.getenv('SHAREPOINT_SITE_NAME')
SHAREPOINT_DOC = os.getenv('SHAREPOINT_DOC')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET_VALUE')

# link : https://enervivo.sharepoint.com/:f:/g/EgP6jb-_DaJKgc3FfEgSVygBytTJid8MOvW5a0B7FFJ_kg?e=2Fxruh

if (__name__) == "__main__":
    sharepoint = SharePoint()

    access_token = get_access_token()
    site_id = get_site_id(access_token, SHAREPOINT_SITE_NAME)
    drive_id = get_drive_id(access_token, site_id)
    folder_id = get_folder_id(access_token, site_id, drive_id, "AAA_FOR_TEST_TO_DELETE_LATER")

    print(folder_id)
