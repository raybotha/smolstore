# -*- coding: utf-8 -*-
import json
from typing import MutableMapping


class JsonSerializer:
    @staticmethod
    def dump(filename: str, tables: MutableMapping):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(tables, file, ensure_ascii=False)

    @staticmethod
    def load(filename: str) -> MutableMapping:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
