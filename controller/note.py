from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from controller.auth.auth import get_user
from db.db import get_db
from model.note import Note
from schema.note import NoteSchema

router = APIRouter()


@router.get("/store", response_model=NoteSchema)
async def store(note: NoteSchema, db: Session = Depends(get_db), user_id: int = Depends(get_user)):
    db_note = Note(title=note.title, content=note.content, user_id=user_id, visibility=note.visibiliy)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.get("/notes/", response_model=List[NoteSchema])
async def note_index(db: Session = Depends(get_db), user_id: int = Depends(get_user)):
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    return notes

@router.get("/notes/{note_id}", response_model=NoteSchema)
async def note_show(note_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_user)):
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    return db_note


@router.patch("/notes/{note_id}", response_model=NoteSchema)
async def note_update(note_id: int, note: NoteSchema, db: Session = Depends(get_db), user_id: int = Depends(get_user)):
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note non trouvée")

    db_note.title = note.title
    db_note.content = note.content
    db_note.visibility = note.visibility
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/notes/{note_id}", response_model=NoteSchema)
async def note_destroy(note_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_user)):
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="La note n'existe pas")
    db.delete(db_note)
    db.commit()
    return db_note