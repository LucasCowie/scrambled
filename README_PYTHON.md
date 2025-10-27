# Scrambled - Python Version

This is the Python conversion of the Scrambled automation server with Discord bot and REST API.

## About

An automation server that interfaces with Discord and other services:

- Discord bot using discord.py
- FastAPI REST API
- WebSocket data via Socket.IO
- MongoDB database integration
- Spotify & Twitch integrations

## Tech Stack

**Python Version**: 3.9+

**Key Dependencies**:
- `discord.py` - Discord bot framework
- `FastAPI` - Modern web framework for REST API
- `motor` - Async MongoDB driver
- `python-socketio` - WebSocket support
- `aiohttp` - Async HTTP client

## Setup

### 1. Create Virtual Environment

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

### 4. Run the Applications

**Start the Discord Bot:**
```bash
python bot/client.py
```

**Start the Web Server:**
```bash
python server/app.py
```

**Or use uvicorn directly:**
```bash
uvicorn server.app:socket_app --host 0.0.0.0 --port 3000 --reload
```

## REST API

| Method | Endpoint              | Returns | Purpose                                    |
| ------ | --------------------- | ------- | ------------------------------------------ |
| GET    | /api/spotify          | JSON    | Currently playing track on Spotify         |
| GET    | /api/twitch           | JSON    | Creator information                        |
| GET    | /api/twitch/ads       | JSON    | Ad schedule information                    |
| GET    | /api/twitch/followers | JSON    | Collection of follower objects             |
| GET    | /api/messages         | JSON    | Collection of message objects              |
| GET    | /api/messages/:author | JSON    | Messages by the provided author            |
| GET    | /api/message/:id      | JSON    | A single message object                    |
| POST   | /api/message          | JSON    | Create a new message                       |
| DELETE | /api/message/:id      | STATUS  | Delete a single message by id              |
| DELETE | /api/messages/:author | STATUS  | Delete all messages by a single author     |

Every endpoint requires a `token` either in request body or query params. This token is set in the `.env` file as `SCRAMBLED`.

## Project Structure

```
scrambled-dev/
├── bot/
│   ├── commands/        # Discord slash commands
│   ├── events/          # Discord event handlers
│   ├── helpers/         # Helper utilities
│   ├── daemons/         # Background tasks
│   └── client.py        # Bot entry point
├── server/
│   ├── controllers/     # API route handlers
│   │   └── database/    # Database operations
│   ├── models/          # Pydantic/MongoDB models
│   ├── public/          # Static files
│   ├── app.py           # FastAPI application
│   └── router.py        # API routes
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

## Differences from JavaScript Version

1. **Discord.py vs Discord.js**: Uses cogs pattern for commands/events instead of file-based loading
2. **FastAPI vs Express**: Modern async Python framework with automatic API documentation
3. **Motor vs Mongoose**: Async MongoDB driver for Python
4. **Type Hints**: Python version includes type annotations for better code quality
5. **Async/Await**: Fully async implementation throughout

## Development

**Auto-reload during development:**

Bot:
```bash
# Install watchdog for file watching
pip install watchdog

# Run with auto-reload
watchmedo auto-restart --patterns="*.py" --recursive -- python bot/client.py
```

Server:
```bash
uvicorn server.app:socket_app --reload
```

## API Documentation

FastAPI provides automatic interactive API documentation:
- Swagger UI: `http://localhost:3000/docs`
- ReDoc: `http://localhost:3000/redoc`

## Notes

- Make sure MongoDB is running and accessible
- Update `.env` with all required tokens and credentials
- The bot requires proper Discord application setup with slash commands
- Some features from the JS version (calendar monitoring, etc.) are marked as TODO and need implementation

## License

MIT
