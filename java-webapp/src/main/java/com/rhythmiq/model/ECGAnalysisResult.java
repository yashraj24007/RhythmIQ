package com.rhythmiq.model;

import java.time.LocalDateTime;

/**
 * ECG Analysis Result Model
 */
public class ECGAnalysisResult {
    private String filename;
    private String predictedClass;
    private double confidence;
    private String severity;
    private double severityConfidence;
    private String classDescription;
    private String severityDescription;
    private LocalDateTime analysisTime;
    private String imagePath;

    // Constructors
    public ECGAnalysisResult() {}

    public ECGAnalysisResult(String filename, String predictedClass, double confidence, 
                           String severity, double severityConfidence) {
        this.filename = filename;
        this.predictedClass = predictedClass;
        this.confidence = confidence;
        this.severity = severity;
        this.severityConfidence = severityConfidence;
        this.analysisTime = LocalDateTime.now();
        this.classDescription = getClassDescription(predictedClass);
        this.severityDescription = getSeverityDescription(severity);
    }

    // Getters and Setters
    public String getFilename() { return filename; }
    public void setFilename(String filename) { this.filename = filename; }

    public String getPredictedClass() { return predictedClass; }
    public void setPredictedClass(String predictedClass) { 
        this.predictedClass = predictedClass;
        this.classDescription = getClassDescription(predictedClass);
    }

    public double getConfidence() { return confidence; }
    public void setConfidence(double confidence) { this.confidence = confidence; }

    public String getSeverity() { return severity; }
    public void setSeverity(String severity) { 
        this.severity = severity;
        this.severityDescription = getSeverityDescription(severity);
    }

    public double getSeverityConfidence() { return severityConfidence; }
    public void setSeverityConfidence(double severityConfidence) { 
        this.severityConfidence = severityConfidence; 
    }

    public String getClassDescription() { return classDescription; }
    public void setClassDescription(String classDescription) { 
        this.classDescription = classDescription; 
    }

    public String getSeverityDescription() { return severityDescription; }
    public void setSeverityDescription(String severityDescription) { 
        this.severityDescription = severityDescription; 
    }

    public LocalDateTime getAnalysisTime() { return analysisTime; }
    public void setAnalysisTime(LocalDateTime analysisTime) { this.analysisTime = analysisTime; }

    public String getImagePath() { return imagePath; }
    public void setImagePath(String imagePath) { this.imagePath = imagePath; }

    // Helper methods
    private String getClassDescription(String className) {
        switch (className.toUpperCase()) {
            case "N": return "Normal beats (sinus rhythm, bundle branch block)";
            case "S": return "Supraventricular beats (atrial premature beats)";
            case "V": return "Ventricular beats (PVC - Premature Ventricular Contractions)";
            case "F": return "Fusion beats (fusion of ventricular + normal beat)";
            case "Q": return "Unknown/Paced beats (unclassifiable beats)";
            case "M": return "Myocardial Infarction (heart attack indicators)";
            default: return "Unknown classification";
        }
    }

    private String getSeverityDescription(String severity) {
        switch (severity.toLowerCase()) {
            case "mild": return "Low risk - routine monitoring recommended";
            case "moderate": return "Medium risk - closer monitoring advised";
            case "severe": return "High risk - immediate medical attention required";
            default: return "Severity assessment unavailable";
        }
    }

    public String getSeverityColorClass() {
        switch (severity.toLowerCase()) {
            case "mild": return "success";
            case "moderate": return "warning";
            case "severe": return "danger";
            default: return "secondary";
        }
    }

    public String getConfidenceLevel() {
        if (confidence >= 0.9) return "Very High";
        else if (confidence >= 0.8) return "High";
        else if (confidence >= 0.7) return "Medium";
        else if (confidence >= 0.6) return "Low";
        else return "Very Low";
    }
}