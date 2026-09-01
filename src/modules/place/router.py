from fastapi import APIRouter, Depends
from src.modules.place.service import listActivePackByName, listActivePlace, listAllPlaces, listPlace, activatePlace, desativatePlace, createPlace
from src.modules.user.service import verificate_token
from src.modules.place.schemas import PlaceSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session

place_routes = APIRouter(prefix="/places", tags=["places"])

@place_routes.get("/")
async def place():
    return {"mensagem": "Você acessou a rota de Lugares!"}

@place_routes.get("/list")
async def ListAllPlaces(
    session: Session = Depends(get_session)
    ):
    result = await listAllPlaces(
        session)
    return result

@place_routes.get("/list/{id}")
async def ListPlace(
    id_place: int, 
    session: Session = Depends(get_session)
    ):
    result = await listPlace(
        id_place=id_place, 
        session=session)
    return result

@place_routes.get("/list-active")
async def ListActivePlace(
    session: Session = Depends(get_session)
    ):
    result = await listActivePlace(
        session=session)
    return result

@place_routes.get("/list-active-name/{name_place}")
async def ListActivePlaceByName(
    name_place: str, 
    session: Session = Depends(get_session)
    ):
    result = await listActivePackByName(
        session=session, 
        name_place=name_place)
    return result

@place_routes.post("/")
async def CreatePlace(
    place_schema: PlaceSchema, 
    session: Session = Depends(get_session),
    user = Depends(verificate_token) 
    ):
    result = await createPlace(
        place_schema=place_schema, 
        session=session, 
        user=user)
    return result

@place_routes.patch("/desativate/{id}")
async def DesativatePlace(
    id_place: int,
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await desativatePlace(
        id_place=id_place, 
        session=session, 
        user=user)
    return result

@place_routes.patch("/activate/{id}")
async def ActivatePlace(
    id_place: int,
    session: Session = Depends(get_session),
    user = Depends(verificate_token)
    ):
    result = await activatePlace(
        id_place=id_place, 
        session=session, 
        user=user)
    return result