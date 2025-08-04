from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Simpan API Key NFT.Storage di server
NFT_STORAGE_API_KEY = "MASUKKAN_API_KEY_NFT_STORAGE_KAMU_DI_SINI"

@app.route("/")
def home():
    return "IVN Token Gateway is running!"

@app.route("/upload_icon", methods=["POST"])
def upload_icon():
    if "icon" not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400
    
    icon_file = request.files["icon"]

    headers = {
        "Authorization": f"Bearer {NFT_STORAGE_API_KEY}"
    }

    response = requests.post(
        "https://api.nft.storage/upload",
        headers=headers,
        files={"file": (icon_file.filename, icon_file)}
    )

    if response.status_code == 200:
        cid = response.json()["value"]["cid"]
        url = f"https://{cid}.ipfs.nftstorage.link/"
        return jsonify({"status": "success", "icon_url": url})
    else:
        return jsonify({"status": "error", "message": response.text}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
