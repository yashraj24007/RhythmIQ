package com.rhythmiq.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.ui.Model;

/**
 * Login Controller for RhythmIQ Application
 * 
 * Handles user authentication routes.
 * Ready for Supabase integration.
 */
@Controller
public class LoginController {
    
    @GetMapping("/login")
    public String showLoginPage(Model model) {
        return "login";
    }
    
    @PostMapping("/login")
    public String handleLogin(
            @RequestParam String email, 
            @RequestParam String password,
            @RequestParam(required = false) String remember,
            Model model) {
        
        // TODO: Integrate with Supabase authentication
        // For now, redirect to home page
        
        System.out.println("Login attempt for email: " + email);
        
        // In production, this would validate against Supabase
        // and handle authentication properly
        
        return "redirect:/";
    }
}