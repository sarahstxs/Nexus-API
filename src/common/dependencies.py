from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker
from src.modules.user.models import User
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from src.core.config import SECRET_KEY, ALGORITHM, oauth2_schema
from src.core.database import db

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificate_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario =int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado! Verifique se o token é válido")
    #Verificar se o token é valido
    # Extrair o ID do usuário do token
    usuario = session.query(User).filter(User.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido!")
    return usuario