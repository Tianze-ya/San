import asyncio
import threading
import os
import signal
from flask import Flask, jsonify, request
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


@app.before_request
def before_request():
    # 记录请求信息
    logger.info(f"Request: {request.method} {request.path}")
    logger.info(f"IP: {request.remote_addr}")
    logger.info(f"User-Agent: {request.headers.get('User-Agent')}")


@app.route("/active", methods=["POST"])
def active():
    # san.broadcast_message("Hello, San!")
    return todata("active")


@app.route("/exit", methods=["POST"])
def exit():
    os.kill(os.getpid(), signal.SIGINT)
    return todata("exit")


def todata(name: str = "", data: str = ""):
    return jsonify({"name": name, "data": data})


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
    san_thread = threading.Thread(target=run_san)
    san_thread.daemon = True
    san_thread.start()

    logger.info(f"Starting FlaskServer on {HOST}:{PORT}")
    run_server()
    logger.info("FlaskServer stopped")
