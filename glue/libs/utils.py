from pydantic import BaseModel
from typing import List
import smart_open
import logging


def write_list_model_newline_json(file_path: str, model_list=List[BaseModel]) -> None:
    """Takes a list of models derived from the Pydantic BaseModel and writes them to a file as newline-delimited json"""
    with smart_open.open(file_path, "w") as f:
        for item in model_list:
            json_line = f"{item.model_dump_json()}\n"
            f.write(json_line)


def get_logger() -> logging.Logger:
    """Gets a logger and sets level to INFO"""
    logger = logging.getLogger()
    logger.level(logging.INFO)

    return logger
