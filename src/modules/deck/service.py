from fastapi import HTTPException
from src.modules.deck.models import Deck
from src.modules.deck_slot.models import DeckSlot
from src.modules.user_hero.models import UserHero
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

async def createDeck(
        session,
        id_user,
        id_hero1,
        id_hero2,
        id_hero3,
        id_hero4,
        id_hero5,
        id_hero6):
    
    if (len({id_hero1, id_hero2, id_hero3, id_hero4, id_hero5, id_hero6}) < 4):
        return {"message": "You cannot have duplicate heroes in your deck!"}
    
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

    result = await addHeroDeck(
        session=session,
        id_deck=id_deck,
        id_hero=id_hero1,
        id_user=id_user)
    user_hero_selected.append(result.id)

    result = await addHeroDeck(
        session=session,
        id_deck=id_deck,
        id_hero=id_hero2,
        id_user=id_user)
    user_hero_selected.append(result.id)

    result = await addHeroDeck(
        session=session,
        id_deck=id_deck,
        id_hero=id_hero3,
        id_user=id_user)
    user_hero_selected.append(result.id)

    result = await addHeroDeck(
        session=session,
        id_deck=id_deck,
        id_hero=id_hero4,
        id_user=id_user)
    user_hero_selected.append(result.id)

    result = await addHeroDeck(
        session=session,
        id_deck=id_deck,
        id_hero=id_hero5,
        id_user=id_user)
    user_hero_selected.append(result.id)

    result = await addHeroDeck(
        session=session,
        id_deck=id_deck,
        id_hero=id_hero6,
        id_user=id_user)
    user_hero_selected.append(result.id)

    return user_hero_selected

async def addHeroDeck(
        session,
        id_deck,
        id_user,
        id_hero):
    user_hero = session.query(UserHero).filter(UserHero.hero == id_hero, UserHero.user == id_user).first()

    if not user_hero:
        raise HTTPException(
            status_code=404,
            detail="The user doesn't have this hero on their team!")
    
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

async def listAllDecks(
        session,
        user):
    
    if not getattr(user, "admin", False):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view all decks!")

    decks = session.query(Deck).all()
    return {"Classes": decks}

async def listDeck(session, id_deck, user):
    deck = session.query(Deck).filter(Deck.id == id_deck).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    user_id = user.id if hasattr(user, "id") else user
    is_admin = getattr(user, "admin", False)

    # Corrigido para utilizar a propriedade correta do modelo Deck (.user)
    if deck.user != user_id and not is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
        
    return deck

async def listDecksByUser(
        session,
        user):
    user_id = user.id if hasattr(user, "id") else user
    deck = session.query(Deck).filter(Deck.user == user_id).all()
    return deck

async def listDeckByUser(
        session,
        user,
        id_deck):
    user_id = user.id if hasattr(user, "id") else user
    deck = session.query(Deck).filter(Deck.user == user_id, Deck.id == id_deck).first()
    return deck

async def desativateDeck(
        session,
        id_deck,
        id_user):    
    deck = session.query(Deck).filter(Deck.id == id_deck, Deck.user == id_user).first()

    if not deck:
        raise HTTPException(
            status_code=404,
            detail="Deck not found!")
    
    deck.active = False
    session.commit()
    return {"message": "Deck deactivated successfully!",
            "Deck": deck}

async def activateDeck(
        session,
        id_deck,
        id_user):    
    deck = session.query(Deck).filter(Deck.id == id_deck, Deck.user == id_user).first()

    if not deck:
        raise HTTPException(
            status_code=404,
            detail="Deck not found!")
    
    deck.active = True
    session.commit()
    return {"message": "Deck activated successfully!",
            "Deck": deck}

async def listActiveDecks(
        session,
        user):
    if not getattr(user, "admin", False):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view active decks!")
     
    deck = session.query(Deck).filter(Deck.active == True).all()
    return deck

async def listActiveDecksByUser(
        session,
        user):
    user_id = user.id if hasattr(user, "id") else user
    deck = session.query(Deck).filter(Deck.active == True, Deck.user == user_id).all()
    return deck

async def saveUserDeck(session, user, id_hero1, id_hero2, id_hero3, id_hero4, id_hero5, id_hero6):
    user_id = user.id if hasattr(user, "id") else user

    if (len({id_hero1, id_hero2, id_hero3, id_hero4, id_hero5, id_hero6}) < 4):
        raise HTTPException(status_code=400, detail="You cannot have duplicate heroes in your deck!")

    # Desativa os decks anteriores do usuário para manter apenas o atual ativo
    old_decks = session.query(Deck).filter(Deck.user == user_id, Deck.active == True).all()
    for d in old_decks:
        d.active = False
    session.commit()

    # Cria o novo deck ativo
    new_deck = Deck(user=user_id, active=True, create_date=datetime.now())
    session.add(new_deck)
    session.commit()
    session.refresh(new_deck)

    id_deck = new_deck.id
    heroes = [id_hero1, id_hero2, id_hero3, id_hero4, id_hero5, id_hero6]

    for hero_id in heroes:
        await addHeroDeck(session=session, id_deck=id_deck, id_user=user_id, id_hero=hero_id)

    return {"message": "Deck saved successfully!", "deck_id": id_deck}