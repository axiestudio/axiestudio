# 🚀 Simple Local Development Setup

## Quick Start (Docker)

```bash
# 1. Clone and navigate
git clone https://github.com/axiestudio/axiestudio.git
cd axiestudio

# 2. Build and run with Docker
docker-compose up --build

# 3. Access Axie Studio
# Open: http://localhost:7860
# Login required (no auto-login)
# Default admin: admin@axiestudio.se / change-this-password
```

## Development Setup (Local)

### Prerequisites
- Python 3.12+
- Node.js 18+
- UV package manager

### Backend Setup
```bash
# Install dependencies
uv sync --extra postgresql

# Run backend
uv run axiestudio run --host 0.0.0.0 --port 7860
```

### Frontend Setup (Separate Terminal)
```bash
cd src/frontend
npm install
npm start
# Frontend runs on http://localhost:3000
```

## Environment Variables

Create `.env` file:
```bash
AXIESTUDIO_SECRET_KEY=your-secret-key
AXIESTUDIO_AUTO_LOGIN=false
AXIESTUDIO_NEW_USER_IS_ACTIVE=false
AXIESTUDIO_SUPERUSER=admin@axiestudio.se
AXIESTUDIO_SUPERUSER_PASSWORD=your-password
DATABASE_URL=sqlite:///./axiestudio.db
```

## Key Features Confirmed ✅

- ❌ **No Auto-Login** - Users must authenticate
- ❌ **No Anonymous Access** - Login required
- ❌ **No Frontend Signup** - Admin creates users
- ✅ **Axie Studio Branding** - Complete rebrand from Langflow
- ✅ **Docker Ready** - Full containerization support

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 7860
lsof -ti:7860 | xargs kill -9
```

### Database Issues
```bash
# Reset database
rm axiestudio.db
uv run axiestudio run
```
