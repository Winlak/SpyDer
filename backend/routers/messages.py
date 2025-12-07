from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_session
from backend.schemas.messages import (
    DeletedMessageRead,
    MessageCreate,
    MessageDeleteCreate,
    MessageEditCreate,
    MessageEditRead,
)
from backend.services.messages import create_message, fetch_deleted, fetch_edits, record_delete, record_edit

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/")
async def create(payload: MessageCreate, session: AsyncSession = Depends(get_session)):
    msg = await create_message(session, payload.dict())
    return {"id": msg.id}


@router.post("/edits/")
async def edits(payload: MessageEditCreate, session: AsyncSession = Depends(get_session)):
    edit = await record_edit(session, payload.dict())
    return {"id": edit.id}


@router.post("/deleted/")
async def deleted(payload: MessageDeleteCreate, session: AsyncSession = Depends(get_session)):
    deletion = await record_delete(session, payload.dict())
    return {"id": deletion.id}


@router.get("/deleted", response_model=list[DeletedMessageRead])
async def list_deleted(user_id: int, limit: int = 10, session: AsyncSession = Depends(get_session)):
    deletions = await fetch_deleted(session, user_id=user_id, limit=limit)
    result = []
    for d in deletions:
        result.append(
            {
                "text": d.message.text,
                "chat_id": d.message.chat.chat_id,
                "chat_title": d.message.chat.title,
                "deleted_at": d.deleted_at,
            }
        )
    return result


@router.get("/edited", response_model=list[MessageEditRead])
async def list_edited(user_id: int, limit: int = 10, session: AsyncSession = Depends(get_session)):
    edits = await fetch_edits(session, user_id=user_id, limit=limit)
    result = []
    for e in edits:
        result.append(
            {
                "old_text": e.old_text,
                "new_text": e.new_text,
                "chat_id": e.message.chat.chat_id,
                "chat_title": e.message.chat.title,
                "edited_at": e.edited_at,
            }
        )
    return result
