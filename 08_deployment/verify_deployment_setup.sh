#!/bin/bash
# verify_deployment_setup.sh - Verify RhythmIQ is ready for Render deployment

echo "🔍 Verifying RhythmIQ Render Deployment Setup..."
echo "================================================="

# Check if we're in the right directory
if [ ! -f "render.yaml" ]; then
    echo "❌ Error: render.yaml not found. Run this from the project root directory."
    exit 1
fi

echo "✅ render.yaml found"

# Check Java webapp structure
if [ ! -f "java-webapp/pom.xml" ]; then
    echo "❌ Error: java-webapp/pom.xml not found"
    exit 1
fi

echo "✅ Java webapp structure verified"

# Check Maven wrapper
if [ ! -f "java-webapp/mvnw" ]; then
    echo "❌ Error: Maven wrapper (mvnw) not found"
    exit 1
fi

echo "✅ Maven wrapper found"

# Check if mvnw is executable (on Unix systems)
if [ -f "java-webapp/mvnw" ] && [ ! -x "java-webapp/mvnw" ]; then
    echo "⚠️  Warning: Maven wrapper may not be executable. Running chmod +x..."
    chmod +x java-webapp/mvnw
    echo "✅ Maven wrapper made executable"
else
    echo "✅ Maven wrapper is executable"
fi

# Check configuration files
if [ ! -f "java-webapp/src/main/resources/application.properties" ]; then
    echo "❌ Error: application.properties not found"
    exit 1
fi

echo "✅ Application properties found"

if [ ! -f "java-webapp/src/main/resources/application-production.properties" ]; then
    echo "❌ Error: Production configuration not found"
    exit 1
fi

echo "✅ Production configuration found"

# Check if PORT variable is configured
if grep -q "server.port=\${PORT:" java-webapp/src/main/resources/application.properties; then
    echo "✅ PORT environment variable configured"
else
    echo "❌ Error: PORT environment variable not configured in application.properties"
    exit 1
fi

# Check git status
echo ""
echo "📁 Git Status:"
git status --porcelain

if [ $? -eq 0 ]; then
    echo "✅ Git repository status checked"
else
    echo "❌ Error: Not a git repository or git error"
    exit 1
fi

echo ""
echo "🎉 RhythmIQ is ready for Render deployment!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub: git push origin main"
echo "2. Go to https://dashboard.render.com"
echo "3. Create new Blueprint or Web Service"
echo "4. Connect your GitHub repository"
echo "5. Deploy!"
echo ""
echo "📖 For detailed instructions, see RENDER_DEPLOYMENT_GUIDE.md"