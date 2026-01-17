import os
import datetime


class Logger:
    def __init__(self, name: str):
        self.name = os.path.basename(name)
        dir = os.path.dirname(__file__)
        logs = os.path.join(dir, "logs")

        if not os.path.isdir(logs):
            os.mkdir(logs)

        self.log_path = os.path.join(dir, "logs", f"{self.get_date()}.log")

    def info(self, message: str):
        self.log("INFO", message)

    def error(self, message: str):
        self.log("ERROR", message)

    def debug(self, message: str):
        self.log("DEBUG", message)

    def log(self, level: str, message: str):
        data = f"[{self.get_time()}] {level} [{self.name}] - {message}\n"
        print(data)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(data)

    def get_date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def get_time(self):
        return datetime.datetime.now().strftime("%H:%M:%S")


if __name__ == "__main__":
    logger = Logger()
