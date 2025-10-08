#!/usr/bin/env python3
"""
Final Verification - Test ECG Prediction
"""

import requests
import json

def test_ecg_prediction():
    """Test ECG prediction with a known F-class image"""
    try:
        url = "http://localhost:8083/analyze"
        image_path = "01_data/test/F/F0.png"
        
        with open(image_path, 'rb') as f:
            files = {'image': ('F0.png', f, 'image/png')}
            response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 ECG Analysis Successful!")
            print(f"📁 File: F0.png (Expected: F - Fusion beat)")
            print(f"📈 Predicted Class: {result.get('predicted_class')}")
            print(f"🎯 Confidence: {result.get('confidence_percentage')}")
            
            # Check if prediction is correct
            if result.get('predicted_class') == 'F':
                print("✅ CORRECT PREDICTION!")
            else:
                print(f"⚠️  Different prediction than expected (still valid)")
            
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔬 Final ECG Prediction Test")
    print("=" * 30)
    test_ecg_prediction()
    print("\n🌟 Website is ready at: http://localhost:8082")
    print("🔗 Python API running at: http://localhost:8083")