from datetime import date
import json,  uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    dob: date = Field(title='Date of Birth')
class Ship(BaseModel):
    id: str
    name: str
    sign:str
    classification: str
    speed: str

ships = [
    Ship(id='1', sign='n/n', name= 'Kronos One', classification='K\'t\'inga-class', speed='Warp 2.6' ),
    #   Ship(id=2, name= 'USS Excelsior NCC-2000', classification='Excelsior-Class', speed='Warp 2.6' ),
    #   Ship(id=3, name= 'USS Defiant NX-74205', classification='n/a', speed='Warp 2.6' ),
    #   Ship(id=4, name= 'USS Reliant NCC-1864', classification='n/a', speed='Warp 2.6' ),
    #   Ship(id=5, name= 'USS Enterprise NCC-1701D', classification='Galaxy-Class', speed='> Warp 10' ),
    #   Ship(id=6, name= 'USS Hathaway NCC-2593', classification='Galaxy-Class', speed='Warp 1' ),
]
# define some users
users = [
    User(id=1, name='John', dob=date(1990, 1, 1)),
    User(id=2, name='Jack', dob=date(1991, 1, 1)),
    User(id=3, name='Jill', dob=date(1992, 1, 1)),
    User(id=4, name='Jane', dob=date(1993, 1, 1)),
]
ship_data = None

def ship_json_to_ship_entity(ship_json : str) -> Ship:
    keys = ship_json.keys()
    name = ship_json['name'] if 'name' in keys else "n/n"
    speed = ship_json['topSpeed'] if 'topSpeed' in keys else "n/n"
    sign = ship_json['sign'] if 'sign' in keys else "n/n"
    classification = ship_json['shipClass'] if 'shipClass' in keys else "n/n"
    id = str(uuid.uuid5(uuid.NAMESPACE_DNS, name))   #+speed+sign+classification))
    ship = Ship(id=id, sign=sign, name=name, classification=classification, speed=speed)
    return ship

def read_ships():
    with open("ships_full.json", "r") as read_content: 
        ship_data = json.load(read_content)
    for s in ship_data:
        ships.append(ship_json_to_ship_entity(s))

@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def ships_table() -> list[AnyComponent]:
    read_ships()
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text='Ships', level=2),  # renders `<h2>Users</h2>`
                c.Table(
                    data=ships,
                    # define two columns for the table
                    columns=[
                        # the first is the ships, name rendered as a link to their profile
                        DisplayLookup(field='name', on_click=GoToEvent(url='/ships/{id}/')),
                        DisplayLookup(field='sign', on_click=GoToEvent(url='/ships/{id}/')),
                        DisplayLookup(field='classification', on_click=GoToEvent(url='/ships/{id}/')),
                    ],
                ),
            ]
        ),
    ]

@app.get("/api/ships/{ship_id}/", response_model=FastUI, response_model_exclude_none=True)
def ship_profile(ship_id: str) -> list[AnyComponent]:
    """
    Ship profile page, the frontend will fetch this when the user visits `/ships/{id}/`.
    """
    try:
        ship = next(s for s in ships if s.id == ship_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Ship not found")
    return [
        c.Page(
            components=[
                c.Heading(text=ship.name, level=2),
                c.Link(components=[c.Text(text='Back')], on_click=BackEvent()),
                c.Details(data=ship),
            ]
        ),
    ]

@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))