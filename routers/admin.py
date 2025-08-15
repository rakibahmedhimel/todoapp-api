from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Todos
from .auth import get_current_user
from typing import Annotated

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

def get_db():
    db = SessionLocal()
    try : 
        yield db 
    finally:
        db.close()

db_dep = Annotated[Session , Depends(get_db)]
user_dep = Annotated[dict, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_dep, db:db_dep):
    
    if user is None or user.get('user_role')!="admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    return db.query(Todos).all()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dep, db: db_dep, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(todo_model)
    db.commit()