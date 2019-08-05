# -*- coding: utf-8 -*-
import pytest

from smolstore import Field
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
    doc = next(table.get(table.fields.user_id == 10))
    assert isinstance(doc, Document)


def test_modify_document(table, new_document):
    table.insert(new_document)
    doc = next(table.get(table.fields.user_id == 10))
    doc["last_name"] = "Doe"
    assert doc == {"first_name": "John", "last_name": "Doe", "user_id": 10}
    doc = next(table.get(table.fields.user_id == 10))
    assert doc["last_name"] == "Doe"
    doc = list(table.get(table.fields.last_name == "Smith"))
    assert len(doc) == 0


def test_modify_indexed_document(table, new_document):
    table.fields.first_name = Field("first_name", index=True)
    table.insert(new_document)
    doc = next(table.get(table.fields.first_name == "John"))
    doc["first_name"] = "Michael"
    assert doc == {"first_name": "Michael", "last_name": "Smith", "user_id": 10}
    doc = list(table.get(table.fields.first_name == "John"))
    assert len(doc) == 0
    doc = next(table.get(table.fields.first_name == "Michael"))
    assert doc == {"first_name": "Michael", "last_name": "Smith", "user_id": 10}


def test_delete_document(table, new_document):
    table.insert(new_document)
    assert len(table) == 1
    doc = next(table.get(table.fields.first_name == "John"))
    doc.delete()
    assert len(table) == 0
    doc = list(table.get(table.fields.first_name == "John"))
    assert len(doc) == 0


def test_delete_indexed_document(table, new_document):
    table.fields.first_name = Field("first_name", index=True)
    table.insert(new_document)
    assert len(table) == 1
    doc = next(table.get(table.fields.first_name == "John"))
    doc.delete()
    assert len(table) == 0
    doc = list(table.get(table.fields.first_name == "John"))
    assert len(doc) == 0
