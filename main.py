from datetime import date
from typing import Annotated
import json,  uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent, PageEvent
from fastui.forms import SelectSearchResponse, fastui_form  #, FormResponse
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from database import StartrekShipModel, engine
app = FastAPI()

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

seed_data='ships_full.json'
#seed_data='ships_one.json'
ships = [
    Ship(id='1', sign='n/n', name= 'Kronos One', classification='K\'t\'inga-class', speed='Warp 2.6' ),
]
ship_data = None
from icecream import ic
def ship_json_to_shipModel_entity(ship_json : str) -> StartrekShipModel:
    ship = ship_json_to_ship_entity(ship_json)
    ic(ship)
    ssm = StartrekShipModel(id=ship.id, name=ship.name, speed=ship.speed, sign=ship.sign, classification=ship.classification)
    ic(ssm)
    return ssm

def ship_json_to_ship_entity(ship_json : str) -> Ship:
    keys = ship_json.keys()
    name = ship_json['name'] if 'name' in keys else "n/n"
    speed = ship_json['topSpeed'] if 'topSpeed' in keys else "n/n"
    sign = ship_json['sign'] if 'sign' in keys else "n/n"
    classification = ship_json['shipClass'] if 'shipClass' in keys else "n/n"
    id = str(uuid.uuid5(uuid.NAMESPACE_DNS, name))   #+speed+sign+classification))
    ship = Ship(id=id, sign=sign, name=name, classification=classification, speed=speed)
    return ship

@app.on_event("startup")
async def read_ships():
    import logging
    logging.basicConfig()
    logger = logging.getLogger('sqlalchemy.engine')
    logger.setLevel(logging.DEBUG)
    session = Session(engine)
    # with open(seed_data, "r") as read_content: 
    #     ship_data = json.load(read_content)
    # for s in ship_data:
    #     ships.append(ship_json_to_ship_entity(s))
    # check for previously imported data
    stmt = select(StartrekShipModel)
    res = session.exec(stmt).first()

    if ic(res) is None:
        print ('There appears to be NO data in the DB')

        with open(seed_data, "r") as seed_content: 
            ship_data = json.load(seed_content)
            #ic(ship_data)
            for s in ship_data:
                ssm = StartrekShipModel(**s)
                ic('>>'+str(ssm))
                session.add(ssm)
        #        ship = ship_json_to_shipModel_entity(s)
        #ssm = StartrekShipModel(
        #    id=str(uuid.uuid5(uuid.NAMESPACE_DNS, 'lhfkghirugiuhrggu0404f48ss'))
        #    , name="ask"
        #    , sign="djfkljvxidfouvjxlbfj"
        #    , classification="skdfjlkfhlxhl"
        #    )
        
        #session.add(ssm)
        session.commit()
        #session.add(StartrekShipModel(
        #    id=str(uuid.uuid5(uuid.NAMESPACE_DNS, 'dmdlsmömlö'))
        #    , name="ask"
        #    , sign="vdölmdyä"
        #    , speed='warp 42.01'
        #)
        
                #ssm = StartrekShipModel(**ship)
        #        print('ship: ' + str(ship))
                #session.add(ship)
    
    else:
        print ('There appears to be data in the DB already :-) ')
    
    

    session.close()

def getShipsFromDB():
    with Session(engine) as session:
        stmt = select(StartrekShipModel)
        res = session.exec(stmt).all()
        ic(res)
    return res

@app.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def ships_table() -> list[AnyComponent]:
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """

    ships = getShipsFromDB()

    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text=f'{len(ships)} Ships', level=2),  # renders `<h2>Ships</h2>`
                c.Table(
                    data=ships,
                    # define theee columns for the table
                    columns=[
                        # the first two cols are rendered as a link to their profile
                        DisplayLookup(field='name', on_click=GoToEvent(url='/ships/{id}/')),
                        DisplayLookup(field='sign', on_click=GoToEvent(url='/ships/{id}/')),
                        DisplayLookup(field='classification')
                    ],
                ),
                c.Div(components=[
                    c.Link(
                        components=[c.Button(text='Add ship')],
                        on_click=GoToEvent(url='/ships/add')
                    )
                ])
            ]
        ),
    ]

@app.post("/api/ships/add")
async def create_ship(form: Annotated[ShipForm, fastui_form(ShipForm)]): # -> FormResponse:
    id = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'name'))
    ship = Ship(id=id, **form.model_dump()) # unpack... (pydantic function) 
    ships.append(ship)
    #return SelectSearchResponse(event=GoToEvent('/'))
    #return FormResponse(event=GoToEvent('/'))


@app.get('/api/ships/add', response_model=FastUI, response_model_exclude_none=True)
def add_ship():
    return [
        c.Page(components=[
            c.Heading(text='Add Ship', level=2),
            c.Paragraph (text='Add new Ship to th list'),
            #c.ModelForm(
            #    type=ShipForm,
            #    submit_url='/api/ships/add',
            #    #status_code=201
            #)
            c.ModelForm(model=ShipForm, submit_url='/api/ships/add') #, success_event=PageEvent(name='form_success')),

        ])
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