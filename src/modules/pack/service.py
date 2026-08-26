import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from src.modules.hero.schemas import HeroSchemaUser
from src.common.dependencies import get_session
from sqlalchemy.orm import Session
from src.modules.pack.models import Pack
from dotenv import load_dotenv

load_dotenv()

async def listAllPacks(session: Session):
    list = session.query(Pack).all()
    return {"Packs": list}