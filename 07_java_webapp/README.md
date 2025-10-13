# RhythmIQ Java Web Application

A Spring Boot web interface to upload ECG images and view AI classification results.

## Features
- Upload ECG image (PNG/JPG)
- Mock classification (placeholder)
- Displays predicted class, confidence, severity, descriptions
- Thymeleaf templates and basic styling

## Next Steps (Planned)
1. Integrate real Python inference via REST (Flask/FastAPI) or JEP/ProcessBuilder
2. Add severity explanation and confidence visualization
3. Persist past analyses
4. Add security and user sessions
5. Dockerize the application

## Running Locally
```bash
# From repository root
cd java-webapp
mvn spring-boot:run
# or build
mvn clean package
java -jar target/rhythmiq-webapp-1.0.0.jar
```

Then open: http://localhost:8080

## Real Model Integration Strategy
- Expose Python model (already trained in /01_data) via a FastAPI service
- Java calls: POST /predict with multipart ECG image
- Response JSON mapped to `ECGAnalysisResult`

See `/integration-notes.md` (to be created) for details.
