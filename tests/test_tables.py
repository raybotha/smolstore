# -*- coding: utf-8 -*-
import pytest

from smolstore import Field
from smolstore import SmolStore
from smolstore import UniqueViolation


@pytest.fixture
def store():
    return SmolStore()


@pytest.fixture
def basic_document():
    return {"username": "eve", "id": 42, "approved": True}


@pytest.fixture
def prefilled_table(store, basic_document):
    store.insert(basic_document)
    return store


def test_insert_document(store, basic_document):
    table = store.table()
    assert len(table) == 0
    table.insert(basic_document)
    assert len(table) == 1


def test_list_documents(prefilled_table, basic_document):
    assert list(prefilled_table) == [basic_document]


def test_search_document(prefilled_table, basic_document):
    table = prefilled_table
    documents = list(table.get(table.fields.username == "eve"))
    assert len(documents) == 1
    assert documents[0] == basic_document


def test_inequality_search_document(prefilled_table):
    table = prefilled_table
    table.insert({"username": "bob", "id": 85})
    docs = list(table.get(table.fields.username != "eve"))
    assert len(docs) == 1
    assert docs == [{"username": "bob", "id": 85}]


def test_delete_document(prefilled_table):
    table = prefilled_table
    assert len(table) == 1
    table.delete(table.fields.id == 42)
    assert len(table) == 0
    assert list(table.get(table.fields.username == "eve")) == []


def test_upsert_document(prefilled_table):
    table = prefilled_table
    table.upsert({"username": "eve", "approved": False}, table.fields.username == "eve")
    assert list(table) == [{"username": "eve", "id": 42, "approved": False}]
    assert list(table.get(table.fields.approved == True)) == []


def test_add_index_document(store, basic_document):
    table = store.table(fields=[Field("username", index=True)])
    assert len(table) == 0
    table.insert(basic_document)
    assert len(table.fields.username._hash_index[hash(basic_document["username"])]) == 1
    assert len(table) == 1
    assert list(table.get(table.fields.username == "eve")) == [
        {"username": "eve", "id": 42, "approved": True}
    ]


def test_inequality_search_indexed_document(store, basic_document):
    table = store.table(fields=[Field("username", index=True)])
    table.insert(basic_document)
    basic_document.update({"username": "bob"})
    table.insert(basic_document)
    assert len(table) == 2
    assert list(table.get(table.fields.username != "eve")) == [
        {"username": "bob", "id": 42, "approved": True}
    ]


def test_delete_indexed_document(store, basic_document):
    table = store.table(fields=[Field("eve", index=True)])
    table.insert(basic_document)
    assert len(table) == 1
    table.delete(table.fields.id == 42)
    assert len(table) == 0
    assert list(table.get(table.fields.username == "eve")) == []


def test_violate_unique_constraint(store, basic_document):
    table = store.table(fields=[Field("username", unique=True)])
    table.insert(basic_document)
    assert len(table) == 1
    with pytest.raises(UniqueViolation):
        table.insert({"username": "eve", "id": 120, "approved": False})
    assert len(table) == 1
    assert list(table.get(table.fields.username == "eve")) == [
        {"username": "eve", "id": 42, "approved": True}
    ]


def test_fields_added_with_document(prefilled_table):
    assert len(prefilled_table.fields) == 3
    assert "username" in prefilled_table.fields
    assert "id" in prefilled_table.fields
    assert "approved" in prefilled_table.fields
    assert isinstance(prefilled_table.fields.username, Field)
    assert isinstance(prefilled_table.fields.id, Field)
    assert isinstance(prefilled_table.fields.approved, Field)


def test_fields_added_unindexed(prefilled_table):
    assert prefilled_table.fields.username.indexed is False
    assert prefilled_table.fields.id.indexed is False
    assert prefilled_table.fields.approved.indexed is False


def test_fields_added_non_unique(prefilled_table):
    assert prefilled_table.fields.username.unique is False
    assert prefilled_table.fields.id.unique is False
    assert prefilled_table.fields.approved.unique is False


def test_raise_on_insert_non_mapping(prefilled_table):
    with pytest.raises(TypeError):
        prefilled_table.insert(["Hey there pal"])


def test_return_none_on_empty_first_query(prefilled_table):
    assert prefilled_table.first(prefilled_table.fields.username == "steve") is None
