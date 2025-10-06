package com.rhythmiq.service;

import com.rhythmiq.model.ECGAnalysisResult;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.Objects;
import java.util.Random;
import java.util.UUID;

/**
 * InferenceService provides a seam to integrate the real Python model.
 * Currently returns mock predictions. Replace mockInference with real call.
 */
@Service
public class InferenceService {

    private final Path uploadDir = Paths.get("java-webapp-uploads");

    public InferenceService() throws IOException {
        Files.createDirectories(uploadDir);
    }

    public ECGAnalysisResult analyze(byte[] imageBytes, String originalFilename) throws IOException {
        String storedName = UUID.randomUUID() + "_" + Objects.requireNonNull(originalFilename);
        Path storedPath = uploadDir.resolve(storedName);
        Files.write(storedPath, imageBytes);
        return mockInference(storedName, storedPath.toString());
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
