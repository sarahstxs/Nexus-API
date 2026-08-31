import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.modules.deck.schemas import DeckSchema
from src.modules.deck_slot.schemas import DeckSlotSchema
from src.common.dependencies import get_session
from sqlalchemy.orm import Session
from src.modules.deck.models import Deck
from src.modules.deck_slot.models import DeckSlot
from src.modules.user_hero.models import UserHero
from src.modules.hero_pack.models import HeroPack
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

async def createDeck(session, id_user, id_hero1, id_hero2, id_hero3, id_hero4):
    if (len({id_hero1, id_hero2, id_hero3, id_hero4}) < 4):
        return {"mensagem": "Você não pode ter heróis repetidos no seu deck!"}
    
    create_date = datetime.now()
    user = id_user
    active = True

    new_deck = {
        "create_date": create_date,
        "user": user,
        "active": active
    }
    final_deck = Deck(**new_deck)
    session.add(final_deck)
    session.commit()
    session.refresh(final_deck)

    id_deck = final_deck.id
    
    user_hero_selected = []

    result = await addHeroDeck(session=session, id_deck=id_deck, id_hero=id_hero1, id_user=id_user)
    user_hero_selected.append(result.user_hero)

    result = await addHeroDeck(session=session, id_deck=id_deck, id_hero=id_hero2, id_user=id_user)
    user_hero_selected.append(result.user_hero)

    result = await addHeroDeck(session=session, id_deck=id_deck, id_hero=id_hero3, id_user=id_user)
    user_hero_selected.append(result.user_hero)

    result = await addHeroDeck(session=session, id_deck=id_deck, id_hero=id_hero4, id_user=id_user)
    user_hero_selected.append(result.user_hero)


    return user_hero_selected

async def addHeroDeck(session, id_deck, id_user, id_hero):
    user_hero = session.query(UserHero).filter(UserHero.hero == id_hero, UserHero.user == id_user).first()

    if not user_hero:
        raise HTTPException(status_code=404, detail="O usuário não tem esse herói em seu time!")
    
    user_hero_slot = user_hero.id
    deck = id_deck
    
    new_deck_slot = {
        "user_hero": user_hero_slot,
        "deck": deck,
        "active": True
    }
    final_deck_slot = DeckSlot(**new_deck_slot)
    session.add(final_deck_slot)
    session.commit()
    session.refresh(final_deck_slot)
    return user_hero