from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.deck.service import createDeck
from src.modules.user.service import verificate_token
from src.modules.class_hero.schemas import ClassSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session

deck_routes = APIRouter(prefix="/decks", tags=["decks"])
#
@deck_routes.get("/")
async def deck():
    return {"mensagem": "Você acessou a rota de Decks!"}

@deck_routes.post("/")
async def CreateDeck(id_user: int,
                     id_hero1: int,
                     id_hero2: int,
                     id_hero3: int,
                     id_hero4: int,
                     session: Session = Depends(get_session)):
    result = await createDeck(id_user=id_user,
                             id_hero1=id_hero1,
                             id_hero2=id_hero2,
                             id_hero3=id_hero3,
                             id_hero4=id_hero4,
                             session=session)
    return result