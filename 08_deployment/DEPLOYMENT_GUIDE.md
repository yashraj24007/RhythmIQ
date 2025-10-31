# 🚀 RhythmIQ Deployment Guide

## Quick Deployment Fixes Applied

### Issues Fixed:
1. ✅ Updated `render.yaml` paths (07_java_webapp → 06_java_webapp, 11_python_api → 09_python_api)
2. ✅ Added environment variables configuration to render.yaml
3. ✅ Fixed Dockerfile CMD to properly handle PORT environment variable
4. ✅ Updated start-webapp.bat with correct paths

---

## Deployment Options

### Option 1: Render.com (Recommended - Free Tier Available)

#### Prerequisites:
- GitHub account with RhythmIQ repository
- Render.com account (free tier available)
- Supabase project with credentials

#### Step-by-Step Instructions:

1. **Push Latest Changes to GitHub** ✅ (Already done)
   ```powershell
   git add .
   git commit -m "Fix deployment configuration"
   git push origin main
   ```

2. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub
   - Authorize Render to access your repositories

3. **Deploy Using Blueprint (Automatic)**
   - Go to Dashboard → New → Blueprint
   - Select your `RhythmIQ` repository
   - Render will detect `08_deployment/render.yaml`
   - Click "Apply"

4. **Configure Environment Variables** (CRITICAL)
   
   For **rhythmiq-python-api** service:
   - `SUPABASE_URL` = `https://ihgmzhxvuvxwlqprsfdk.supabase.co`
   - `SUPABASE_ANON_KEY` = Your anon key from .env
   - `SUPABASE_SERVICE_KEY` = Your service role key from .env

   For **rhythmiq-java-webapp** service:
   - `SUPABASE_URL` = `https://ihgmzhxvuvxwlqprsfdk.supabase.co`
   - `SUPABASE_ANON_KEY` = Your anon key from .env
   - `SUPABASE_SERVICE_KEY` = Your service role key from .env
   - `PYTHON_API_URL` = `https://rhythmiq-python-api.onrender.com` (auto-set in render.yaml)

5. **Wait for Deployment**
   - Python API: ~5-10 minutes
   - Java Webapp: ~10-15 minutes (Docker build takes longer)

6. **Access Your Application**
   - Java Webapp: `https://rhythmiq-java-webapp.onrender.com`
   - Python API: `https://rhythmiq-python-api.onrender.com/health`

---

### Option 2: Manual Render Deployment (Alternative)

If Blueprint doesn't work:

1. **Deploy Python API Manually**
   - Dashboard → New → Web Service
   - Connect GitHub repository
   - Configure:
     - **Name**: rhythmiq-python-api
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r 09_python_api/requirements.txt`
     - **Start Command**: `python 09_python_api/rhythmiq_api.py`
     - **Environment**: Add all SUPABASE_* variables
   - Deploy

2. **Deploy Java Webapp Manually**
   - Dashboard → New → Web Service
   - Connect GitHub repository
   - Configure:
     - **Name**: rhythmiq-java-webapp
     - **Runtime**: Docker
     - **Dockerfile Path**: `./06_java_webapp/Dockerfile`
     - **Docker Context**: `./06_java_webapp`
     - **Environment**: Add all SUPABASE_* and PYTHON_API_URL variables
   - Deploy

---

### Option 3: Railway.app

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables via Railway Dashboard
# Then deploy
railway up
```

---

### Option 4: Docker Compose (Local/VPS)

**Note**: Need to create `docker-compose.yml` first

```yaml
version: '3.8'
services:
  python-api:
    build: ./09_python_api
    ports:
      - "8083:8083"
    env_file:
      - .env
  
  java-webapp:
    build: ./06_java_webapp
    ports:
      - "8082:8082"
    env_file:
      - .env
    depends_on:
      - python-api
```

Deploy with:
```bash
docker-compose up -d
```

---

## Common Deployment Issues & Solutions

### Issue 1: "Module not found" in Python API
**Solution**: Ensure paths in `rhythmiq_api.py` are correct:
```python
project_root = os.path.dirname(current_dir)
sys.path.append(os.path.join(project_root, '02_preprocessing'))
sys.path.append(os.path.join(project_root, '03_model_training'))
```

### Issue 2: "Model file not found"
**Solution**: Check that `05_trained_models/rythmguard_model.joblib` exists in repository

### Issue 3: Java build fails with "Cannot resolve dependencies"
**Solution**: 
- Check `pom.xml` dependencies
- Ensure Maven wrapper is executable: `chmod +x mvnw`
- Try building locally first: `./mvnw clean package`

### Issue 4: Environment variables not loading
**Solution**:
- Verify variables are set in Render Dashboard
- Check capitalization (must match exactly)
- Restart service after adding variables

### Issue 5: Port binding errors
**Solution**:
- Render provides PORT environment variable automatically
- Java: Uses `${PORT:-8080}`
- Python: Should listen on `0.0.0.0:${PORT:-8083}`

### Issue 6: Python API returns 502 Bad Gateway
**Solution**:
- Check Health Check Path is correct: `/health`
- Verify API is binding to `0.0.0.0` not `127.0.0.1`
- Check logs for startup errors

---

## Verifying Deployment

### Check Python API:
```bash
curl https://rhythmiq-python-api.onrender.com/health
# Should return: {"status": "healthy", "model_loaded": true}
```

### Check Java Webapp:
```bash
curl https://rhythmiq-java-webapp.onrender.com
# Should return HTML homepage
```

### Test Full Flow:
1. Visit Java webapp URL
2. Try to register a new account
3. Login with credentials
4. Upload an ECG image
5. Verify prediction results

---

## Render.yaml Structure Explained

```yaml
services:
  - type: web                    # Web service (has public URL)
    name: rhythmiq-python-api    # Service name
    runtime: python              # Python runtime
    buildCommand: pip install... # Install dependencies
    startCommand: python ...     # Start the server
    healthCheckPath: /health     # Endpoint to check if service is up
    envVars:                     # Environment variables
      - key: SUPABASE_URL
        sync: false              # Don't share between services
```

---

## Cost Considerations

### Render.com Free Tier:
- ✅ 750 hours/month free (enough for 1 service running 24/7)
- ✅ Automatic SSL certificates
- ⚠️ Services spin down after 15 min of inactivity (free tier)
- ⚠️ Cold start: ~30 seconds to wake up
- 💡 **Tip**: Deploy only Java webapp on free tier, run Python API locally

### Railway.app:
- $5/month starter plan
- 500 hours free trial credits
- No sleep on inactivity

### Recommended for Production:
- Render.com Starter ($7/month per service)
- AWS EC2 t2.micro (free tier 1 year)
- DigitalOcean Droplet ($6/month)

---

## Environment Variables Reference

Required for both services:

| Variable | Description | Example |
|----------|-------------|---------|
| `SUPABASE_URL` | Your Supabase project URL | `https://xxx.supabase.co` |
| `SUPABASE_ANON_KEY` | Public anonymous key | `eyJhbG...` |
| `SUPABASE_SERVICE_KEY` | Secret service role key | `eyJhbG...` |

Java webapp only:

| Variable | Description | Example |
|----------|-------------|---------|
| `PYTHON_API_URL` | URL of Python API service | `https://rhythmiq-python-api.onrender.com` |
| `PORT` | Port to run on (auto-set by Render) | `8082` |

---

## Monitoring Your Deployment

### Render Dashboard:
- View logs in real-time
- Monitor CPU/Memory usage
- See deployment history
- Check environment variables

### Health Checks:
```bash
# Python API
curl https://your-api.onrender.com/health

# Java Webapp  
curl https://your-webapp.onrender.com/actuator/health
```

---

## Rollback Procedure

If deployment fails:

1. **Via Git**:
   ```bash
   git log --oneline  # Find previous working commit
   git revert HEAD    # Revert last commit
   git push origin main
   ```

2. **Via Render Dashboard**:
   - Go to service → Deploys
   - Find last successful deployment
   - Click "Redeploy"

---

## Next Steps After Deployment

1. ✅ Test all features (login, register, upload, analyze)
2. ✅ Configure custom domain (optional)
3. ✅ Set up monitoring alerts
4. ✅ Enable automatic deployments from main branch
5. ✅ Add deployment status badge to README

---

## Support

If you encounter issues:

1. Check Render logs for error messages
2. Verify environment variables are set correctly
3. Test locally first: `.\08_deployment\start-services.ps1`
4. Check this guide for common issues

---

**Last Updated**: October 31, 2025
**RhythmIQ Version**: 1.0.0
