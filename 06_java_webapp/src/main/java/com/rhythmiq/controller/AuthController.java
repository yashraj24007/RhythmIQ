package com.rhythmiq.controller;

import com.rhythmiq.model.User;
import com.rhythmiq.service.UserService;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

/**
 * Authentication controller - simple demo authentication (fast!)
 */
@Controller
public class AuthController {

    private final UserService userService;

    public AuthController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/login")
    public String loginPage(@RequestParam(required = false) String error,
                           @RequestParam(required = false) String logout,
                           @RequestParam(required = false) String registration_disabled,
                           Model model) {
        if (error != null) {
            model.addAttribute("error", "Invalid username or password. Use demo/demo123");
        }
        if (logout != null) {
            model.addAttribute("message", "You have been logged out successfully");
        }
        if (registration_disabled != null) {
            model.addAttribute("info", "Registration is disabled. Please use demo account.");
        }
        return "login";
    }

    @PostMapping("/login")
    public String login(@RequestParam String username,
                       @RequestParam String password,
                       HttpSession session,
                       Model model) {
        // Simple demo authentication - fast startup!
        User user = userService.authenticate(username, password);
        if (user != null) {
            session.setAttribute("user", user);
            return "redirect:/dashboard";
        } else {
            model.addAttribute("error", "Invalid username or password. Use demo/demo123");
            return "login";
        }
    }

    @GetMapping("/register")
    public String registerPage(Model model) {
        return "register";
    }

    @PostMapping("/register")
    public String register(@RequestParam String email,
                          @RequestParam String password,
                          @RequestParam String confirmPassword,
                          HttpSession session,
                          Model model) {
        
        // Validate passwords match
        if (!password.equals(confirmPassword)) {
            model.addAttribute("error", "Passwords do not match");
            return "register";
        }
        
        // Simple registration disabled - use demo account
        model.addAttribute("error", "Registration is currently disabled. Please use the demo account: demo/demo123");
        return "register";
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate();
        return "redirect:/login?logout=true";
    }
}
