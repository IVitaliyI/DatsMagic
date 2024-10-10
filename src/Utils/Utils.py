from datetime import datetime
import logging
import json
import os


class Logger:
    def __init__(self, log_file: str = "program.log") -> None:
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.info("Logging initialized")

    @staticmethod
    def log_info(message: str):
        logging.info(message)

    @staticmethod
    def log_error(message: str):
        logging.error(message)


class DataSaver:
    def __init__(self) -> None:
        self.folder_name = self.create_output_folder()

    def create_output_folder(self) -> str:
        folder_name = datetime.now().strftime("session_%Y-%m-%d_%H-%M-%S")
        os.makedirs(folder_name, exist_ok=True)
        Logger.log_info(f"Output folder created: {folder_name}")
        return folder_name

    def save_to_file(self, file_name, data):
        file_path = os.path.join(self.folder_name, file_name)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)  # Сохраняем данные в JSON-файл
        Logger.log_info(f"Data saved to {file_path}")
