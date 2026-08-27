from fastapi import APIRouter, Depends, HTTPException
import httpx
from src.modules.class_hero.service import listAllClasses, createClass, desativateClass, listClass, activateClass
from src.modules.user.service import verificate_token
from src.modules.class_hero.schemas import ClassSchema
from sqlalchemy.orm import Session
from src.common.dependencies import get_session

class_routes = APIRouter(prefix="/classes", tags=["classes"])
#
@class_routes.get("/")
async def class_hero():
    return {"mensagem": "Você acessou a rota de classes!"}

@class_routes.get("/list")
async def ListAllClasses(session: Session = Depends(get_session)):
    result = await listAllClasses(session)
    return result

@class_routes.get("/list/{id}")
async def ListClass(id_class: int, session: Session = Depends(get_session)):
    result = await listClass(id_class=id_class, session=session)
    return result

@class_routes.post("/")
async def CreateClass(
    class_hero: ClassSchema, 
    session: Session = Depends(get_session),
    user = Depends(verificate_token) 
    ):
    result = await createClass(class_schema=class_hero, session=session, user=user)
    return result

@class_routes.patch("/desativate/{id}")
async def DesativateClass(id_class: int,
                      session: Session = Depends(get_session),
                      user = Depends(verificate_token) ):
    result = await desativateClass(id_class=id_class, session=session, user=user)
    return result

@class_routes.patch("/activate/{id}")
async def ActivateClass(id_class: int,
                      session: Session = Depends(get_session),
                      user = Depends(verificate_token) ):
    result = await activateClass(id_class=id_class, session=session, user=user)
    return result
