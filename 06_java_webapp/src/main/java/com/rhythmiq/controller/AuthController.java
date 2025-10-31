package com.rhythmiq.controller;

import com.google.gson.JsonObject;
import com.rhythmiq.model.User;
import com.rhythmiq.service.UserService;
import com.rhythmiq.service.SupabaseAuthService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

/**
 * Authentication controller for login and registration with Supabase
 */
@Controller
public class AuthController {

    private final UserService userService;
    
    @Autowired
    private SupabaseAuthService supabaseAuthService;

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
        // Try Supabase authentication
        JsonObject result = supabaseAuthService.signIn(username, password);
        
        if (result.has("access_token")) {
            // Successful login
            String accessToken = result.get("access_token").getAsString();
            JsonObject userObj = result.getAsJsonObject("user");
            
            User user = new User();
            user.setUsername(userObj.get("email").getAsString());
            user.setEmail(userObj.get("email").getAsString());
            
            session.setAttribute("user", user);
            session.setAttribute("access_token", accessToken);
            return "redirect:/dashboard";
        } else if (result.has("error")) {
            model.addAttribute("error", "Invalid email or password");
            return "login";
        } else {
            // Fallback to demo account
            User user = userService.authenticate(username, password);
            if (user != null) {
                session.setAttribute("user", user);
                return "redirect:/dashboard";
            } else {
                model.addAttribute("error", "Invalid username or password");
                return "login";
            }
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
        
        // Register with Supabase
        JsonObject result = supabaseAuthService.signUp(email, password);
        
        if (result.has("access_token")) {
            // Successful registration - auto login
            String accessToken = result.get("access_token").getAsString();
            JsonObject userObj = result.getAsJsonObject("user");
            
            User user = new User();
            user.setUsername(userObj.get("email").getAsString());
            user.setEmail(userObj.get("email").getAsString());
            
            session.setAttribute("user", user);
            session.setAttribute("access_token", accessToken);
            
            model.addAttribute("message", "Registration successful! Please check your email to verify your account.");
            return "redirect:/dashboard";
        } else if (result.has("error")) {
            String error = result.get("error").getAsString();
            model.addAttribute("error", error.contains("already registered") ? 
                "Email already registered. Please login instead." : 
                "Registration failed. Please try again.");
            return "register";
        } else {
            model.addAttribute("error", "Registration failed. Please try again.");
            return "register";
        }
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        // Get access token and sign out from Supabase
        String accessToken = (String) session.getAttribute("access_token");
        if (accessToken != null) {
            supabaseAuthService.signOut(accessToken);
        }
        session.invalidate();
        return "redirect:/login?logout=true";
    }
}
