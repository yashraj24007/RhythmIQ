package com.rhythmiq.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.rhythmiq.model.ECGAnalysisResult;
import com.rhythmiq.service.ECGAnalysisService;

/**
 * Main Web Controller for RhythmIQ Application
 */
@Controller
public class ECGController {

    @Autowired
    private ECGAnalysisService ecgAnalysisService;

    /**
     * Home page
     */
    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("title", "RhythmIQ - ECG Analysis System");
        return "index";
    }

    /**
     * Upload page
     */
    @GetMapping("/upload")
    public String uploadPage(Model model) {
        model.addAttribute("title", "Upload ECG Image");
        return "upload";
    }

    /**
     * Handle file upload and analysis
     */
    @PostMapping("/analyze")
    public String analyzeECG(@RequestParam("file") MultipartFile file,
                            RedirectAttributes redirectAttributes,
                            Model model) {
        
        // Validate file
        if (!ecgAnalysisService.isValidECGImage(file)) {
            redirectAttributes.addFlashAttribute("error", 
                "Please upload a valid ECG image file (PNG, JPG, JPEG)");
            return "redirect:/upload";
        }

        try {
            // Analyze ECG
            ECGAnalysisResult result = ecgAnalysisService.analyzeECG(file);
            
            // Add result to model
            model.addAttribute("title", "ECG Analysis Results");
            model.addAttribute("result", result);
            
            return "results";
            
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("error", 
                "Error analyzing ECG image: " + e.getMessage());
            return "redirect:/upload";
        }
    }

    /**
     * About page
     */
    @GetMapping("/about")
    public String about(Model model) {
        model.addAttribute("title", "About RhythmIQ");
        return "about";
    }

    /**
     * API Documentation page
     */
    @GetMapping("/api-docs")
    public String apiDocs(Model model) {
        model.addAttribute("title", "API Documentation");
        return "api-docs";
    }
}