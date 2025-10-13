# 🚀 **RhythmIQ Java Web Application - Quick Start Guide**

## ❗ **Current Issue**
The Maven wrapper is having issues with the Java environment. Here are the solutions:

### **Solution 1: Install Maven (Recommended)**

1. **Download Maven**: Go to https://maven.apache.org/download.cgi
2. **Extract Maven**: Extract to `C:\apache-maven-3.9.5`
3. **Set Environment Variables**:
   - Add `MAVEN_HOME=C:\apache-maven-3.9.5` 
   - Add `%MAVEN_HOME%\bin` to your PATH
4. **Restart VS Code** and terminal
5. **Run**: 
   ```
   cd E:\Projects\RhythmIQ\java-webapp
   mvn clean spring-boot:run
   ```

### **Solution 2: Use IDE (VS Code)**

1. **Install Java Extension Pack** in VS Code
2. **Open** `E:\Projects\RhythmIQ\java-webapp` in VS Code
3. **Find** `RhythmIQApplication.java` in `src/main/java/com/rhythmiq/`
4. **Click** the "Run" button above the `main` method
5. **Or** press `F5` to debug

### **Solution 3: Fix Maven Wrapper**

Run this in PowerShell:
```powershell
cd E:\Projects\RhythmIQ\java-webapp
Remove-Item -Recurse -Force .mvn
Invoke-WebRequest -Uri "https://repo.maven.apache.org/maven2/org/apache/maven/wrapper/maven-wrapper/3.8.6/maven-wrapper-3.8.6.jar" -OutFile ".mvn/wrapper/maven-wrapper.jar"
```

### **Expected Result**

Once running, you should see:
```
Started RhythmIQApplication in X.XXX seconds
Tomcat started on port 8081 (http)
```

**Then access**: http://localhost:8081

---

## 🛠️ **Current Status**
- ✅ **Java**: Installed (version 24.0.2)
- ❌ **Maven**: Not installed or JAVA_HOME issue
- ✅ **Application**: Code ready
- ✅ **Model**: Available (99.1% accuracy)

## 📱 **Application Features**
- **Upload ECG Images**: Drag & drop interface
- **Real-time Analysis**: 6 ECG classifications
- **Severity Assessment**: Low/Medium/High risk
- **Professional UI**: Bootstrap-based interface

---
*Choose Solution 1 for the fastest setup!*