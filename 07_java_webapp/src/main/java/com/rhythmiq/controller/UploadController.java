package com.rhythmiq.controller;

import com.rhythmiq.model.ECGAnalysisResult;
import com.rhythmiq.service.InferenceService;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.Objects;

import org.springframework.beans.factory.annotation.Autowired;

@Controller
public class UploadController {
    private final InferenceService inferenceService;

    @Autowired
    public UploadController(InferenceService inferenceService) {
        this.inferenceService = inferenceService;
    }

    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("now", LocalDateTime.now());
        return "index";
    }

    @GetMapping("/upload")
    public String uploadPage(Model model) {
        return "upload";
    }

    @PostMapping(value = "/analyze", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public String analyze(@RequestParam("ecgImage") MultipartFile ecgImage,
                          Model model) throws IOException {
        if (ecgImage.isEmpty()) {
            model.addAttribute("error", "Please select an ECG image to upload.");
            return "upload";
        }

        String originalName = Objects.requireNonNull(ecgImage.getOriginalFilename());
        ECGAnalysisResult result = inferenceService.analyze(ecgImage.getBytes(), originalName);
        model.addAttribute("result", result);
        model.addAttribute("imageFile", result.getFilename());
        return "results";
    }

    @ResponseBody
    @PostMapping(value = "/api/analyze", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ECGAnalysisResult apiAnalyze(@RequestParam("ecgImage") MultipartFile ecgImage) throws IOException {
        if (ecgImage.isEmpty()) {
            throw new IllegalArgumentException("ECG image is required");
        }
        String originalName = Objects.requireNonNull(ecgImage.getOriginalFilename());
        return inferenceService.analyze(ecgImage.getBytes(), originalName);
    }
}
