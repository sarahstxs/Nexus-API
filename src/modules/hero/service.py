import os
import httpx
from fastapi import HTTPException
from src.modules.hero.models import Hero
from src.modules.hero_pack.models import HeroPack
from dotenv import load_dotenv

load_dotenv()


async def listAllHeroes(
        meta_personagem: int):
    api_key = os.getenv("API_KEY")
    headers = {"User-Agent": "NexusMarvelTower_v1.0"}
    
    heroes_list = []
    offset = 0
    limit_page = 100
    meta_hero = meta_personagem
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        while len(heroes_list) < meta_hero:
            url_external_api = (
                f"https://comicvine.gamespot.com/api/characters/"
                f"?api_key={api_key}&format=json&limit={limit_page}&offset={offset}"
            )
            
            try:
                awser = await client.get(url_external_api, headers=headers)
            except (httpx.ReadTimeout, httpx.ConnectTimeout):
                raise HTTPException(
                    status_code=504,
                    detail="The external Comic Vine API took too long to respond (Timeout). Please try again later."
                )
            
            if awser.status_code != 200:
                raise HTTPException(
                    status_code=awser.status_code, 
                    detail=f"he external API failed on the page with offset {offset}. Status code: {awser.status_code}"
                )
                
            dados = awser.json()
            results_list = dados.get("results", [])
            
            
            if not results_list:
                break
                
            for hero in results_list:
                publisher_info = hero.get("publisher")
                if publisher_info and isinstance(publisher_info, dict):
                    name_publisher = publisher_info.get("name", "").strip()
                    if name_publisher.lower() == "marvel":
                        heroes_list.append({
                            "nome": hero.get("name"),
                            "resumo": hero.get("deck"),
                            "imagem": hero.get("image", {}).get("original_url"),
                            "editora": name_publisher
                        })
                        
                        if len(heroes_list) >= meta_hero:
                            break
            
            offset += limit_page
            
    if len(heroes_list) == 0:
        return {"message": "No Marvel characters were found in the consulted pages."}
        
    return {
        "total": len(heroes_list),
        "characters": heroes_list
        }

async def listHero(
        session,
        id_hero):
    hero = session.query(Hero).filter(Hero.id == id_hero).first()
    return hero

async def createHero(
        hero_schema_user, 
        session, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to create this hero!")
    
    id = hero_schema_user.id
    active = hero_schema_user.active
    nemesis = hero_schema_user.nemesis
    rarity = hero_schema_user.rarity
    class_hero = hero_schema_user.class_hero
    hyper_attack = hero_schema_user.hyper_attack
    base_atk = hero_schema_user.base_atk
    base_hp = hero_schema_user.base_hp
    base_def = hero_schema_user.base_def

    api_key = os.getenv("API_KEY")
    url = f"https://comicvine.gamespot.com/api/characters/?api_key={api_key}&format=json&filter=id:{id}"
    
    headers = {"User-Agent": "NexusMarvelTower_v1.0"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        awser = await client.get(url, headers=headers)
        
    if awser.status_code != 200:
        raise HTTPException(
            status_code=502, 
            detail="Error fetching data from the external API.")
        
    api_data = awser.json().get("results", [])
    
    if not api_data:
        raise HTTPException(
            status_code=404, 
            detail="Character not found on Comic Vine.")
    
    first_result = api_data[0]

    origin_data = first_result.get("origin") or {}
    first_apperance_data = first_result.get("first_appeared_in_issue") or {}
    image_data = first_result.get("image") or {}
    
    final_hero = {
        "id": id,
        "active": active,
        "name": first_result.get("name"),
        "real_name": first_result.get("real_name"),
        "deck": first_result.get("deck"),
        "gender": first_result.get("gender"),
        "origin": origin_data.get("id"),
        "birth": first_result.get("birth"),
        "appearance": first_result["count_of_issue_appearances"],
        "first_appearance_comic": first_apperance_data.get("name"),
        "image_hero": image_data.get("original_url"),
        "nemesis": nemesis,
        "rarity": rarity,
        "class_hero": class_hero,
        "hyper_attack": hyper_attack,
        "base_atk": base_atk,
        "base_hp": base_hp,
        "base_def": base_def
    }
    new_hero = Hero(**final_hero)

    session.add(new_hero)
    session.commit()
    session.refresh(new_hero)
    return {"message": f"Hero registered successfully!"}
    
async def addHeroPack(
        hero_pack_schema, 
        session, 
        user, 
        id_hero):
    
    if not user.admin:
        raise HTTPException(
            status_code=403, 
            detail="You don't have permission to add a hero to a pack!")
    
    hero = id_hero
    pack = hero_pack_schema.pack
    active = hero_pack_schema.active

    new_hero_pack = {
        "hero": hero,
        "pack": pack,
        "active": active
    }
    final_hero_pack = HeroPack(**new_hero_pack)
    session.add(final_hero_pack)
    session.commit()
    session.refresh(final_hero_pack)
    return {"message": f"Hero registered in the pack successfully!"}

async def desativateHeroPack(
        session, 
        id_hero_pack, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to deactivate this pack!")
    
    hero_pack = session.query(HeroPack).filter(HeroPack.id == id_hero_pack).first()

    if not hero_pack:
        raise HTTPException(
            status_code=404, 
            detail="")
    
    hero_pack.active = False
    session.commit()
    return {"message": "Hero deactivated in the pack successfully!",
            "Pack": hero_pack}

async def activateHeroPack(
        session, 
        id_hero_pack, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to activate this hero!")
    
    hero_pack = session.query(HeroPack).filter(HeroPack.id == id_hero_pack).first()

    if not hero_pack:
        raise HTTPException(
            status_code=404, 
            detail="Hero in pack not found!")
    
    hero_pack.active = True
    session.commit()
    return {"message": "Hero activated in the pack successfully!",
            "Pack": hero_pack}

async def desativateHero(
        session, 
        id_hero, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to deactivate this hero!")
    
    hero = session.query(Hero).filter(Hero.id == id_hero).first()

    if not hero:
        raise HTTPException(
            status_code=404, 
            detail="Hero not found!")
    
    hero.active = False
    session.commit()
    return {"message": "Hero deactivated successfully!",
            "Hero": hero}

async def activateHero(
        session, 
        id_hero, 
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to activate this hero!")
    
    hero = session.query(Hero).filter(Hero.id == id_hero).first()

    if not hero:
        raise HTTPException(
            status_code=404, 
            detail="Hero not found!")
    
    hero.active = True
    session.commit()
    return {"message": "Hero activated successfully!",
            "Hero": hero}

async def listActiveHero(
        session):
    hero = session.query(Hero).filter(Hero.active == True).all()
    return hero

async def listActiveHeroByName(
        session, 
        name_hero):
    hero = session.query(Hero).filter(
        Hero.name.icontains(name_hero),
        Hero.active == True
    ).all()
    
    return hero