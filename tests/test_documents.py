# -*- coding: utf-8 -*-
import pytest

from smolstore.document import Document
from smolstore.store import SmolStore


@pytest.fixture
def table():
    store = SmolStore()
    table = store.table()
    return table


@pytest.fixture
def new_document():
    return {"first_name": "John", "last_name": "Smith", "user_id": 10}


def test_add_document(table, new_document):
    table.insert(new_document)
    doc = table.get(table.fields.user_id == 10)[0]
    assert isinstance(doc, Document)


def test_modify_document(table, new_document):
    table.insert(new_document)
    doc = table.get(table.fields.user_id == 10)[0]
    doc["last_name"] = "Doe"
    assert doc == {"first_name": "John", "last_name": "Doe", "user_id": 10}
    doc = table.get(table.fields.user_id == 10)[0]
    assert doc["last_name"] == "Doe"
    doc = table.get(table.fields.last_name == "Smith")
    assert len(doc) == 0


def test_modify_indexed_document(table, new_document):
    table.insert(new_document)
    table.fields.first_name.indexed = True
    doc = table.get(table.fields.first_name == "John")[0]
    doc["first_name"] = "Michael"
    assert doc == {"first_name": "Michael", "last_name": "Smith", "user_id": 10}
    doc = table.get(table.fields.first_name == "John")
    assert len(doc) == 0
    doc = table.get(table.fields.first_name == "Michael")[0]
    assert doc == {"first_name": "Michael", "last_name": "Smith", "user_id": 10}


def test_delete_document(table, new_document):
    table.insert(new_document)
    assert len(table) == 1
    doc = table.get(table.fields.first_name == "John")[0]
    doc.delete()
    assert len(table) == 0
    doc = table.get(table.fields.first_name == "John")
    assert len(doc) == 0


def test_delete_indexed_document(table, new_document):
    table.insert(new_document)
    table.fields.first_name.indexed = True
    assert len(table) == 1
    doc = table.get(table.fields.first_name == "John")[0]
    doc.delete()
    assert len(table) == 0
    doc = table.get(table.fields.first_name == "John")
    assert len(doc) == 0
