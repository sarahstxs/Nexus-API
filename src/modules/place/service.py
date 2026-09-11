from fastapi import HTTPException
from src.modules.place.models import Place
from dotenv import load_dotenv

load_dotenv()

async def listAllPlaces(
        session):
    list = session.query(Place).all()
    return {"Places": list}

async def createPlace(
        session, 
        place_schema, 
        user):

    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to create places!")
    
    name = place_schema.name
    image = place_schema.image
    effect = place_schema.effect
    active = place_schema.active

    new_place = {
        "name": name,
        "image": image,
        "effect": effect,
        "active": active
    }
    
    final_place = Place(**new_place)
    session.add(final_place)
    session.commit()
    session.refresh(final_place)
    return {"message": f"Place registered successfully!"}

async def desativatePlace(
        session, 
        id_place, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to deactivate this place!")
    
    place = session.query(Place).filter(Place.id == id_place).first()

    if not place:
        raise HTTPException(
            status_code=404, 
            detail="Place not found!")
    
    place.active = False
    session.commit()
    return {"message": "Place deactivated successfully!",
            "Place": place}

async def activatePlace(
        session, 
        id_place, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to activate this place!")
    
    place = session.query(Place).filter(Place.id == id_place).first()

    if not place:
        raise HTTPException(
            status_code=404, 
            detail="Place not found!")
    
    place.active = True
    session.commit()
    return {"message": "Place activated successfully!",
            "Place": place}

async def listPlace(
        session, 
        id_place):
    place = session.query(Place).filter(Place.id == id_place).first()
    return place

async def listActivePlace(
        session):
    place = session.query(Place).filter(Place.active == True).all()
    return {"Place": place}

async def listActivePackByName(
        session, 
        name_place):
    place = session.query(Place).filter(
        Place.name.icontains(name_place),
        Place.active == True
    ).all()
    
    return place