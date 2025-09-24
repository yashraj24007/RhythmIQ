package com.rhythmiq;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * RhythmIQ Web Application
 * 
 * Main entry point for the ECG Analysis Web Application
 */
@SpringBootApplication
public class RhythmIQApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(RhythmIQApplication.class, args);
        System.out.println("\n🫀 RhythmIQ ECG Analysis System Started!");
        System.out.println("🌐 Access the application at: http://localhost:8081");
        System.out.println("📊 Upload ECG images for AI-powered analysis\n");
    }
}