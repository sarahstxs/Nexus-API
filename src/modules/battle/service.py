from fastapi import HTTPException
from src.modules.battle.models import Battle
from datetime import datetime
from fastapi import HTTPException
import random
from typing import List
from src.modules.user_hero.models import UserHero
from src.modules.place.models import Place
from src.modules.battle.schemas import BattleActionSchema

async def createBattle(
        session,
        id_deck,
        id_user,
        id_active_tower_run,
        battle_schema):
    date = datetime.now()
    floor_reached = id_active_tower_run
    deck = id_deck
    result = battle_schema.result
    user = id_user

    new_battle = {
        "date": date,
        "floor_reached": floor_reached,
        "deck": deck,
        "result": result,
        "user": user
    }
    final_battle = Battle(**new_battle)
    session.add(final_battle)
    session.commit()
    session.refresh(final_battle)

    return {"message": "Battle registered successfully!"}

async def listAllBattles(
        session,
        user):
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to deactivate this battle!")

    list = session.query(Battle).all()
    return {"Battles": list}

async def listBattle(
        session,
        id_battle,
        user):
    
    if not user.admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to list this battle!")
    
    battle = session.query(Battle).filter(Battle.id == id_battle).first()
    return battle

async def listBattlesByUser(
        session,
        user):
    battle = session.query(Battle).filter(Battle.user == user.id).all()
    return battle

async def listBattleByUser(
        session,
        user,
        id_battle):
    battle = session.query(Battle).filter(Battle.user == user.id, Battle.id == id_battle).first()
    return battle

async def startBattle(session, user_id, floor: int, place_id: int, deck_hero_ids: List[int]):
    # 1. Carrega o Local (Place) para o plano de fundo e bônus de origem
    place = session.query(Place.id, Place.name, Place.image, Place.effect).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    # 2. Valida e carrega exatamente os 6 heróis do deck do usuário
    if len(deck_hero_ids) != 6:
        raise HTTPException(status_code=400, detail="You must select exactly 6 heroes for battle!")

    user_heroes = session.query(UserHero).filter(UserHero.id.in_(deck_hero_ids), UserHero.user == user_id).all()
    if len(user_heroes) != 6:
        raise HTTPException(status_code=400, detail="Some selected heroes were not found on your account!")

    # 3. Gera os Inimigos com base no Andar (Floor) (Chefes a cada 5 andares ou equipes de 6 inimigos)
    is_boss_floor = (floor % 5 == 0)
    enemies = generate_enemies(floor, is_boss_floor)

    return {
        "floor": floor,
        "is_boss": is_boss_floor,
        "place": {
            "name": place.name,
            "image": place.image,
            "effect": place.effect
        },
        "player_team": [
            {
                "id": h.id,
                "hero_id": h.hero,
                "current_hp": h.current_hp,
                "max_hp": h.max_hp,
                "energy": 0, # Começa com 0 de energia para a habilidade suprema
                "alive": h.alive
            } for h in user_heroes
        ],
        "enemy_team": enemies
    }

def generate_enemies(floor: int, is_boss: bool):
    multiplier = 1 + (floor * 0.12)
    if is_boss:
        return [
            {"name": f"Tower Boss Floor {floor}", "hp": int(800 * multiplier), "max_hp": int(800 * multiplier), "attack": int(70 * multiplier)}
        ]
    else:
        # Gera uma equipe inimiga proporcional de até 6 oponentes comuns
        num_enemies = min(6, 3 + (floor // 3))
        return [
            {
                "name": f"Enemy Guard {i+1}", 
                "hp": int(180 * multiplier), 
                "max_hp": int(180 * multiplier), 
                "attack": int(20 * multiplier)
            } for i in range(num_enemies)
        ]

async def processTurn(session, user_id, action: BattleActionSchema, current_battle_state: dict):
    hero_id = action.user_hero_id
    action_type = action.action_type
    target_idx = action.target_enemy_index
    
    enemies = current_battle_state["enemy_team"]
    players = current_battle_state["player_team"]

    # Valida alvo inimigo
    if target_idx >= len(enemies) or enemies[target_idx]["hp"] <= 0:
        raise HTTPException(status_code=400, detail="Invalid or dead target!")

    target_enemy = enemies[target_idx]
    log_messages = []

    # Processa ação do herói do jogador
    if action_type == "basic":
        damage = 35
        target_enemy["hp"] -= damage
        log_messages.append(f"Seu herói atacou {target_enemy['name']} causando {damage} de dano!")
    elif action_type == "special":
        damage = 70
        target_enemy["hp"] -= damage
        log_messages.append(f"Habilidade Especial usada em {target_enemy['name']} ({damage} de dano)!")
    elif action_type == "ultimate":
        damage = 130
        target_enemy["hp"] -= damage
        log_messages.append(f"HABILIDADE SUPREMA! {damage} de dano em {target_enemy['name']}!")
    elif action_type == "defend":
        log_messages.append("Herói em posição defensiva!")

    # Verifica se o inimigo alvo foi derrotado
    if target_enemy["hp"] <= 0:
        target_enemy["hp"] = 0
        log_messages.append(f"{target_enemy['name']} foi derrotado!")

    # Turno de retaliação dos inimigos vivos contra os 6 heróis do jogador
    for enemy in enemies:
        if enemy["hp"] > 0:
            alive_players = [p for p in players if p["alive"]]
            if alive_players:
                defending_player = random.choice(alive_players)
                dmg_dealt = enemy["attack"]
                defending_player["current_hp"] -= dmg_dealt
                if defending_player["current_hp"] <= 0:
                    defending_player["current_hp"] = 0
                    defending_player["alive"] = False
                    log_messages.append(f"{enemy['name']} atacou e eliminou um herói do seu time!")
                else:
                    log_messages.append(f"{enemy['name']} causou {dmg_dealt} de dano ao seu time.")

    # Condições de fim de turno (vitória ou derrota)
    all_enemies_dead = all(e["hp"] <= 0 for e in enemies)
    all_players_dead = all(not p["alive"] for p in players)

    status = "ongoing"
    if all_enemies_dead:
        status = "victory"
    elif all_players_dead:
        status = "defeat"

    return {
        "battle_state": current_battle_state,
        "logs": log_messages,
        "status": status
    }