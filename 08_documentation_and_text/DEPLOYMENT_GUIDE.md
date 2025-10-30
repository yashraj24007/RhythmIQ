# 🚀 RhythmIQ Deployment Guide

## 📋 Architecture Overview

Your RhythmIQ application has **two components**:
1. **Python Flask API** (ML Model) - Port 8083
2. **Java Spring Boot Webapp** (Frontend) - Port 8082

## 🎯 Hosting Recommendations

### ❌ Why NOT Vercel?
- **Vercel is designed for static sites and serverless functions** (Next.js, React, etc.)
- Does NOT support:
  - Java Spring Boot applications
  - Long-running Python processes
  - Machine Learning model hosting

### ✅ Recommended: Render.com
**Best for your use case** - Supports both Java and Python backends

### ✅ Alternative: Railway.app
Good alternative with similar features

---

## 🔧 Option 1: Deploy on Render (RECOMMENDED)

### Step 1: Prepare Python ML API

Create `render.yaml` in project root:

```yaml
services:
  # Python ML API Service
  - type: web
    name: rhythmiq-ml-api
    runtime: python
    buildCommand: pip install -r requirements-api.txt
    startCommand: python 11_python_api/rhythmiq_api.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.13.7
      - key: PORT
        value: 8083
    
  # Java Spring Boot Webapp
  - type: web
    name: rhythmiq-webapp
    runtime: java
    buildCommand: cd 07_java_webapp && ./mvnw clean package -DskipTests
    startCommand: java -jar 07_java_webapp/target/rhythmiq-webapp-1.0.0.jar
    envVars:
      - key: JAVA_VERSION
        value: 21
      - key: PORT
        value: 8082
      - key: PYTHON_API_URL
        value: https://rhythmiq-ml-api.onrender.com
```

### Step 2: Create Separate Requirements File for API

Create `requirements-api.txt`:
```txt
Flask==3.1.0
joblib==1.4.2
numpy==2.2.1
Pillow==11.0.0
scikit-learn==1.6.1
```

### Step 3: Update Python API for Production

Modify `11_python_api/rhythmiq_api.py` - Add at the end:

```python
if __name__ == '__main__':
    # Load model on startup
    if load_model():
        port = int(os.environ.get('PORT', 8083))
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        print("❌ Failed to start: Model not loaded")
        sys.exit(1)
```

### Step 4: Update Java Webapp Configuration

Create `07_java_webapp/src/main/resources/application-prod.properties`:

```properties
# Production Configuration
spring.application.name=RhythmIQ ECG Analysis
server.port=${PORT:8082}

# Python API URL (from environment variable)
python.api.url=${PYTHON_API_URL:http://localhost:8083}

# File upload settings
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
spring.servlet.multipart.enabled=true

# Upload directory (use temp directory in production)
upload.dir=${UPLOAD_DIR:/tmp/uploads}

# Logging
logging.level.root=INFO
logging.level.com.rhythmiq=INFO
```

### Step 5: Deploy to Render

1. **Push code to GitHub**:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

2. **Create Render Account**: https://render.com

3. **Create New Blueprint**:
   - Click "New +"
   - Select "Blueprint"
   - Connect your GitHub repository
   - Render will detect `render.yaml` and create both services

4. **Set Environment Variables** (in Render dashboard):
   - For Java webapp:
     - `PYTHON_API_URL` = `https://rhythmiq-ml-api.onrender.com`
   - Both services will auto-detect PORT

5. **Deploy**: Render will automatically build and deploy both services

---

## 🔧 Option 2: Deploy on Railway.app

### Step 1: Install Railway CLI
```bash
npm i -g @railway/cli
railway login
```

### Step 2: Initialize Railway Project
```bash
railway init
railway link
```

### Step 3: Create Two Services

**For Python API**:
```bash
railway up --service python-api
# Set start command: python 11_python_api/rhythmiq_api.py
```

**For Java Webapp**:
```bash
railway up --service java-webapp
# Set build command: cd 07_java_webapp && ./mvnw clean package -DskipTests
# Set start command: java -jar 07_java_webapp/target/rhythmiq-webapp-1.0.0.jar
```

---

## 🔧 Option 3: Heroku (Requires Paid Plan)

Create `Procfile`:
```
web: cd 07_java_webapp && java -jar target/rhythmiq-webapp-1.0.0.jar
worker: python 11_python_api/rhythmiq_api.py
```

---

## 🐳 Option 4: Docker Deployment (Any Cloud)

### Create Dockerfiles

**1. Python API - `Dockerfile.python`**:
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Copy Python API and dependencies
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY 11_python_api/ ./11_python_api/
COPY 02_preprocessing/ ./02_preprocessing/
COPY 03_model_training/ ./03_model_training/
COPY 05_trained_models/ ./05_trained_models/
COPY 01_data/ ./01_data/

WORKDIR /app/11_python_api

EXPOSE 8083

CMD ["python", "rhythmiq_api.py"]
```

**2. Java Webapp - `Dockerfile.java`**:
```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS build

WORKDIR /app

# Copy Maven project
COPY 07_java_webapp/pom.xml .
COPY 07_java_webapp/mvnw .
COPY 07_java_webapp/mvnw.cmd .
COPY 07_java_webapp/.mvn .mvn
COPY 07_java_webapp/src src

# Build application
RUN ./mvnw clean package -DskipTests

# Runtime stage
FROM eclipse-temurin:21-jre-jammy

WORKDIR /app

# Copy JAR from build stage
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8082

CMD ["java", "-jar", "app.jar"]
```

**3. Docker Compose - `docker-compose.yml`**:
```yaml
version: '3.8'

services:
  python-api:
    build:
      context: .
      dockerfile: Dockerfile.python
    ports:
      - "8083:8083"
    environment:
      - PORT=8083
    volumes:
      - ./05_trained_models:/app/05_trained_models
    restart: unless-stopped

  java-webapp:
    build:
      context: .
      dockerfile: Dockerfile.java
    ports:
      - "8082:8082"
    environment:
      - PORT=8082
      - PYTHON_API_URL=http://python-api:8083
    depends_on:
      - python-api
    restart: unless-stopped
```

Deploy to:
- **DigitalOcean App Platform**
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Apps**

---

## 🔧 Fix: Stop CMD Window from Opening (Local Development)

### Option A: Modify start-services.ps1 (Hide Windows)

Replace line 46 in `start-services.ps1`:
```powershell
# OLD (shows window):
Start-Process -FilePath "java" `
              -ArgumentList "-jar","target\rhythmiq-webapp-1.0.0.jar" `
              -WindowStyle Normal

# NEW (hides window):
Start-Process -FilePath "java" `
              -ArgumentList "-jar","target\rhythmiq-webapp-1.0.0.jar" `
              -WindowStyle Hidden
```

### Option B: Create Background Service (Windows)

Use **NSSM** (Non-Sucking Service Manager):
```bash
# Download NSSM
choco install nssm

# Install as Windows Service
nssm install RhythmIQ-Java "java" "-jar E:\Projects\RhythmIQ\07_java_webapp\target\rhythmiq-webapp-1.0.0.jar"
nssm install RhythmIQ-Python "python" "E:\Projects\RhythmIQ\11_python_api\rhythmiq_api.py"

# Start services
nssm start RhythmIQ-Java
nssm start RhythmIQ-Python
```

---

## 📝 Summary of Best Approach

### For Cloud Hosting:
**🥇 Render.com** (Free tier available)
- Easiest setup
- Supports both Python and Java
- Auto-deploys from GitHub
- Free SSL certificates

### For Local Development:
**Option 1**: Modify `start-services.ps1` to use `-WindowStyle Hidden`  
**Option 2**: Use Windows Services with NSSM

---

## 🚀 Quick Start: Deploy to Render

1. Create `render.yaml` (provided above)
2. Create `requirements-api.txt` (provided above)
3. Update `rhythmiq_api.py` with production settings
4. Push to GitHub
5. Connect GitHub to Render
6. Deploy! 🎉

**Your app will be live at**:
- Python API: `https://rhythmiq-ml-api.onrender.com`
- Web App: `https://rhythmiq-webapp.onrender.com`

---

## ⚠️ Important Notes

1. **Model File Size**: The `rythmguard_model.joblib` must be committed to Git or uploaded separately
2. **Free Tier Limitations**:
   - Render free tier: Services sleep after 15 minutes of inactivity
   - First request after sleep takes ~30 seconds to wake up
3. **Upgrade to Paid**: For production, use paid tier ($7/month per service)

Need help with deployment? Let me know which platform you prefer! 🚀
