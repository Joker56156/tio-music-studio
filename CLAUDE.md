# TIO Music Studio

## Stack
- Backend: FastAPI + Celery + Redis + SQLite (SQLModel ORM)
- Frontend: Vite + React + TypeScript + Tailwind v4 + shadcn/ui
- ML Models: ACE-Step 1.5 (primary), YuE (vocals), DiffRhythm (fast variations)
- LLM: Claude API (Sonnet 4.5) for prompt translation, Ollama fallback

## Commands
- Backend: `cd backend && uvicorn app.main:app --reload --port 8000`
- Worker: `celery -A app.worker.celery_app worker --pool=solo --loglevel=info`
- Frontend: `cd frontend && npm run dev`
- Redis: `redis-server`

## IMPORTANT
- Celery MUST use --pool=solo (CUDA cannot survive fork())
- Worker concurrency MUST be 1 (single GPU)
- Use torch.inference_mode() not torch.no_grad()
- All model loading happens in worker process, NOT in FastAPI
- SQLite needs connect_args={"check_same_thread": False}
- Audio served via FileResponse (not StreamingResponse) for seeking support
