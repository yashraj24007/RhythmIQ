# 🚀 RhythmIQ Render Deployment Guide

This guide will help you deploy your RhythmIQ ECG Analysis web application to Render.

## 📋 Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Java 21** - Your app uses Java 21 (handled automatically by Render)

## 🛠️ Pre-Deployment Setup (Already Completed)

The following files have been created/updated for Render deployment:

### ✅ Configuration Files Created:
- `render.yaml` - Render service configuration
- `java-webapp/.gitattributes` - Line ending configuration
- `java-webapp/mvnw` - Unix Maven wrapper script
- `java-webapp/src/main/resources/application-production.properties` - Production settings

### ✅ Files Updated:
- `java-webapp/src/main/resources/application.properties` - Added PORT environment variable support
- `java-webapp/src/main/java/com/rhythmiq/service/InferenceService.java` - Updated to use /tmp directory

## 🚀 Deployment Steps

### Step 1: Push to GitHub
```bash
# Navigate to your project directory
cd "c:\Users\skamb\OneDrive\Documents\shreesh\shreesh_clg\RhythmIQ\RhythmIQ"

# Add all files
git add .

# Commit changes
git commit -m "Configure for Render deployment"

# Push to GitHub
git push origin main
```

### Step 2: Deploy on Render

#### Option A: Using render.yaml (Recommended)
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Select your repository
5. Click **"Apply"**

#### Option B: Manual Web Service Creation
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name:** `rhythmiq-webapp`
   - **Environment:** `Java`
   - **Build Command:** `cd java-webapp && chmod +x mvnw && ./mvnw clean package -DskipTests`
   - **Start Command:** `cd java-webapp && java -Dserver.port=$PORT -jar target/rhythmiq-webapp-1.0.0.jar`
   - **Plan:** Free (or paid for better performance)

### Step 3: Environment Variables (Optional)
In the Render dashboard, you can set these environment variables:

- `JAVA_OPTS`: `-Xmx512m -XX:MaxMetaspaceSize=128m`
- `SPRING_PROFILES_ACTIVE`: `production`

## 🔧 Application Features

Your deployed application will have:

- **ECG Image Upload** - Users can upload ECG images for analysis
- **Mock AI Analysis** - Currently returns mock predictions (ready for real model integration)
- **Responsive Web Interface** - Clean, professional UI
- **File Size Limits** - 5MB max file size in production
- **Optimized Performance** - Compression and caching enabled

## 📱 Access Your Application

Once deployed, Render will provide a URL like:
```
https://rhythmiq-webapp.onrender.com
```

## ⚠️ Important Notes

### Free Tier Limitations:
- **Sleep Mode**: App sleeps after 15 minutes of inactivity
- **Cold Starts**: First request after sleep may take 10-30 seconds
- **Ephemeral Storage**: Uploaded files are temporary (deleted on restart)

### File Upload Behavior:
- Files are stored in `/tmp` directory
- Files are automatically cleaned up on app restart
- Maximum file size: 5MB in production, 10MB in development

## 🔍 Troubleshooting

### Build Fails?
1. Check build logs in Render dashboard
2. Ensure Maven wrapper has execute permissions
3. Verify Java version compatibility

### App Won't Start?
1. Check start command in render.yaml
2. Verify PORT environment variable is being used
3. Check application logs for errors

### Upload Issues?
1. Verify file size is under 5MB
2. Check supported file formats (PNG, JPG, JPEG)
3. Ensure /tmp directory permissions

## 🔄 Future Enhancements

To integrate a real Python ML model:

1. **Add Python Runtime**: Update render.yaml to include Python
2. **Install Dependencies**: Add Python requirements.txt
3. **Update InferenceService**: Replace mock predictions with real model calls
4. **Add Model Files**: Include trained model files in deployment

## 💡 Tips for Production

1. **Upgrade to Paid Plan** for:
   - No sleep mode
   - Faster cold starts
   - More memory/CPU
   - Persistent storage options

2. **Enable Auto-Deploy** from main branch for continuous deployment

3. **Set up Health Checks** using the built-in health endpoint

4. **Monitor Logs** through Render dashboard for debugging

## 📞 Support

If you encounter issues:
1. Check Render documentation
2. Review application logs in Render dashboard
3. Test locally first to isolate deployment-specific issues

Your RhythmIQ application is now ready for cloud deployment! 🎉