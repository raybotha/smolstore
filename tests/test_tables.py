# -*- coding: utf-8 -*-
import pytest

from smolstore import SmolStore


@pytest.fixture
def store():
    return SmolStore()


@pytest.fixture
def basic_document():
    return {"username": "eve", "id": 42, "approved": True}


@pytest.fixture
def prefilled_table(store, basic_document):
    table = store.table()
    table.insert(basic_document)
    return table


def test_insert_document(store, basic_document):
    table = store.table()
    assert len(table) == 0
    table.insert(basic_document)
    assert len(table) == 1


def test_list_documents(prefilled_table, basic_document):
    assert list(prefilled_table) == [basic_document]


def test_search_document(prefilled_table):
    table = prefilled_table
    documents = list(table.get(table.fields.username == "eve"))
    assert len(documents) == 1
    assert documents[0] == basic_document
