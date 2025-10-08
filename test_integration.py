"""
Simple test script to check Python-Java integration
"""
import requests
import json

# Test the Python API directly
def test_python_api():
    try:
        # Test health endpoint
        health_response = requests.get("http://localhost:8083/health")
        print("Python API Health:", health_response.status_code, health_response.json())
        
        # Test analyze endpoint with a file
        files = {'image': open('01_data/test/N/N52879.png', 'rb')}
        analyze_response = requests.post("http://localhost:8083/analyze", files=files)
        
        if analyze_response.status_code == 200:
            result = analyze_response.json()
            print("\n🎉 PYTHON API WORKING!")
            print(f"Predicted Class: {result.get('predicted_class')}")
            print(f"Confidence: {result.get('confidence_percentage')}")
            print(f"Severity: {result.get('severity')}")
            print(f"Description: {result.get('description')}")
            return True
        else:
            print(f"Error: {analyze_response.status_code} - {analyze_response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing Python API: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing RhythmIQ Python API Integration")
    print("=" * 50)
    
    if test_python_api():
        print("\n✅ Python API is working correctly!")
        print("The issue is in Java-Python communication.")
    else:
        print("\n❌ Python API has issues.")