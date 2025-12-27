import os
import datetime


class Logger:
    def __init__(self):
        dir = os.path.dirname(__file__)
        logs =  os.path.join(dir, "logs")

        if not os.path.isdir(logs):
            os.mkdir(logs)
        
        self.log_path = os.path.join(dir, "logs", f"{self.get_date()}.log")
        self.log_file = open(self.log_path, "a", encoding="utf-8")

    def info(self, message: str):
        self.log("INFO", message)

    def error(self, message: str):
        self.log("ERROR", message)  

    def debug(self, message: str):  
        self.log("DEBUG", message)

    def log(self, level: str, message: str):
        data = f"[{self.get_time()}] {level} - {message}\n"
        #print(data)
        self.log_file.write(data)

    def get_date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def get_time(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def __del__(self):
        self.log_file.close()

if __name__ == "__main__":
    logger = Logger()
