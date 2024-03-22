from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    dob: date = Field(title='Date of Birth')
class Ship(BaseModel):
    id: int
    name: str
    classification: str
    speed: str

ships = [
    Ship(id=1, name= 'Kronos One', classification='K\'t\'inga-class', speed='Warp 2.6' ),
      Ship(id=2, name= 'USS Excelsior NCC-2000', classification='Excelsior-Class', speed='Warp 2.6' ),
      Ship(id=3, name= 'USS Defiant NX-74205', classification='n/a', speed='Warp 2.6' ),
      Ship(id=4, name= 'USS Reliant NCC-1864', classification='n/a', speed='Warp 2.6' ),
      Ship(id=5, name= 'USS Enterprise NCC-1701D', classification='Galaxy-Class', speed='> Warp 10' ),
      Ship(id=6, name= 'USS Hathaway NCC-2593', classification='Galaxy-Class', speed='Warp 1' ),
]
# define some users
users = [
    User(id=1, name='John', dob=date(1990, 1, 1)),
    User(id=2, name='Jack', dob=date(1991, 1, 1)),
    User(id=3, name='Jill', dob=date(1992, 1, 1)),
    User(id=4, name='Jane', dob=date(1993, 1, 1)),
]


@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def ships_table() -> list[AnyComponent]:
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
                        # the second warp speed
                        DisplayLookup(field='speed', mode=DisplayMode.auto),
                    ],
                ),
            ]
        ),
    ]

@app.get("/api/ships/{ship_id}/", response_model=FastUI, response_model_exclude_none=True)
def ship_profile(ship_id: int) -> list[AnyComponent]:
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