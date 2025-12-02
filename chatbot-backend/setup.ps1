# Bwire Global Tech AI Chatbot - Quick Setup Script
# Run this to set up everything automatically

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Bwire Global Tech AI Chatbot Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "Installing Python packages (this may take a few minutes)..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✓ All packages installed" -ForegroundColor Green

# Download NLP models
Write-Host ""
Write-Host "Downloading NLP models..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
Write-Host "✓ NLP models downloaded" -ForegroundColor Green

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "Setting up environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file from template" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit .env and add your API key!" -ForegroundColor Yellow
    Write-Host "   Options:" -ForegroundColor White
    Write-Host "   1. OpenAI: https://platform.openai.com/api-keys" -ForegroundColor White
    Write-Host "   2. Anthropic: https://console.anthropic.com/" -ForegroundColor White
    Write-Host ""
}

# Create data directory
Write-Host ""
Write-Host "Creating data directories..." -ForegroundColor Yellow
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
}
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}
Write-Host "✓ Data directories created" -ForegroundColor Green

# Create knowledge base file
Write-Host ""
Write-Host "Creating knowledge base..." -ForegroundColor Yellow
$knowledgeBase = @"
{
  "company": {
    "name": "Bwire Global Tech",
    "location": "Nairobi, Kenya",
    "email": "bilfordderek917@gmail.com",
    "phone": "+254722206805",
    "website": "https://www.triventatech.com"
  },
  "services": [
    {
      "name": "Web Development",
      "description": "Professional websites, e-commerce, web applications",
      "pricing": "KES 50,000 - 200,000+"
    },
    {
      "name": "AI & Data Science",
      "description": "Machine learning, chatbots, predictive analytics",
      "pricing": "Custom quotes based on complexity"
    },
    {
      "name": "Cybersecurity",
      "description": "Security audits, penetration testing, threat protection",
      "pricing": "Starting from KES 100,000"
    },
    {
      "name": "Cloud Solutions",
      "description": "AWS, Azure, Google Cloud deployment and management",
      "pricing": "KES 80,000 - 300,000"
    },
    {
      "name": "Mobile Apps",
      "description": "Android and iOS applications",
      "pricing": "KES 150,000 - 500,000"
    },
    {
      "name": "Training Programs",
      "description": "Tech training and workshops",
      "pricing": "Contact for details"
    }
  ]
}
"@
$knowledgeBase | Out-File -FilePath "data\knowledge_base.json" -Encoding UTF8
Write-Host "✓ Knowledge base created" -ForegroundColor Green

# Display next steps
Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✓ Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Edit .env file and add your API key:" -ForegroundColor White
Write-Host "   notepad .env" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start the server:" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Test the API:" -ForegroundColor White
Write-Host "   Visit: http://localhost:8000/health" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Read the documentation:" -ForegroundColor White
Write-Host "   Get-Content README.md" -ForegroundColor Gray
Write-Host ""
Write-Host "For support, contact:" -ForegroundColor White
Write-Host "  Email: bilfordderek917@gmail.com" -ForegroundColor Gray
Write-Host "  Phone: +254722206805" -ForegroundColor Gray
Write-Host ""
