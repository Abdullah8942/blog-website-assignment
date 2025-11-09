# Blog Web App Django - Complete Local Setup Script
# This script will install all dependencies and run the development server

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Blog Web App Django - Setup & Run" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if Python is installed
Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from python.org" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Step 2: Create Virtual Environment
Write-Host "Step 2: Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".\venv") {
    Write-Host "Virtual environment already exists, skipping creation..." -ForegroundColor Cyan
} else {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Step 3: Activate Virtual Environment
Write-Host "Step 3: Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Step 4: Install Dependencies
Write-Host "Step 4: Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ All dependencies installed" -ForegroundColor Green
Write-Host ""

# Step 5: Run Migrations
Write-Host "Step 5: Running database migrations..." -ForegroundColor Yellow
python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to run migrations" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Migrations completed" -ForegroundColor Green
Write-Host ""

# Step 6: Collect Static Files
Write-Host "Step 6: Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to collect static files" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Static files collected" -ForegroundColor Green
Write-Host ""

# Step 7: Check for superuser
Write-Host "Step 7: Checking for superuser..." -ForegroundColor Yellow
$superuserCount = python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).count())"
if ($superuserCount -eq 0) {
    Write-Host "No superuser found. Creating one..." -ForegroundColor Cyan
    python manage.py createsuperuser
} else {
    Write-Host "✓ Superuser already exists" -ForegroundColor Green
}
Write-Host ""

# Step 8: Ask about sample data
Write-Host "Step 8: Setting up sample data..." -ForegroundColor Yellow
$setupSample = Read-Host "Would you like to load sample data? (y/n)"
if ($setupSample -eq "y" -or $setupSample -eq "Y") {
    python manage.py setup_sample_data
    Write-Host "✓ Sample data loaded" -ForegroundColor Green
} else {
    Write-Host "Skipped sample data setup" -ForegroundColor Cyan
}
Write-Host ""

# Step 9: Start Development Server
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Starting Development Server" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✓ All setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "The application will now start at http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Admin panel: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver
