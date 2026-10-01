import os
import uuid
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Database memori sementara (array)
notes = []

# 1. Endpoint: Mengambil semua catatan (READ)
@app.route("/api/notes", methods=["GET"])
def get_notes():
    return jsonify(notes)

# 2. Endpoint: Menambah catatan baru (CREATE)
@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    
    new_note = {
        "id": str(uuid.uuid4()), 
        "title": data.get("title", ""), 
        "content": data.get("content", "")
    }
    notes.insert(0, new_note) # Masukkan ke urutan paling atas
    
    return jsonify(new_note), 201

# 3. Endpoint: Menghapus catatan (DELETE)
@app.route("/api/notes/<note_id>", methods=["DELETE"])
def delete_note(note_id):
    global notes
    # Filter array: simpan semua catatan KECUALI yang ID-nya cocok dengan note_id
    notes = [note for note in notes if note["id"] != note_id]
    return jsonify({"message": "Catatan dihapus"}), 200

# 4. Rute utama: Menampilkan file index.html ke browser
@app.route("/", methods=["GET"])
def serve_frontend():
    # Mencari lokasi file index.html yang berada satu folder di atas folder 'api'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'index.html')
    return send_file(html_path)

# Script eksekusi untuk testing di lokal
if __name__ == "__main__":
    app.run(port=8000, debug=True)