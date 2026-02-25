import json
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from ..database import get_session
from ..models.track import Track

router = APIRouter()


@router.get("/tracks")
async def list_tracks(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    favorites_only: bool = Query(default=False),
    session: Session = Depends(get_session),
):
    query = select(Track).order_by(Track.created_at.desc())
    if favorites_only:
        query = query.where(Track.is_favorite == True)
    query = query.offset(offset).limit(limit)

    tracks = session.exec(query).all()

    return [
        {
            **track.model_dump(exclude={"peaks_json"}),
            "peaks": json.loads(track.peaks_json) if track.peaks_json else None,
            "audio_url": f"/api/audio/{track.id}",
        }
        for track in tracks
    ]


@router.get("/tracks/{track_id}")
async def get_track(track_id: str, session: Session = Depends(get_session)):
    track = session.get(Track, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    return {
        **track.model_dump(exclude={"peaks_json"}),
        "peaks": json.loads(track.peaks_json) if track.peaks_json else None,
        "audio_url": f"/api/audio/{track.id}",
    }


@router.patch("/tracks/{track_id}")
async def update_track(
    track_id: str,
    title: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    session: Session = Depends(get_session),
):
    track = session.get(Track, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    if title is not None:
        track.title = title
    if is_favorite is not None:
        track.is_favorite = is_favorite

    session.add(track)
    session.commit()
    session.refresh(track)

    return track


@router.delete("/tracks/{track_id}")
async def delete_track(track_id: str, session: Session = Depends(get_session)):
    track = session.get(Track, track_id)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    session.delete(track)
    session.commit()

    return {"ok": True}
