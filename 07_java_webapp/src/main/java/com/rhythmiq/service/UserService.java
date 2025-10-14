package com.rhythmiq.service;

import com.rhythmiq.model.User;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * User service for managing user accounts
 * In-memory storage for demo purposes
 */
@Service
public class UserService {
    
    private final Map<String, User> users = new HashMap<>();
    private Long nextId = 1L;

    public UserService() {
        // Create default demo users
        createDefaultUsers();
    }

    private void createDefaultUsers() {
        // Demo user - ONLY user allowed for now (later will integrate with Supabase)
        User demo = new User("demo", "demo123", "demo@rhythmiq.com", "Demo User");
        demo.setId(nextId++);
        users.put(demo.getUsername(), demo);
    }

    public Optional<User> findByUsername(String username) {
        return Optional.ofNullable(users.get(username));
    }

    public boolean validateCredentials(String username, String password) {
        return findByUsername(username)
                .map(user -> user.getPassword().equals(password) && user.isEnabled())
                .orElse(false);
    }

    public User authenticate(String username, String password) {
        Optional<User> userOpt = findByUsername(username);
        if (userOpt.isPresent() && validateCredentials(username, password)) {
            User user = userOpt.get();
            user.setLastLogin(LocalDateTime.now());
            return user;
        }
        return null;
    }

    public User createUser(String username, String password, String email, String fullName) {
        if (users.containsKey(username)) {
            return null; // User already exists
        }

        User newUser = new User(username, password, email, fullName);
        newUser.setId(nextId++);
        users.put(username, newUser);
        return newUser;
    }

    public boolean existsByUsername(String username) {
        return users.containsKey(username);
    }
}
