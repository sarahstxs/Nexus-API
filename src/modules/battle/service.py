from fastapi import HTTPException
from src.modules.battle.models import Battle
from datetime import datetime
from src.modules.user_hero.models import UserHero
from src.modules.place.models import Place
from src.modules.user.models import User

from typing import List

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
    print(f"\n--- INÍCIO DA BATALHA ---")
    print(f"User ID autenticado: {user_id}")
    print(f"IDs dos heróis recebidos do Android: {deck_hero_ids}")

    # 1. Carrega o Local (Place) para o fundo da batalha
    place = session.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    # 2. Valida se vieram 6 IDs
    if len(deck_hero_ids) != 6:
        raise HTTPException(status_code=400, detail="You must select exactly 6 heroes for battle!")

    # 3. Procura os heróis na base de dados
    # ATENÇÃO: Se na tua model UserHero o campo de relacionamento/FK do utilizador se chamar 'user_id' 
    # em vez de 'user', deves alterar para: UserHero.user_id == user_id
    user_heroes = session.query(UserHero).filter(
        UserHero.hero.in_(deck_hero_ids), 
        UserHero.user == user_id  # Altere para UserHero.user_id se necessário
    ).all()

    found_ids = [h.id for h in user_heroes]
    print(f"IDs encontrados na BD para este utilizador: {found_ids}")

    if len(user_heroes) != 6:
        missing_ids = [hid for hid in deck_hero_ids if hid not in found_ids]
        print(f"⚠️ ERRO: Os seguintes IDs enviados não pertencem ao user_id {user_id} ou não existem: {missing_ids}")
        raise HTTPException(
            status_code=400, 
            detail=f"Alguns heróis não foram encontrados na sua conta (IDs em falta: {missing_ids})"
        )

    # 4. Carrega o utilizador para atualizar o nível e recompensas
    user = session.query(User).filter(User.id == user_id).first()

    # 5. Calcula o Poder Total da Equipa
    player_power = 0
    for h in user_heroes:
        hp = getattr(h, 'max_hp', getattr(h, 'hp', 100))
        atk = getattr(h, 'attack', 10)
        player_power += hp + (atk * 3)

    # 6. Calcula o Poder do Inimigo com base no Andar (Chefes a cada 5 andares)
    is_boss = (floor % 5 == 0)
    enemy_power = 100 + (floor * 150)
    if is_boss:
        enemy_power = int(enemy_power * 1.5)

    # 7. Compara os poderes para definir o resultado
    is_victory = player_power >= enemy_power

    # 8. Se vencer, atualiza o nível e moedas na base de dados
    if is_victory and user:
    
    # CORRIGIDO: Verificar 'current_level' em vez de 'level'
        if hasattr(user, 'current_level'):
            print("Entrou no level")
            user.current_level += 1
        
        # Garante que o highest_level também existe antes de comparar
            if hasattr(user, 'highest_level') and user.current_level > user.highest_level:
                user.highest_level = user.current_level
                print("Entrou no mais")
            
        if hasattr(user, 'coins'):
            print("Entrou no coins")
            user.coins += (floor * 50) 
        
        session.commit()
        session.refresh(user)

        print(f"Resultado: {'Vitória' if is_victory else 'Derrota'} (Equipa: {player_power} vs Inimigo: {enemy_power})\n")

    return {
        "floor": floor,
        "is_boss": is_boss,
        "place": {
            "name": getattr(place, 'name', 'Torre de Desafio'),
            "image": getattr(place, 'image', ''),
            "effect": getattr(place, 'effect', None)
        },
        "player_power": player_power,
        "enemy_power": enemy_power,
        "status": "victory" if is_victory else "defeat",
        "message": "🎉 Vitória! Subiu de nível e superou o andar." if is_victory else "💀 Derrota! O inimigo era demasiado forte para este deck."
    }