# pgpyfatovutwls

> Full-stack production-ready boilerplate with PostgreSQL, Python, FastAPI, Tortoise ORM, Vue, TailwindCSS, and Lemon Squeezy

A modern, scalable web application boilerplate that provides authentication, subscription management, monitoring, and internationalization out of the box.

## 🚀 Features

- **Backend**: FastAPI with async support, Tortoise ORM, PostgreSQL
- **Frontend**: Vue 3, Vite, TailwindCSS, responsive design
- **Authentication**: JWT-based authentication with email verification
- **Subscriptions**: Lemon Squeezy integration for payment processing
- **Monitoring**: Prometheus, Grafana, Loki for comprehensive observability
- **Internationalization**: Multi-language support (Italian, English, Spanish)
- **CI/CD**: GitHub Actions with automated deployment
- **Docker**: Full containerization for development and production
- **Security**: Best practices implemented throughout

## 📋 Tech Stack

### Backend
- **Python 3.12** - Stable Python runtime
- **FastAPI** - High-performance async web framework
- **Tortoise ORM** - Async ORM for database operations
- **PostgreSQL 16** - Reliable database with timezone support
- **Pydantic** - Data validation and settings management
- **JWT** - Secure authentication tokens
- **Prometheus** - Metrics collection
- **Structlog** - Structured logging
- **Sentry** - Error tracking and monitoring

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Fast build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **Pinia** - State management for Vue
- **Vue Router** - Client-side routing
- **Vue i18n** - Internationalization
- **Axios** - HTTP client
- **Headless UI** - Accessible UI components

### DevOps & Monitoring
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy and static file serving
- **Prometheus** - Metrics collection
- **Grafana** - Metrics visualization
- **Loki** - Log aggregation
- **GitHub Actions** - CI/CD pipeline

## 🛠 Quick Start

### Prerequisites

- **Docker** and **Docker Compose**
- **Node.js 18+** (for frontend development)
- **Python 3.12+** (for backend development)
- **Git**

### 1. Clone and Setup

```bash
git clone https://github.com/paodal/pgpyfatovutwls.git
cd pgpyfatovutwls

# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Development Setup

```bash
# Start all services
docker compose up -d

# The application will be available at:
# - Backend API: http://localhost:8003
# - API Documentation: http://localhost:8003/docs
# - Frontend: http://localhost:8004
# - Grafana: http://localhost:3001 (admin/admin)
# - Prometheus: http://localhost:9090
```

### 3. Initialize Database

The database will be automatically initialized with:
- Default subscription plans (Free and Premium)
- Database schema generation
- Super admin user (configured via SUPER_ADMIN_EMAIL)

## 🏗 Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

### Database Migrations

```bash
cd backend

# Initialize Aerich (first time only)
aerich init-db

# Generate migration
aerich migrate

# Apply migration
aerich upgrade
```

## 🌍 Environment Configuration

### Required Environment Variables

```env
# Database
DATABASE_URL=postgres://user:password@host:port/database

# Security
SECRET_KEY=your-super-secret-key

# Email (for notifications)
GMAIL_PASSPHRASE=your-gmail-app-password

# Lemon Squeezy (for subscriptions)
LS_API_KEY=your-lemon-squeezy-api-key
LEMON_SQUEEZY_WEBHOOK_SECRET=your-webhook-secret
LEMON_SQUEEZY_STORE_ID=your-store-id

# Monitoring (optional)
SENTRY_DSN=your-sentry-dsn
```

### Email Configuration

To enable email notifications:

1. Enable 2-factor authentication on your Gmail account
2. Generate an app password: [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Add the app password to `GMAIL_PASSPHRASE` in your environment

### Lemon Squeezy Configuration

1. Create account at [Lemon Squeezy](https://lemonsqueezy.com)
2. Create products and variants
3. Configure webhook endpoint: `https://your-domain.com/api/v1/webhooks/lemon-squeezy`
4. Add API keys to environment variables

## 🔧 API Documentation

The API documentation is automatically generated and available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/token` - User login
- `GET /api/v1/auth/me` - Get current user
- `GET /api/v1/subscriptions/plans` - Get subscription plans
- `POST /api/v1/subscriptions/checkout/{plan_id}` - Create checkout session
- `GET /api/v1/subscriptions/current` - Get current subscription

## 📊 Monitoring

### Metrics

The application exposes metrics at `/metrics` endpoint for Prometheus scraping:

- HTTP request count and duration
- Error rates and status codes
- Custom business metrics

### Dashboards

Grafana dashboards are pre-configured with:
- Application performance metrics
- Database performance
- Infrastructure metrics
- Custom business KPIs

Access Grafana at http://localhost:3001 (admin/admin)

### Logging

Structured logging with Loki integration:
- All application logs are centralized
- Search and filter capabilities
- Error tracking and alerting

## 🚀 Deployment

### Production Deployment

The application uses GitHub Actions for automated deployment:

1. **Staging**: Push to `develop` branch
   - Deploys to `test.pgpyfatovutwls.europeople.net`
   - Port: 9003

2. **Production**: Push to `main` branch
   - Deploys to `pgpyfatovutwls.europeople.net`
   - Port: 8003

### Manual Deployment

```bash
# Build production images
docker compose -f docker-compose.prod.yml build

# Deploy
docker compose -f docker-compose.prod.yml up -d

# Check health
curl http://localhost:8003/health
```

### Server Requirements

- **Ubuntu 20.04+**
- **Docker** and **Docker Compose**
- **Nginx** (for reverse proxy)
- **Certbot** (for SSL certificates)
- **PostgreSQL** (for database)

## 🔐 Security

### Authentication & Authorization

- JWT tokens with configurable expiration
- Password hashing with bcrypt
- Email verification workflow
- Role-based access control (user/superuser)

### Security Headers

- CORS configuration
- Security headers (HSTS, CSP, etc.)
- Input validation and sanitization

### Data Protection

- Secure database connections
- Environment variable protection
- Secrets management via GitHub Secrets

## 🌐 Internationalization

The application supports multiple languages:

- **Italian** (default)
- **English**
- **Spanish**

### Adding New Languages

1. Create language file in `frontend/src/locales/`
2. Add language to `LanguageSelector.vue`
3. Update language options in registration form

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
# Run full test suite
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

## 📄 Database Schema

### Users Table
- Basic user information
- Authentication credentials
- Profile settings (language, timezone)
- Lemon Squeezy customer integration

### Subscription Plans Table
- Plan details (name, price, features)
- Currency support (EUR, USD, GBP)
- Lemon Squeezy product integration

### User Subscriptions Table
- Active subscriptions
- Billing information
- Status tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a Pull Request

### Code Style

- **Backend**: Follow PEP 8, use Black for formatting
- **Frontend**: Use ESLint and Prettier
- **Commits**: Use conventional commit messages

## 📜 License

This project is licensed under a proprietary license. Redistribution is prohibited.

---

## 🆘 Support

For support and questions:

- **Documentation**: Check this README and API docs
- **Issues**: Create a GitHub issue
- **Email**: Contact the development team

## 🔄 Changelog

### v1.0.0 (2024-12-25)
- Initial release
- Complete authentication system
- Lemon Squeezy integration
- Monitoring and logging
- Internationalization support
- Production-ready deployment

---

**Built with ❤️ using modern technologies for scalable web applications.**# 🚀 Deployment triggered with corrected dual-port workflow
# Fix workflow syntax
# Fix YAML indentation
