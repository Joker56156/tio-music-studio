import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session

from ..database import get_session
from ..models.track import Track

router = APIRouter()


@router.get("/audio/{track_id}")
async def serve_audio(track_id: str, session: Session = Depends(get_session)):
    track = session.get(Track, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    if not os.path.exists(track.file_path):
        raise HTTPException(status_code=404, detail="Audio file not found on disk")

    media_type = "audio/mpeg" if track.format == "mp3" else f"audio/{track.format}"

    return FileResponse(
        path=track.file_path,
        media_type=media_type,
        filename=f"{track.title}.{track.format}",
    )
