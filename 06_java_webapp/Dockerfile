# Use OpenJDK 21 (matching your pom.xml configuration)
FROM openjdk:21-jdk-slim

# Set working directory
WORKDIR /app

# Install necessary packages for building
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Maven wrapper and pom.xml first (for better Docker layer caching)
COPY mvnw pom.xml ./
COPY .mvn .mvn

# Make Maven wrapper executable
RUN chmod +x mvnw

# Download dependencies (this layer will be cached if pom.xml doesn't change)
RUN ./mvnw dependency:go-offline -B

# Copy source code
COPY src src

# Build the application
RUN ./mvnw clean package -DskipTests

# Expose the port that Render will assign (via PORT environment variable)
EXPOSE $PORT

# Create a non-root user for security
RUN addgroup --system --gid 1001 rhythmiq && \
    adduser --system --uid 1001 rhythmiq

# Create writable uploads directory
RUN mkdir -p /var/tmp/java-webapp-uploads && chown -R rhythmiq:rhythmiq /var/tmp/java-webapp-uploads

# Change ownership of the app directory
RUN chown -R rhythmiq:rhythmiq /app

# Switch to non-root user
USER rhythmiq

# Run the application
# The PORT environment variable will be provided by Render
CMD sh -c "java -Dserver.port=${PORT:-8080} -jar target/rhythmiq-webapp-1.0.0.jar"