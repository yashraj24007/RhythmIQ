package com.rhythmiq.service;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.rhythmiq.config.SupabaseConfig;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.core5.http.io.entity.StringEntity;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class SupabaseAuthService {
    
    @Autowired
    private SupabaseConfig supabaseConfig;
    
    @Autowired
    private CloseableHttpClient httpClient;
    
    private final Gson gson = new Gson();
    
    /**
     * Sign up a new user with email and password
     */
    public JsonObject signUp(String email, String password) {
        try {
            String url = supabaseConfig.getSupabaseUrl() + "/auth/v1/signup";
            HttpPost request = new HttpPost(url);
            
            // Set headers
            request.setHeader("apikey", supabaseConfig.getSupabaseKey());
            request.setHeader("Content-Type", "application/json");
            
            // Create request body
            JsonObject body = new JsonObject();
            body.addProperty("email", email);
            body.addProperty("password", password);
            
            request.setEntity(new StringEntity(gson.toJson(body)));
            
            // Execute request
            return httpClient.execute(request, response -> {
                String responseBody = EntityUtils.toString(response.getEntity());
                return gson.fromJson(responseBody, JsonObject.class);
            });
        } catch (Exception e) {
            JsonObject error = new JsonObject();
            error.addProperty("error", e.getMessage());
            return error;
        }
    }
    
    /**
     * Sign in an existing user
     */
    public JsonObject signIn(String email, String password) {
        try {
            String url = supabaseConfig.getSupabaseUrl() + "/auth/v1/token?grant_type=password";
            HttpPost request = new HttpPost(url);
            
            // Set headers
            request.setHeader("apikey", supabaseConfig.getSupabaseKey());
            request.setHeader("Content-Type", "application/json");
            
            // Create request body
            JsonObject body = new JsonObject();
            body.addProperty("email", email);
            body.addProperty("password", password);
            
            request.setEntity(new StringEntity(gson.toJson(body)));
            
            // Execute request
            return httpClient.execute(request, response -> {
                String responseBody = EntityUtils.toString(response.getEntity());
                return gson.fromJson(responseBody, JsonObject.class);
            });
        } catch (Exception e) {
            JsonObject error = new JsonObject();
            error.addProperty("error", e.getMessage());
            return error;
        }
    }
    
    /**
     * Verify a JWT token
     */
    public JsonObject verifyToken(String token) {
        try {
            String url = supabaseConfig.getSupabaseUrl() + "/auth/v1/user";
            HttpPost request = new HttpPost(url);
            
            // Set headers
            request.setHeader("apikey", supabaseConfig.getSupabaseKey());
            request.setHeader("Authorization", "Bearer " + token);
            
            // Execute request
            return httpClient.execute(request, response -> {
                String responseBody = EntityUtils.toString(response.getEntity());
                return gson.fromJson(responseBody, JsonObject.class);
            });
        } catch (Exception e) {
            JsonObject error = new JsonObject();
            error.addProperty("error", e.getMessage());
            return error;
        }
    }
    
    /**
     * Sign out (invalidate token on client side)
     */
    public boolean signOut(String token) {
        try {
            String url = supabaseConfig.getSupabaseUrl() + "/auth/v1/logout";
            HttpPost request = new HttpPost(url);
            
            // Set headers
            request.setHeader("apikey", supabaseConfig.getSupabaseKey());
            request.setHeader("Authorization", "Bearer " + token);
            
            // Execute request
            httpClient.execute(request, response -> {
                return response.getCode() == 204;
            });
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
