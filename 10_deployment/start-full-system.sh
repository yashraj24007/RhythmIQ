#!/bin/bash
# Start RhythmIQ with Real ML Model Integration

echo "🫀 RhythmIQ ECG Analysis System - Full Integration"
echo "==================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi

echo "📦 Installing Python API dependencies..."
pip3 install -r api_requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully!"
echo

echo "🐍 Starting Python ML API Service (Port 8083)..."
python3 python_api_service.py &
PYTHON_PID=$!

# Wait a moment for Python API to start
sleep 5

echo "🌐 Testing Python API connection..."
if curl -s http://localhost:8083/health > /dev/null; then
    echo "✅ Python API is running!"
else
    echo "⚠️  Python API might still be starting..."
fi

echo
echo "☕ Starting Java Web Application (Port 8082)..."
cd java-webapp
./mvnw spring-boot:run &
JAVA_PID=$!

echo
echo "🎉 RhythmIQ is now running with REAL ML MODEL!"
echo "🌐 Web Interface: http://localhost:8082"
echo "🐍 Python API: http://localhost:8083"
echo
echo "Press Ctrl+C to stop both services"

# Handle Ctrl+C
trap 'kill $PYTHON_PID $JAVA_PID; exit' INT

# Wait for processes
wait