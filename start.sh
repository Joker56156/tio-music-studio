#!/bin/bash
# TIO Music Studio — Local launcher
set -e

echo "======================================="
echo "  TIO Music Studio"
echo "======================================="

# Check GPU
if command -v nvidia-smi &>/dev/null; then
    echo ""
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    echo ""
fi

# Check Python
if ! command -v python &>/dev/null; then
    echo "ERROR: Python not found. Install Python 3.11+."
    exit 1
fi

# Check Redis
if ! command -v redis-server &>/dev/null; then
    echo "ERROR: Redis not found. Install Redis."
    exit 1
fi

# Activate virtual environment if it exists
if [ -f "backend/venv/bin/activate" ]; then
    source backend/venv/bin/activate
elif [ -f "backend/venv/Scripts/activate" ]; then
    source backend/venv/Scripts/activate
fi

# Start Redis
redis-server --daemonize yes 2>/dev/null || true
echo "[OK] Redis"

# Start Celery worker (MUST use --pool=solo for CUDA)
cd backend
celery -A app.worker.celery_app worker --pool=solo --loglevel=info &
CELERY_PID=$!
echo "[OK] Celery worker (PID: $CELERY_PID)"

# Start FastAPI
uvicorn app.main:app --host 127.0.0.1 --port 8000 &
API_PID=$!
echo "[OK] FastAPI at http://localhost:8000"
cd ..

# Start frontend
cd frontend
if [ -d "dist" ]; then
    npx serve -s dist -l 3000 &
else
    npx vite --port 3000 &
fi
FRONTEND_PID=$!
echo "[OK] Frontend at http://localhost:3000"
cd ..

# Graceful shutdown
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $CELERY_PID $API_PID $FRONTEND_PID 2>/dev/null
    redis-cli shutdown 2>/dev/null || true
    echo "All services stopped."
}
trap cleanup SIGINT SIGTERM

echo ""
echo "======================================="
echo "  TIO Music Studio is running!"
echo "  App:     http://localhost:3000"
echo "  API:     http://localhost:8000/docs"
echo "  Press Ctrl+C to stop."
echo "======================================="
echo ""
wait
