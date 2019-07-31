# -*- coding: utf-8 -*-
import os

import pytest
from smolstore import SmolStore


@pytest.fixture
def create_file_store():
    filename = "store.db"
    store = SmolStore(filename)
    return store


def test_save_empty_store_to_file(create_file_store):
    store = create_file_store
    store.commit()
    assert os.path.exists("store.db")
    os.remove("store.db")


def test_save_empty_table_to_file(create_file_store):
    store = create_file_store
    _ = store.table()
    store.commit()
    assert os.path.exists("store.db")
    os.remove("store.db")
