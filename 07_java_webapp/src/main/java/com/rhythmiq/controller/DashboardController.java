package com.rhythmiq.controller;

import com.rhythmiq.model.User;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.time.LocalDateTime;

/**
 * Dashboard controller
 */
@Controller
public class DashboardController {

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        // Create a demo user for display purposes
        User user = new User("demo", "demo123", "demo@rhythmiq.com", "Demo User");
        user.setId(1L);
        
        model.addAttribute("user", user);
        model.addAttribute("currentTime", LocalDateTime.now());
        
        // Add some mock statistics
        model.addAttribute("totalAnalyses", 127);
        model.addAttribute("todayAnalyses", 12);
        model.addAttribute("accuracy", "83.3%");
        model.addAttribute("avgConfidence", "87.2%");
        
        return "dashboard";
    }

    @GetMapping("/profile")
    public String profile(Model model) {
        // Create a demo user for display purposes
        User user = new User("demo", "demo123", "demo@rhythmiq.com", "Demo User");
        user.setId(1L);
        
        model.addAttribute("user", user);
        return "profile";
    }

    @GetMapping("/history")
    public String history(Model model) {
        // Create a demo user for display purposes
        User user = new User("demo", "demo123", "demo@rhythmiq.com", "Demo User");
        user.setId(1L);
        
        model.addAttribute("user", user);
        return "history";
    }
}
