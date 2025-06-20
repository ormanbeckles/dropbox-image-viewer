from flask import Flask, jsonify
from flask_cors import CORS
import dropbox
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains (or configure specific origins)

ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')

def list_images_from_dropbox(folder_path=''):
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    try:
        res = dbx.files_list_folder(folder_path)
        images = []
        for entry in res.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                if entry.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    link = dbx.files_get_temporary_link(entry.path_lower)
                    images.append({'name': entry.name, 'link': link.link})
        return images
    except dropbox.exceptions.ApiError as err:
        return {'error': str(err)}

@app.route('/images', methods=['GET'])
def get_images():
    images = list_images_from_dropbox()
    return jsonify(images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
