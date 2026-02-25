# TIO Music Studio

Local AI music generation studio powered by ACE-Step 1.5, YuE, and DiffRhythm. Runs entirely on your GPU with no per-generation fees.

## Stack

- **Backend**: FastAPI + Celery + Redis + SQLite
- **Frontend**: React + TypeScript + Tailwind CSS + WaveSurfer.js
- **ML Models**: ACE-Step 1.5 (primary), YuE (premium vocals), DiffRhythm (fast instrumentals)
- **LLM**: Claude API for prompt translation (Ollama fallback)

## Requirements

- Python 3.11+
- Node.js 22+
- Redis
- NVIDIA GPU with 12GB+ VRAM (24GB recommended for YuE)
- CUDA 12.x + cuDNN
- ffmpeg

## Quick Start

```bash
# 1. Clone
git clone https://github.com/Joker56156/tio-music-studio.git
cd tio-music-studio

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env      # Edit with your Anthropic API key

# 3. Frontend setup
cd ../frontend
npm install

# 4. Start everything
cd ..
bash start.sh
```

## Development

```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Backend API
cd backend && uvicorn app.main:app --reload --port 8000

# Terminal 3: Celery worker
cd backend && celery -A app.worker.celery_app worker --pool=solo --loglevel=info

# Terminal 4: Frontend
cd frontend && npm run dev
```

## Model Setup

Models download automatically on first use:

| Model | VRAM | Speed | Best For |
|-------|------|-------|----------|
| ACE-Step 1.5 | ~4 GB | <10s/song | General use (default) |
| YuE | ~20 GB | ~6min/30s | Premium vocals |
| DiffRhythm | ~8 GB | ~15s/song | Fast instrumentals |

## Architecture

```
tio-music-studio/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Settings
│   │   ├── database.py          # SQLite via SQLModel
│   │   ├── models/              # DB models (Job, Track)
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── routers/             # API endpoints
│   │   ├── services/            # Business logic
│   │   └── worker/              # Celery tasks
│   ├── outputs/                 # Generated audio
│   └── models/                  # ML model checkpoints
├── frontend/
│   └── src/
│       ├── components/          # React components
│       ├── hooks/               # Custom hooks
│       ├── lib/                 # API client, utilities
│       └── types/               # TypeScript types
├── docker-compose.yml
└── start.sh
```

## License

MIT
