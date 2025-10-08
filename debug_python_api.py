"""
Debug script to test the Python API directly and see what's happening
"""
import requests
import json
import os

def test_debug():
    print("🔍 Debugging Python API")
    print("=" * 50)
    
    # Test model info first
    try:
        model_info = requests.get("http://localhost:8083/model-info")
        print("Model Info:", model_info.json())
        print()
    except Exception as e:
        print(f"Error getting model info: {e}")
    
    # Test with actual file
    test_file = '01_data/test/N/N52879.png'
    if os.path.exists(test_file):
        print(f"Testing with file: {test_file}")
        
        try:
            with open(test_file, 'rb') as f:
                files = {'image': f}
                response = requests.post("http://localhost:8083/analyze", files=files)
                
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.headers.get('content-type', '').startswith('application/json'):
                result = response.json()
                print("\n📊 Parsed Result:")
                for key, value in result.items():
                    print(f"  {key}: {value}")
            
        except Exception as e:
            print(f"Error in API call: {e}")
    else:
        print(f"Test file not found: {test_file}")

if __name__ == "__main__":
    test_debug()