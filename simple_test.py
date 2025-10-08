#!/usr/bin/env python3
"""
Simple Test Script for RhythmIQ End-to-End Integration
"""

import subprocess
import time
import requests
import os
import json

def test_simple_api():
    """Test just the health endpoint first"""
    try:
        print("🧪 Testing Python API Health Check...")
        response = requests.get("http://localhost:8083/health", timeout=5)
        if response.status_code == 200:
            print("✅ Python API is responding!")
            print(f"📊 Response: {response.json()}")
            return True
        else:
            print(f"❌ API returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to connect to API: {e}")
    return False

def test_with_image():
    """Test with a real ECG image"""
    try:
        api_url = "http://localhost:8083/analyze"
        test_image = "01_data/test/F/F0.png"
        
        if not os.path.exists(test_image):
            print(f"❌ Test image not found: {test_image}")
            return False
            
        print(f"🖼️  Testing with image: {test_image}")
        
        with open(test_image, 'rb') as f:
            files = {'image': ('F0.png', f, 'image/png')}
            response = requests.post(api_url, files=files, timeout=30)
            
        if response.status_code == 200:
            result = response.json()
            print("✅ Image analysis successful!")
            print(f"📈 Predicted class: {result.get('predicted_class')}")
            print(f"🎯 Confidence: {result.get('confidence_percentage')}")
            print(f"📝 Description: {result.get('description')}")
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Image test failed: {e}")
    return False

if __name__ == "__main__":
    print("🚀 Starting RhythmIQ Integration Test")
    print("=" * 40)
    
    # Test 1: Health Check
    if not test_simple_api():
        print("❌ Health check failed. Make sure Python API is running on port 8083")
        exit(1)
    
    # Test 2: Image Analysis
    print("\n" + "=" * 40)
    test_with_image()
    
    print("\n🏁 Test Complete!")