#!/usr/bin/env python3
"""
Test script to verify Python API predictions with actual ECG images
"""

import requests
import json
import os

def test_python_api():
    """Test the Python API with a known ECG image"""
    
    # API endpoint
    api_url = "http://localhost:8083/analyze"
    health_url = "http://localhost:8083/health"
    
    print("🧪 Testing RhythmIQ Python API Integration")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test 2: ECG Analysis with F-class image (should predict 'F')
    print("\n2️⃣ Testing ECG Analysis...")
    test_image_path = "01_data/test/F/F0.png"
    
    if not os.path.exists(test_image_path):
        print(f"❌ Test image not found: {test_image_path}")
        return
    
    print(f"📄 Using test image: {test_image_path}")
    print("📊 Expected class: F (Fusion of ventricular and normal beat)")
    
    try:
        with open(test_image_path, 'rb') as image_file:
            files = {'image': ('F0.png', image_file, 'image/png')}
            
            print("🚀 Sending request to Python API...")
            response = requests.post(api_url, files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ API Response received successfully!")
                print(f"📈 Predicted class: {result.get('predicted_class', 'Unknown')}")
                print(f"🎯 Confidence: {result.get('confidence', 0):.2%}")
                
                # Check if prediction matches expected class
                predicted_class = result.get('predicted_class', '')
                if predicted_class == 'F':
                    print("🎉 PREDICTION CORRECT! Model is working as expected.")
                else:
                    print(f"⚠️  PREDICTION MISMATCH! Expected 'F', got '{predicted_class}'")
                
                # Show detailed predictions if available
                if 'predictions' in result:
                    print("\n📊 Detailed Predictions:")
                    for class_name, prob in result['predictions'].items():
                        print(f"   {class_name}: {prob:.2%}")
                        
            else:
                print(f"❌ API request failed: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"❌ API test error: {e}")
        return
    
    # Test 3: Test with different class (M-class)
    print("\n3️⃣ Testing with M-class image...")
    test_image_m = "01_data/test/M/M0.png" if os.path.exists("01_data/test/M/M0.png") else None
    
    if test_image_m:
        print(f"📄 Using test image: {test_image_m}")
        print("📊 Expected class: M (Myocardial infarction)")
        
        try:
            with open(test_image_m, 'rb') as image_file:
                files = {'image': ('M0.png', image_file, 'image/png')}
                response = requests.post(api_url, files=files, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    predicted_class = result.get('predicted_class', '')
                    print(f"📈 Predicted class: {predicted_class}")
                    print(f"🎯 Confidence: {result.get('confidence', 0):.2%}")
                    
                    if predicted_class == 'M':
                        print("🎉 PREDICTION CORRECT for M-class!")
                    else:
                        print(f"⚠️  Different prediction: Expected 'M', got '{predicted_class}'")
                else:
                    print(f"❌ M-class test failed: {response.status_code}")
        except Exception as e:
            print(f"❌ M-class test error: {e}")
    else:
        print("📄 M-class test image not found, skipping...")
    
    print("\n🏁 API Testing Complete!")

if __name__ == "__main__":
    test_python_api()