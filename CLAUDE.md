# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### 一键启动（首次）
```bash
make start
# 或
bash start.sh
```

### 后续快速启动
```bash
python manage.py runserver 0.0.0.0:8001
```

### Backend (Django)
```bash
# Install dependencies
pip install -r requirements/base.txt

# Run development server
python manage.py runserver 0.0.0.0:8001

# Run all tests
python manage.py test applications/task applications/music applications/user applications/subsonic

# Run single test file
python manage.py test applications.task.tests

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate --run-syncdb

# Create admin user
python manage.py createsuperuser
```

### Frontend (Vue 2)
```bash
cd web
npm install
npm run dev     # Dev server with hot reload (port 8080)
npm run build   # Production build
npm run lint    # Lint
```

### Docker
```bash
# Build and run (Docker Compose)
docker compose -f local.yml up -d

# Rebuild
docker compose -f local.yml build
```

### Production (Gunicorn)
```bash
gunicorn -w 2 -b 0.0.0.0:8001 django_vue_cli.wsgi:application --timeout 120 --worker-class=gevent
```

## Project Architecture

Music Tag Web is a Django + Vue 2 application for editing music file metadata (ID3 tags, etc.). It runs as a web service that can be deployed alongside music servers like Navidrome.

### High-Level Structure

```
├── django_vue_cli/          # Django project config (settings, urls, wsgi)
├── applications/            # Django apps (business logic)
│   ├── music/               # Music data models (Album, Track, Artist, Genre, etc.)
│   ├── task/                # Core task handlers — file listing, ID3 read/write, batch auto-tag, folder organization, lyrics
│   │   ├── services/        # Music identification & tag sources (acoustid, kugou, kuwo, qq music, netease)
│   │   └── tasks.py         # Sync task functions (scan, batch auto-tag, folder tidy)
│   ├── user/                # User management views
│   └── subsonic/            # Subsonic API implementation (for Navidrome-compatible clients)
├── component/               # Reusable components
│   ├── drf/                 # Custom DRF base classes (viewsets, mixins, pagination, filters, middleware, auth)
│   ├── music_tag/           # Audio tag reading/writing (fork of MusicBrainz Picard's tag layer, built on mutagen)
│   └── mz/                  # Music fingerprint recognition (chromaprint, acoustid)
├── web/                     # Vue 2 frontend (iView UI, Vuex, Vue Router)
│   └── src/
│       ├── views/           # Page components
│       ├── components/      # Shared UI components
│       ├── api/             # Axios API client
│       ├── vuex/            # State management
│       └── router/          # Lazy-loaded route definitions
├── compose/                 # Docker compose configs
│   ├── local/               # Dev Dockerfile + start scripts
│   └── prod/                # Production Dockerfile + start scripts
├── requirements/            # Split requirement files
```

### Key Design Decisions

1. **Custom DRF layer** (`component/drf/`): Extends DRF's `ModelViewSet` and `APIView` with uniform success/failure response formatting, custom pagination (`CustomPageNumberPagination`), custom exception middleware, and JWT auth via `rest_framework_jwt`.

2. **Task-oriented API** (`applications/task/`): The main business logic lives in `TaskViewSets` as DRF `@action` endpoints — file listing, ID3 reading/writing, batch updates, lyrics fetching, folder organization. Long-running operations (scan, batch auto-tag, folder tidy) run synchronously inline without Celery/Redis middleware.

3. **Music identification sources** (`applications/task/services/`): Multiple backends for looking up music metadata — AcoustID (fingerprint), Netease/QQMusic/Kugou/Kuwo (online databases), and smart tag matching.

4. **Subsonic compatibility** (`applications/subsonic/`): Implements enough of the Subsonic API (used by Navidrome, etc.) for media player clients to browse and stream. Custom authentication, content negotiation, and XML/JSON renderers.

5. **Music tag engine** (`component/music_tag/`): A modified fork from MusicBrainz Picard, wrapping mutagen to provide a unified tag interface across FLAC, MP3 (ID3v2), M4A (MP4), OGG Vorbis, APE, WMA/ASF, WAV, AIFF, DSF, etc. Each format has its own module.

6. **No external middleware**: Batch auto-tagging, full scan, and folder organization run inline in the request thread. No Celery, Redis, MySQL, or Nginx required — SQLite + Django dev server or Gunicorn is all you need.

7. **Dual deployment**: The app serves the Vue SPA statically via Django templates in production, while the frontend dev server runs independently on port 8080 for development.

### Database Models (applications/music/)

Key models managed by the music app — these are the core data entities:
- `Album` — album metadata, artist FK, songs count, duration, genre, cover art
- `Track` — per-song data: name, path, artist, album, track number, has_cover_art, file size
- `Artist` — artist name, musicbrainz ID
- `Genre` — genre label
- `Attachment` — uploaded image files (covers, embedded art)
- `Playlist`, `TrackFavorite`, etc.

### API Routes

| Prefix | Source | Purpose |
|--------|--------|---------|
| `/api/` | `task.urls` | Main API — file operations, ID3 editing, batch tagging |
| `/rest/` | `subsonic.urls` | Subsonic-compatible endpoints |
| `/user/` | `user.urls` | User management |
| `/api/token/` | JWT | Obtain/refresh JWT tokens |
| `/admin/` | Django admin | Django admin interface |

### Configuration

- `django_vue_cli/settings.py` — main settings; imports `local_settings.py` if present for local overrides
- Default DB is SQLite (`db.sqlite3`)
- Optional `local_settings.py` (gitignored) for secrets or environment-specific config
- `SITE_LOGIN` env var controls login requirement
