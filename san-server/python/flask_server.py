import asyncio
import threading
import os
import signal
from message import make_msg
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
    logger.debug(f"Request: {request.method} {request.path} IP: {request.remote_addr}")


@app.route("/active", methods=["POST"])
def active():
    return todata("active")


@app.route("/api", methods=["POST"])
async def message():
    data = request.get_json()["data"]
    name = data["name"]
    addr = data["address"]
    match name:
        case "getAllAddress":
            all_addr = await san.get_all_addresses()
            return todata("AllAddress", all_addr)
        case "photo":
            msg = make_msg("photo", addr=addr)
            await san.send_message(msg)
            return todata("photo", "ok")
        case _:
            logger.error(f"未知Api: {name}")

    # san.broadcast_message(data["message"])


@app.route("/exit", methods=["POST"])
def exit():
    os.kill(os.getpid(), signal.SIGINT)
    return todata("exit")


def todata(name: str = "", data: str = ""):
    return jsonify({"name": name, "data": data})


def run_server():
    serve(app, host=HOST, port=PORT)


def run_san():
    asyncio.run(san.run())


if __name__ == "__main__":
    san_thread = threading.Thread(target=run_san)
    san_thread.daemon = True
    san_thread.start()

    logger.info(f"Starting FlaskServer on {HOST}:{PORT}")
    try:
        run_server()
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("SanServer stopped")
        logger.info("FlaskServer stopped")
        asyncio.sleep(0.3)
