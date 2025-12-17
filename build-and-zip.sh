#!/bin/bash
# Bash script to build and zip frontend for Namecheap upload
# Run this from the project root directory

echo "🚀 Building frontend for production..."

# Check if backend URL is set
if [ -z "$VITE_API_URL" ]; then
    echo "⚠️  VITE_API_URL not set. Using default Render URL..."
    export VITE_API_URL="https://nano-banana-ta-backend.onrender.com"
fi

echo "📦 Backend URL: $VITE_API_URL"

# Navigate to frontend directory
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📥 Installing dependencies..."
    npm install
fi

# Build the frontend
echo "🔨 Building production bundle..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    cd ..
    exit 1
fi

# Go back to root
cd ..

# Check if dist folder exists
if [ ! -d "frontend/dist" ]; then
    echo "❌ Build output not found!"
    exit 1
fi

# Create zip file
ZIP_PATH="frontend-build.zip"
if [ -f "$ZIP_PATH" ]; then
    rm "$ZIP_PATH"
    echo "🗑️  Removed existing zip file"
fi

echo "📦 Creating zip file..."
cd frontend/dist
zip -r "../../$ZIP_PATH" . -q
cd ../..

if [ -f "$ZIP_PATH" ]; then
    ZIP_SIZE=$(du -h "$ZIP_PATH" | cut -f1)
    echo "✅ Build complete!"
    echo "📁 Zip file created: $ZIP_PATH ($ZIP_SIZE)"
    echo ""
    echo "📤 Next steps:"
    echo "   1. Upload $ZIP_PATH to Namecheap cPanel File Manager"
    echo "   2. Extract it in public_html folder"
    echo "   3. Make sure index.html is in public_html root"
    echo "   4. Update backend CORS to allow your domain"
else
    echo "❌ Failed to create zip file!"
    exit 1
fi

