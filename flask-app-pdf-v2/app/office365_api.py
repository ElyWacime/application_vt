from dotenv import load_dotenv
import os
import requests
from app.graph_api import get_access_token, get_site_id, get_drive_id, get_folder_id

load_dotenv()

SHAREPOINT_SITE = os.getenv('SHAREPOINT_SITE')
SHAREPOINT_SITE_NAME = os.getenv('SHAREPOINT_SITE_NAME')
SHAREPOINT_DOC = os.getenv('SHAREPOINT_DOC')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET_VALUE')

class SharePoint:
    def _auth(self):
        try:
            access_token = get_access_token()
            return access_token
        except Exception as e:
            print(f"Error authenticating: {e}")
            raise

    def upload_file(self, file_name, folder_path, content):
        access_token = self._auth()
        site_id = get_site_id(access_token, SHAREPOINT_SITE_NAME)
        drive_id = get_drive_id(access_token, site_id)
        folder_id = get_folder_id(access_token, site_id, drive_id, folder_path)
        
        url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{folder_id}:/{file_name}:/content"

        # use this if i want to create a folder that doesn't exist
        # url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{folder_path}/{file_name}:/content"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/octet-stream'
        }
        response = requests.put(url, headers=headers, data=content)
        response.raise_for_status()
        return response.json()
    
    def upload_file_in_chunks(self, file_path, folder_name, chunk_size, chunk_uploaded=None, **kwargs):
        conn = self._auth()
        # Modified to use the root-relative path
        target_folder_url = f'{SHAREPOINT_DOC}/{folder_name}'
        target_folder = conn.web.get_folder_by_server_relative_path(target_folder_url)
        response = target_folder.files.create_upload_session(
            source_path=file_path,
            chunk_size=chunk_size,
            chunk_uploaded=chunk_uploaded,
            **kwargs
        ).execute_query()
        return response

###################################################
##### YOU SHOULD TAKE A LOOK AT THIS FUNCTION #####
###################################################


# def upload_file_to_sharepoint(access_token, site_id, drive_id, folder_path, file_path):
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/octet-stream'
#     }
    
#     file_name = os.path.basename(file_path)
#     upload_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{folder_path}/{file_name}:/content"
    
#     with open(file_path, 'rb') as file:
#         response = requests.put(upload_url, headers=headers, data=file)
    
#     response.raise_for_status()
#     print(f"File uploaded successfully: {response.json()}")
#     return response.json()

# # Example usage
# if __name__ == "__main__":
#     access_token = get_access_token()
#     site_id = get_site_id(access_token, os.getenv('SHAREPOINT_SITE_NAME'))
#     drive_id = get_drive_id(access_token, site_id)
#     folder_path = "Documents partages/09-Projets/AAA_FOR_TEST_TO_DELETE_LATER"  # Adjust the folder path as needed
#     file_path = "/path/to/your/file.txt"  # Adjust the file path as needed
    
#     upload_file_to_sharepoint(access_token, site_id, drive_id, folder_path, file_path)