# -*- coding: utf-8 -*-
import os

import pytest

from smolstore import SmolStore
from smolstore.table import Table


@pytest.fixture
def create_file_store():
    filename = "store.db"
    store = SmolStore(filename)
    return store


def test_save_empty_store_to_file(create_file_store):
    store = create_file_store
    try:
        store.save()
        assert os.path.exists("store.db")
    finally:
        os.remove("store.db")


def test_save_empty_table_to_file(create_file_store):
    store = create_file_store
    try:
        _ = store.table()
        store.save()
        assert os.path.exists("store.db")

        store = SmolStore("store.db")
        assert isinstance(store._tables.get("_default"), Table)
    finally:
        os.remove("store.db")


def test_save_and_load_docs_file(create_file_store):
    store = create_file_store
    docs = store.table("docs")
    docs.insert({"username": "ray"})
    try:
        store.save()

        store = SmolStore("store.db")
        docs = store.table("docs")
        doc = docs.first(docs.fields.username == "ray")
        assert doc == {"username": "ray"}
    finally:
        os.remove("store.db")
