#!/bin/bash

echo "🍌 Setting up Nano Banana TA Tool..."

# Backend setup
echo "📦 Installing backend dependencies..."
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your GOOGLE_API_KEY"
fi

cd ..

# Frontend setup
echo "📦 Installing frontend dependencies..."
cd frontend
npm install

cd ..

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Backend: cd backend && python main.py"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "Don't forget to add your GOOGLE_API_KEY to backend/.env"

