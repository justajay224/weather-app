from flask import Flask, send_file, abort

app = Flask(__name__, static_folder="static")

@app.route("/")
def serve_index():
    return send_file("index.html")

@app.route("/<path:path>")
def block_direct_access(path):
        return send_file("index.html")  # Fallback ke halaman utama

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
