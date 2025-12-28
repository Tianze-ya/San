import asyncio
import threading
from flask import Flask, jsonify
from flask_cors import CORS
from waitress import serve
from san_server import SanServer
from log import Logger

HOST = "127.0.0.1"
PORT = 5000


logger = Logger(__file__)
app = Flask(__name__)
san = SanServer()
CORS(app)


@app.route("/process", methods=["POST"])
def process_data():
    # 处理逻辑
    san.broadcast_message("Hello, San!")
    return jsonify({"result": "success"})


def run_server():
    serve(app, host=HOST, port=PORT)


def run():
    app.run(host=HOST, port=PORT, use_reloader=False)


def run_san():
    try:
        asyncio.run(san.run())
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("SanServer stopped")


if __name__ == "__main__":
    logger.info("------------------------------------------------------------")
    san_thread = threading.Thread(target=run_san)
    san_thread.daemon = True
    san_thread.start()

    logger.info(f"Starting FlaskServer on {HOST}:{PORT}")
    run_server()
    logger.info("FlaskServer stopped")
    logger.info("------------------------------------------------------------")
