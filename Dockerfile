# Multi-stage Docker build for RhythmIQ Java Spring Boot application
FROM eclipse-temurin:21-jdk-alpine as builder

# Set working directory
WORKDIR /app

# Copy Maven wrapper and pom.xml first (for better Docker layer caching)
COPY java-webapp/pom.xml java-webapp/mvnw ./
COPY java-webapp/.mvn .mvn/

# Make Maven wrapper executable
RUN chmod +x mvnw

# Download dependencies (this layer will be cached if pom.xml doesn't change)
RUN ./mvnw dependency:go-offline -B

# Copy source code
COPY java-webapp/src src/

# Build the application
RUN ./mvnw clean package -DskipTests

# Production stage
FROM eclipse-temurin:21-jre-alpine

# Install curl for health checks (Alpine Linux)
RUN apk add --no-cache curl

# Create app directory
WORKDIR /app

# Create non-root user for security (Alpine Linux)
RUN addgroup -g 1001 -S rhythmiq && \
    adduser -u 1001 -S rhythmiq -G rhythmiq

# Copy JAR from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Change ownership
RUN chown rhythmiq:rhythmiq app.jar

# Switch to non-root user
USER rhythmiq

# Expose port (Render will provide PORT env var)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8080}/ || exit 1

# Start the application
CMD ["sh", "-c", "java -Dserver.port=${PORT:-8080} -Xmx512m -XX:MaxMetaspaceSize=128m -jar app.jar"]