from pydantic import BaseModel, Field

#
# Model used when adding new ships
#
class ShipForm(BaseModel):
    name: str
    sign:str
    classification: str
    speed: str

#
# Model used for everything persistence
#
class Ship(BaseModel):
     id: str
     name: str #= Field(title='Name')
     sign:str #= Field(title='Call-Sign')
     classification: str  #= Field(title='Ship Classification')
     speed: str  #= Field(title='Maximum Speed')
