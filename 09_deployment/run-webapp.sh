#!/bin/bash
# RhythmIQ Java Web Application - Build and Run Script

echo "🫀 RhythmIQ ECG Analysis System"
echo "=================================="

# Change to webapp directory
cd java-webapp

echo "📦 Building application..."
./mvnw clean package -DskipTests

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "🚀 Starting RhythmIQ Web Application..."
    echo "🌐 Application will be available at: http://localhost:8080"
    echo ""
    
    # Run the application
    ./mvnw spring-boot:run
else
    echo "❌ Build failed!"
    exit 1
fi