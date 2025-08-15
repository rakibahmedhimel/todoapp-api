from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Todos
from .auth import get_current_user
from typing import Annotated

router = APIRouter()

def get_db():
    db = SessionLocal()
    try : 
        yield db 
    finally:
        db.close()

db_dep = Annotated[Session , Depends(get_db)]
user_dep = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=3, max_length=100)
    priority : int = Field(gt=0, lt=6)
    complete : bool

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dep, db : db_dep):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).filter(Todos.owner_id==user.get('user_id')).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(user:user_dep, db:db_dep, todo_id:int=Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found")
    return todo_model

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dep, db : db_dep, todo_request : TodoRequest):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    new_todo = Todos(**todo_request.model_dump(), owner_id=user.get('user_id'))

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)


@router.put("/update_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dep, db : db_dep, todo_update : TodoRequest, todo_id : int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = db.query(Todos).filter(todo_id == Todos.id).filter(Todos.owner_id==user.get('id')).first()
    if not todo_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    todo_model.title = todo_update.title
    todo_model.description = todo_update.description
    todo_model.complete = todo_update.complete
    todo_model.priority = todo_update.priority

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dep, db: db_dep, todo_id : int = Path(gt=0)):
    db_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('id')).first()
    if not db_model:
        raise HTTPException(status_code=404, detail="Task Not Found.")
    db.delete(db_model)
    db.commit()
