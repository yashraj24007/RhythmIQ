package com.rhythmiq.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClients;

@Configuration
public class SupabaseConfig {
    
    @Value("${supabase.url:https://your-project.supabase.co}")
    private String supabaseUrl;
    
    @Value("${supabase.key:your-anon-key}")
    private String supabaseKey;
    
    @Bean
    public CloseableHttpClient httpClient() {
        return HttpClients.createDefault();
    }
    
    public String getSupabaseUrl() {
        return supabaseUrl;
    }
    
    public String getSupabaseKey() {
        return supabaseKey;
    }
}
