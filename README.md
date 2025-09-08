# Template Full-Stack Web Application
[![.github/workflows/deploy.yml](https://github.com/kosyachniy/web/actions/workflows/deploy.yml/badge.svg)](https://github.com/kosyachniy/web/actions/workflows/deploy.yml)

## Overview
Modern full-stack web application with Python FastAPI backend, Next.js frontend, Telegram bot, and comprehensive monitoring. Built with Docker containers and featuring multilingual support (5 languages), Feature-Sliced Design architecture, and production-ready monitoring.

Form | Side | Stack | Language | Path
---|---|---|---|---
API | Back-end | FastAPI | Python | ``` backend/ ```
Web app | Front-end | React | JavaScript | ``` frontend/ ```
Telegram bot | Back-end | AIOGram | Python | ``` tg/ ```
iOS | Front-end | React Native | JavaScript | planned
Android | Front-end | React Native | JavaScript | planned

## Architecture

### Stack
<table>
    <thead>
        <tr>
            <th>Side</th>
            <th>Logo</th>
            <th>Technology</th>
            <th>Version</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="5" align="center">DevOps</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/docker_logo.png?raw=true" alt="Docker" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/docker_name.png?raw=true" alt="Docker" height="50" /></td>
            <td align="center">20.10.21</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/nginx_logo.png?raw=true" alt="NGINX" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/nginx_name.png?raw=true" alt="NGINX" height="50" /></td>
            <td align="center">1.23</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/letsencrypt_logo.png?raw=true" alt="Let's Encrypt" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/letsencrypt_name.png?raw=true" alt="Let's Encrypt" height="50" /></td>
            <td align="center"></td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/grafana_logo.png?raw=true" alt="Grafana" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/grafana_name.png?raw=true" alt="Grafana" height="50" /></td>
            <td align="center">9.2.5</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/prometheus_logo.png?raw=true" alt="Prometheus" height="50" /></td>
            <td></td>
            <td align="center">2.40.1</td>
        </tr>
        <tr>
            <td rowspan="5" align="center">Back-end</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/python_logo.png?raw=true" alt="Python" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/python_name.png?raw=true" alt="Python" height="50" /></td>
            <td align="center">3.10</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/fastapi_logo.png?raw=true" alt="FastAPI" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/fastapi_name.png?raw=true" alt="FastAPI" height="50" /></td>
            <td align="center">0.87</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/mongodb_logo.png?raw=true" alt="MongoDB" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/mongodb_name.png?raw=true" alt="MongoDB" height="50" /></td>
            <td align="center">6.0</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/redis_logo.png?raw=true" alt="Redis" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/redis_name.png?raw=true" alt="Redis" height="50" /></td>
            <td align="center">7.0</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/socketio_logo.png?raw=true" alt="Socket.IO" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/socketio_name.png?raw=true" alt="Socket.IO" height="50" /></td>
            <td align="center"></td>
        </tr>
        <tr>
            <td rowspan="6" align="center">Front-end</td>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/javascript_logo.png?raw=true" alt="JavaScript" height="50" /></td>
            <td></td>
            <td align="center">node 19.1</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/reactjs_logo.png?raw=true" alt="ReactJS" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/reactjs_name.png?raw=true" alt="ReactJS" height="50" /></td>
            <td align="center">18.2</td>
        </tr>
        <tr>
            <td></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/nextjs_name.png?raw=true" alt="Next.js" height="50" /></td>
            <td align="center">13.0.3</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/redux_logo.png?raw=true" alt="Redux" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/redux_name.png?raw=trueg" alt="Redux" height="50" /></td>
            <td align="center">4.2</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/bootstrap_logo.png?raw=true" alt="Bootstrap" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/bootstrap_name.png?raw=true" alt="Bootstrap" height="50" /></td>
            <td align="center">5.2.1</td>
        </tr>
        <tr>
            <td align="center"><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/ckeditor_logo.png?raw=true" alt="CKEditor" height="50" /></td>
            <td><img src="https://github.com/kosyachniy/dev/blob/main/media/logos/png/ckeditor_name.png?raw=true" alt="CKEditor" height="50" /></td>
            <td align="center">5</td>
        </tr>
    </tbody>
</table>

#### Backend
- **Framework**: FastAPI (async Python web framework)
- **Language**: Python 3.11+ with type hints
- **Database**: MongoDB with custom ConSys ODM library
- **Caching**: Redis for sessions and background tasks
- **Validation**: Pydantic v2 models
- **Logging**: loguru for structured JSON logging
- **Testing**: pytest with async support
- **Package Management**: uv (fast Python installer)
- **Monitoring**: Prometheus metrics collection

#### Frontend
- **Framework**: Next.js 15 (App Router) with React 19
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS + Radix UI (shadcn/ui)
- **State Management**: Redux Toolkit (RTK)
- **Icons**: react-icons (fa6 → bi → hi priority)
- **Internationalization**: next-intl (5 languages: en, es, ru, ar, zh)
- **Architecture**: Feature-Sliced Design (FSD)
- **Quality Tools**: ESLint + TypeScript + Prettier

### Infrastructure
- **Containerization**: Docker with multi-stage builds
- **Web Server**: NGINX reverse proxy
- **SSL**: Let's Encrypt certificates
- **Monitoring**: Prometheus + Grafana dashboards
- **Background Jobs**: Celery with Redis broker

## Key Features
- **Multilingual Support**: 5 languages (English, Spanish, Russian, Arabic, Chinese)
- **Modern UI/UX**: Responsive design with light/dark theme support
- **Feature-Sliced Design**: Scalable frontend architecture with strict import rules
- **API-First**: RESTful API with OpenAPI documentation
- **Real-time Updates**: Socket.IO integration for live data
- **Comprehensive Monitoring**: Prometheus metrics and Grafana dashboards
- **Production Ready**: Docker containers with CI/CD pipeline

## Project Structure
```
web/
├── backend/           # FastAPI Python backend
│   ├── app/          # Main application code
│   ├── models/       # MongoDB models (ConSys ODM)
│   └── routes/       # API endpoints
├── frontend/         # Next.js TypeScript frontend
│   ├── src/app/      # Next.js App Router
│   ├── src/entities/ # Business domain models
│   ├── src/features/ # User-facing functionality
│   ├── src/widgets/  # Complex UI compositions
│   └── src/shared/   # Reusable infrastructure
├── tg/               # Telegram bot (Python)
├── infra/            # Docker configurations
└── data/             # Application data
```

## Quick Start

### Run
[Before starting, you can learn how to configure the server →](https://github.com/kosyachniy/dev/blob/main/server/SERVER.md)

<table>
    <thead>
        <tr>
            <th>local</th>
            <th>prod</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td valign="top">
                1. Configure <code> .env </code> from <code> base.env </code> and add:
                <pre>
# Type
# LOCAL / TEST / DEV / PRE / PROD
MODE=LOCAL<br />

\# Links
PROTOCOL=http
EXTERNAL_HOST=localhost
EXTERNAL_PORT=80
DATA_PATH=./data
                </pre>
            </td>
            <td valign="top">
                1. Configure <code> .env </code> from <code> base.env </code> and add:
                <pre>
\# Type
\# LOCAL / TEST / DEV / PRE / PROD
MODE=PROD

\# Links
PROTOCOL=https
EXTERNAL_HOST=web.kosyachniy.com
WEB_PORT=8201
API_PORT=8202
JOBS_PORT=8203
TG_PORT=8204
DB_PORT=8205
REDIS_PORT=8206
PROMETHEUS_PORT=8207
GRAFANA_PORT=8208
DATA_PATH=~/web/data # or change to global path, for example: ~/data/web
                </pre>
            </td>
        </tr>
        <tr>
            <td>
                2. <code> make dev </code>
            </td>
            <td>
                2. <code> make base <br/> make run </code>
            </td>
        </tr>
        <tr>
            <td>
                3. Open ` http://localhost/ `
            </td>
            <td>
                3. Open ` https://web.kosyachniy.com/ ` (your link)
            </td>
        </tr>
    </tbody>
</table>

### Prerequisites
- Docker and Docker Compose
- Make (for development commands)

### Local Development

1. **Configure environment**:
   ```bash
   # Copy base configuration
   cp base.env .env

   # Add local development settings
   echo "MODE=LOCAL" >> .env
   echo "PROTOCOL=http" >> .env
   echo "EXTERNAL_HOST=localhost" >> .env
   echo "EXTERNAL_PORT=80" >> .env
   echo "DATA_PATH=./data" >> .env
   ```

2. **Start development environment**:
   ```bash
   make up          # Full local development (databases + API + frontend)
   # OR
   make up-base     # Just databases (Redis, MongoDB)
   ```

3. **Frontend development** (optional, for hot reload):
   ```bash
   cd frontend/
   npm install
   npm run dev      # Next.js dev server on http://localhost:3000
   ```

4. **Access the application**:
   - **Frontend**: http://localhost (via nginx proxy)
   - **API**: http://localhost/api/ (backend API)
   - **Direct Frontend**: http://localhost:3000 (if running npm run dev)

### Development Commands

```bash
# Environment Management
make up          # Local: full development environment
make up-dev      # Remote development environment
make up-prod     # Production environment
make up-base     # Infrastructure only (Redis, MongoDB)
make down        # Stop all services
make status      # Check container status

# Testing & Quality
make test          # Run all tests (API + Web)
make test-backend  # Backend tests only
make test-web      # Frontend tests only
make unit-test     # Run pytest unit tests
make lint          # Lint Python code

# Debugging & Monitoring
make shell         # Connect to API container
make db-shell      # Connect to MongoDB
make logs-api      # View API logs
make logs-jobs     # View background jobs logs
make logs-tg       # View Telegram bot logs
```

### Frontend Development

```bash
cd frontend/

npm run dev        # Start Next.js dev server
npm run build      # Build for production
npm run lint       # Run ESLint
```

### API Testing

Test backend endpoints when containers are running:

```bash
# Get categories
curl -X POST http://localhost/api/categories/get/ \
  -H "Content-Type: application/json" \
  -d '{}'

# Get posts with pagination
curl -X POST http://localhost/api/posts/get/ \
  -H "Content-Type: application/json" \
  -d '{"limit": 5, "offset": 0}'
```

## Production Deployment

1. **Configure production environment**:
   ```bash
   cp base.env .env
   # Edit .env with production settings (HTTPS, domain, ports, etc.)
   ```

2. **Deploy**:
   ```bash
   make up-prod
   ```

For detailed configuration and deployment instructions, see [CLAUDE.md](./CLAUDE.md).
