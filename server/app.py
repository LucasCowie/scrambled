"""FastAPI server application for Scrambled."""

import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import socketio
from motor.motor_asyncio import AsyncIOMotorClient

from router import router as api_router

load_dotenv()

# Create FastAPI app
app = FastAPI(title="Scrambled API", version="0.1.2")

# Create Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# MongoDB connection
mongo_client = AsyncIOMotorClient(os.getenv('DB_URI'))
db = mongo_client.get_database()

# Store database in app state
app.state.db = db
app.state.sio = sio

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
static_path = Path(__file__).parent / 'public'
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Routes for static resources
@app.get('/favicon.ico')
async def favicon():
    """Serve favicon."""
    return FileResponse(Path(__file__).parent / 'public' / 'resources' / 'favicon.ico')

@app.get('/resources/vendor/socket.io.js')
async def socketio_js():
    """Serve Socket.IO client library."""
    # Socket.IO client would be served from CDN or custom location
    raise HTTPException(status_code=404, detail="Use Socket.IO CDN")

# API routes
app.include_router(api_router, prefix='/api')

# 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors."""
    return {"error": "404 Not Found!", "status": 404}

# General error handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    return {"error": str(exc), "status": 500}

# Socket.IO events
@sio.event
async def connect(sid, environ):
    """Handle client connection."""
    print(f'[fastapi] >> [socket.io] A new client connection occurred: {sid}')

@sio.event
async def disconnect(sid):
    """Handle client disconnection."""
    print(f'[fastapi] >> [socket.io] Client disconnected: {sid}')

@sio.on('scrambled-stage.spotify-pong')
async def handle_spotify_pong(sid, data):
    """Handle Spotify pong event."""
    print(f'[socket.io] Spotify pong: {data}')

if __name__ == '__main__':
    import uvicorn
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 3000))
    
    print(f'[fastapi] Available at http://{host}:{port}')
    
    # Start server
    uvicorn.run(
        socket_app,
        host=host,
        port=port,
        log_level='info'
    )
