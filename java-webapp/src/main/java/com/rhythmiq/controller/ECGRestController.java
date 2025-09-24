package com.rhythmiq.controller;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.rhythmiq.model.ECGAnalysisResult;
import com.rhythmiq.service.ECGAnalysisService;

/**
 * REST API Controller for RhythmIQ Application
 */
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class ECGRestController {

    @Autowired
    private ECGAnalysisService ecgAnalysisService;

    /**
     * Health check endpoint
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> healthCheck() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "UP");
        response.put("service", "RhythmIQ ECG Analysis API");
        response.put("version", "1.0.0");
        return ResponseEntity.ok(response);
    }

    /**
     * Analyze ECG via REST API
     */
    @PostMapping("/analyze")
    public ResponseEntity<?> analyzeECG(@RequestParam("file") MultipartFile file) {
        
        try {
            // Validate file
            if (!ecgAnalysisService.isValidECGImage(file)) {
                Map<String, String> error = new HashMap<>();
                error.put("error", "Invalid file format. Please upload PNG, JPG, or JPEG files only.");
                return ResponseEntity.badRequest().body(error);
            }

            // Analyze ECG
            ECGAnalysisResult result = ecgAnalysisService.analyzeECG(file);
            
            return ResponseEntity.ok(result);
            
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Analysis failed: " + e.getMessage());
            return ResponseEntity.internalServerError().body(error);
        }
    }

    /**
     * Get supported ECG classes
     */
    @GetMapping("/classes")
    public ResponseEntity<Map<String, Object>> getSupportedClasses() {
        Map<String, Object> response = new HashMap<>();
        
        Map<String, String> classes = new HashMap<>();
        classes.put("N", "Normal beats (sinus rhythm, bundle branch block)");
        classes.put("S", "Supraventricular beats (atrial premature beats)");
        classes.put("V", "Ventricular beats (PVC - Premature Ventricular Contractions)");
        classes.put("F", "Fusion beats (fusion of ventricular + normal beat)");
        classes.put("Q", "Unknown/Paced beats (unclassifiable beats)");
        classes.put("M", "Myocardial Infarction (heart attack indicators)");
        
        response.put("classes", classes);
        response.put("total_classes", classes.size());
        
        return ResponseEntity.ok(response);
    }

    /**
     * Get severity levels
     */
    @GetMapping("/severity-levels")
    public ResponseEntity<Map<String, Object>> getSeverityLevels() {
        Map<String, Object> response = new HashMap<>();
        
        Map<String, String> severityLevels = new HashMap<>();
        severityLevels.put("Mild", "Low risk - routine monitoring recommended");
        severityLevels.put("Moderate", "Medium risk - closer monitoring advised");
        severityLevels.put("Severe", "High risk - immediate medical attention required");
        
        response.put("severity_levels", severityLevels);
        response.put("total_levels", severityLevels.size());
        
        return ResponseEntity.ok(response);
    }
}