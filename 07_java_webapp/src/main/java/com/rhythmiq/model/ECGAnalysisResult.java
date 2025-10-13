package com.rhythmiq.model;

import java.time.LocalDateTime;

/**
 * Plain Java object to hold ECG classification & severity output.
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

    public ECGAnalysisResult() { this.analysisTime = LocalDateTime.now(); }

    public ECGAnalysisResult(String filename, String predictedClass, double confidence,
                             String severity, double severityConfidence) {
        this();
        this.filename = filename;
        setPredictedClass(predictedClass);
        setConfidence(confidence);
        setSeverity(severity);
        setSeverityConfidence(severityConfidence);
    }

    public String getFilename() { return filename; }
    public void setFilename(String filename) { this.filename = filename; }

    public String getPredictedClass() { return predictedClass; }
    public void setPredictedClass(String predictedClass) {
        this.predictedClass = predictedClass;
        this.classDescription = describeClass(predictedClass);
    }

    public double getConfidence() { return confidence; }
    public void setConfidence(double confidence) { this.confidence = confidence; }

    public String getSeverity() { return severity; }
    public void setSeverity(String severity) {
        this.severity = severity;
        this.severityDescription = describeSeverity(severity);
    }

    public double getSeverityConfidence() { return severityConfidence; }
    public void setSeverityConfidence(double severityConfidence) { this.severityConfidence = severityConfidence; }

    public String getClassDescription() { return classDescription; }
    public String getSeverityDescription() { return severityDescription; }
    public LocalDateTime getAnalysisTime() { return analysisTime; }
    public void setAnalysisTime(LocalDateTime analysisTime) { this.analysisTime = analysisTime; }
    public String getImagePath() { return imagePath; }
    public void setImagePath(String imagePath) { this.imagePath = imagePath; }

    private String describeClass(String cls) {
        if (cls == null) return "Unknown classification";
        switch (cls.toUpperCase()) {
            case "N": return "Normal beats (sinus rhythm, bundle branch block)";
            case "S": return "Supraventricular beats (atrial premature beats)";
            case "V": return "Ventricular beats (PVC - Premature Ventricular Contractions)";
            case "F": return "Fusion beats (fusion of ventricular + normal beat)";
            case "Q": return "Unknown/Paced beats (unclassifiable beats)";
            case "M": return "Myocardial Infarction (heart attack indicators)";
            default: return "Unknown classification";
        }
    }

    private String describeSeverity(String sev) {
        if (sev == null) return "Severity assessment unavailable";
        switch (sev.toLowerCase()) {
            case "mild": return "Low risk - routine monitoring recommended";
            case "moderate": return "Medium risk - closer monitoring advised";
            case "severe": return "High risk - immediate medical attention required";
            default: return "Severity assessment unavailable";
        }
    }

    public String getSeverityColorClass() {
        if (severity == null) return "secondary";
        switch (severity.toLowerCase()) {
            case "mild": return "success";
            case "moderate": return "warning";
            case "severe": return "danger";
            default: return "secondary";
        }
    }

    public String getConfidenceLevel() {
        if (confidence >= 0.9) return "Very High";
        if (confidence >= 0.8) return "High";
        if (confidence >= 0.7) return "Medium";
        if (confidence >= 0.6) return "Low";
        return "Very Low";
    }
}