import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.modules.hero.schemas import HeroSchemaUser
from src.common.dependencies import get_session
from sqlalchemy.orm import Session
from src.modules.hero.models import Hero
from dotenv import load_dotenv

load_dotenv()


async def listAllHeroes(meta_personagem: int):
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
                    detail="A API externa da Comic Vine demorou muito para responder (Timeout). Tente novamente mais tarde."
                )
            
            if awser.status_code != 200:
                raise HTTPException(
                    status_code=awser.status_code, 
                    detail=f"A API externa falhou na página com offset {offset}. Código: {awser.status_code}"
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
        return {"mensagem": "Nenhum personagem da Marvel foi encontrado nas páginas consultadas."}
        
    return {
        "total": len(heroes_list),
        "personagens": heroes_list
        }

async def createHero(hero_schema_user: HeroSchemaUser, session: Session = Depends(get_session)):
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
        raise HTTPException(status_code=502, detail="Erro ao buscar dados na API externa.")
        
    api_data = awser.json().get("results", [])
    
    if not api_data:
        raise HTTPException(status_code=404, detail="Personagem não encontrado na Comic Vine.")
    
    # o primeiro resultado que a API achou
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
    return {"mensagem": f"Herói cadastrado com sucesso "}
    