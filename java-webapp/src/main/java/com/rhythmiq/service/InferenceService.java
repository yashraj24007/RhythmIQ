package com.rhythmiq.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.rhythmiq.model.ECGAnalysisResult;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.Objects;
import java.util.Random;
import java.util.UUID;

/**
 * InferenceService integrates with Python ML model API for real ECG analysis.
 * Falls back to mock predictions if Python API is unavailable.
 */
@Service
public class InferenceService {

    private final Path uploadDir = Paths.get("java-webapp-uploads");
    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;
    private final String pythonApiUrl = "http://localhost:8083/analyze";
    public InferenceService() throws IOException {
        Files.createDirectories(uploadDir);
        this.restTemplate = new RestTemplate();
        this.objectMapper = new ObjectMapper();
    }

    public ECGAnalysisResult analyze(byte[] imageBytes, String originalFilename) throws IOException {
        String storedName = UUID.randomUUID() + "_" + Objects.requireNonNull(originalFilename);
        Path storedPath = uploadDir.resolve(storedName);
        Files.write(storedPath, imageBytes);
        
        // Try to call Python API first, fallback to mock if unavailable
        try {
            return callPythonAPI(imageBytes, originalFilename, storedName, storedPath.toString());
        } catch (Exception e) {
            System.err.println("Python API unavailable, using mock inference: " + e.getMessage());
            return mockInference(storedName, storedPath.toString());
        }
    }
    
    private ECGAnalysisResult callPythonAPI(byte[] imageBytes, String originalFilename, String storedName, String storedPath) {
        try {
            // Prepare multipart request
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);
            
            // Create file resource
            ByteArrayResource fileResource = new ByteArrayResource(imageBytes) {
                @Override
                public String getFilename() {
                    return originalFilename;
                }
            };
            
            // Build multipart body
            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("image", fileResource);
            
            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
            
            // Call Python API
            ResponseEntity<String> response = restTemplate.exchange(
                pythonApiUrl, 
                HttpMethod.POST, 
                requestEntity, 
                String.class
            );
            
            // Parse response
            JsonNode jsonResponse = objectMapper.readTree(response.getBody());
            
            if (jsonResponse.get("success").asBoolean()) {
                // Create result from Python API response
                ECGAnalysisResult result = new ECGAnalysisResult();
                result.setFilename(storedName);
                result.setPredictedClass(jsonResponse.get("predicted_class").asText());
                result.setConfidence(jsonResponse.get("confidence").asDouble());
                result.setSeverity(jsonResponse.get("severity").asText());
                result.setSeverityConfidence(jsonResponse.get("severity_confidence").asDouble());
                result.setImagePath(storedPath);
                result.setAnalysisTime(LocalDateTime.now());
                return result;
            } else {
                throw new RuntimeException("Python API returned error: " + jsonResponse.get("error").asText());
            }
            
        } catch (Exception e) {
            throw new RuntimeException("Failed to call Python API", e);
        }
    }

    private ECGAnalysisResult mockInference(String filename, String path) {
        String[] classes = {"N","S","V","F","Q","M"};
        Random r = new Random();
        String predicted = classes[r.nextInt(classes.length)];
        double confidence = 0.70 + r.nextDouble() * 0.30;
        String severity;
        double sevConf = 0.60 + r.nextDouble() * 0.35;
        switch (predicted) {
            case "V": severity = sevConf > 0.75 ? "severe" : "moderate"; break;
            case "M": severity = sevConf > 0.65 ? "severe" : "moderate"; break;
            case "S": severity = "moderate"; break;
            default: severity = "mild"; break;
        }
        ECGAnalysisResult res = new ECGAnalysisResult();
        res.setFilename(filename);
        res.setPredictedClass(predicted);
        res.setConfidence(confidence);
        res.setSeverity(severity);
        res.setSeverityConfidence(sevConf);
        res.setImagePath(path);
        res.setAnalysisTime(LocalDateTime.now());
        return res;
    }
}
