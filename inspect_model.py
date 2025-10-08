"""
Script to inspect the model file and see what's actually stored
"""
import joblib
import os

model_path = '05_trained_models/rythmguard_model.joblib'

if os.path.exists(model_path):
    print(f"🔍 Inspecting model file: {model_path}")
    print("=" * 50)
    
    try:
        model = joblib.load(model_path)
        print(f"Model type: {type(model)}")
        print(f"Model object: {model}")
        
        if hasattr(model, 'keys'):
            print("\nModel appears to be a dictionary with keys:")
            for key in model.keys():
                print(f"  - {key}: {type(model[key])}")
        
        if hasattr(model, 'predict'):
            print("\n✅ Model has predict method")
        else:
            print("\n❌ Model does NOT have predict method")
            
        if isinstance(model, dict) and 'model' in model:
            actual_model = model['model']
            print(f"\nActual model inside dict: {type(actual_model)}")
            if hasattr(actual_model, 'predict'):
                print("✅ Actual model has predict method")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"❌ Model file not found: {model_path}")