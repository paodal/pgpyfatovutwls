#!/bin/bash

# Test script for pgpyfatovutwls setup
set -e

echo "🧪 Testing pgpyfatovutwls local development setup..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found. Please run from the project root."
    exit 1
fi

echo "✅ Project structure verified"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker is running"

# Check required files
required_files=(
    "backend/Dockerfile"
    "frontend/Dockerfile" 
    "backend/requirements.txt"
    "frontend/package.json"
    ".env.example"
    "README.md"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: Required file $file is missing"
        exit 1
    fi
done

echo "✅ All required files present"

# Test Docker Compose configuration
echo "🔧 Testing Docker Compose configuration..."
if ! docker compose config > /dev/null 2>&1; then
    echo "❌ Error: Docker Compose configuration is invalid"
    exit 1
fi

echo "✅ Docker Compose configuration is valid"

# Check if ports are available
check_port() {
    local port=$1
    local service=$2
    
    if lsof -i :$port > /dev/null 2>&1; then
        echo "⚠️  Warning: Port $port is already in use (needed for $service)"
        return 1
    else
        echo "✅ Port $port is available for $service"
        return 0
    fi
}

check_port 5432 "PostgreSQL"
check_port 8000 "Backend API"
check_port 3000 "Frontend"
check_port 9090 "Prometheus"
check_port 3001 "Grafana"
check_port 3100 "Loki"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please review and update the configuration."
fi

echo ""
echo "🎉 Setup test completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Review and update .env file with your configuration"
echo "2. Run: docker compose up -d"
echo "3. Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Grafana: http://localhost:3001 (admin/admin)"
echo "   - Prometheus: http://localhost:9090"
echo ""
echo "🔧 For development:"
echo "   - Backend: cd backend && uvicorn app.main:app --reload"
echo "   - Frontend: cd frontend && npm run dev"
echo ""