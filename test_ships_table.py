# https://github.com/pydantic/FastUI/blob/main/src/python-fastui/tests/test_tables_display.py

import pytest
from fastui import components
from fastui.components import display
from pydantic import BaseModel, Field

class Ship(BaseModel):
     id: str
     name: str = Field(title='Name')
     sign:str = Field(title='Call-Sign')
     classification: str  = Field(title='Ship Classification')
     speed: str  = Field(title='Maximum Speed')


ships = [
       Ship(id='2', name= 'USS Excelsior', sign='NCC-2000', classification='Excelsior-Class', speed='Warp 2.6' ),
]

def test_all_data_fields_should_be_matched_by_correczt_table_headers():
    table = components.Table(data=ships)

    # insert_assert(table.model_dump(by_alias=True, exclude_none=True))
    assert table.model_dump(by_alias=True, exclude_none=True) == {
        'data': [{'id': '2', 'name': 'USS Excelsior', 'sign':'NCC-2000', 'classification':'Excelsior-Class', 'speed':'Warp 2.6'}],
        'columns': [{'field': 'id'}, {'field': 'name', 'title': 'Name'}, {'field': 'sign', 'title': 'Call-Sign'}, {'field': 'classification', 'title':'Ship Classification'}, {'field': 'speed', 'title':'Maximum Speed'}],
        'type': 'Table',
    }

