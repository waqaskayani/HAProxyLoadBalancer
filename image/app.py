from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def index():
    return(f"Hostname: {socket.gethostname()}, Waqas")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
