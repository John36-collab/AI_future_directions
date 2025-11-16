#!/usr/bin/env python3
"""
Test script to verify that the application can handle OpenCV import errors gracefully
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    
    # Test basic dependencies
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import tensorflow as tf
        print("✅ TensorFlow imported successfully")
    except ImportError as e:
        print(f"❌ TensorFlow import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    # Test OpenCV import with fallback
    try:
        import cv2
        OPENCV_AVAILABLE = True
        print("✅ OpenCV imported successfully")
    except ImportError as e:
        OPENCV_AVAILABLE = False
        print(f"⚠️ OpenCV not available: {e}")
        print("✅ Using PIL-based fallback")
    
    # Test PIL import
    try:
        from PIL import Image
        print("✅ PIL imported successfully")
    except ImportError as e:
        print(f"❌ PIL import failed: {e}")
        return False
    
    # Test tempfile and os
    try:
        import tempfile
        import os
        print("✅ Tempfile and os imported successfully")
    except ImportError as e:
        print(f"❌ Tempfile or os import failed: {e}")
        return False
    
    return True

def test_image_processing():
    """Test image processing functionality"""
    print("\nTesting image processing...")
    
    try:
        from PIL import Image
        import numpy as np
        import tempfile
        import os
        
        # Create a test image
        test_image = Image.new('RGB', (224, 224), color='red')
        
        # Test saving and loading with PIL
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            test_image.save(tmp_file.name)
            temp_path = tmp_file.name
        
        # Test PIL-based preprocessing
        with Image.open(temp_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img = img.resize((224, 224), Image.Resampling.LANCZOS)
            processed_image = np.array(img, dtype=np.float32) / 255.0
        
        # Add batch dimension
        processed_image = np.expand_dims(processed_image, axis=0)
        
        print(f"✅ PIL-based image processing successful")
        print(f"   Processed image shape: {processed_image.shape}")
        print(f"   Image value range: [{processed_image.min():.3f}, {processed_image.max():.3f}]")
        
        # Cleanup
        os.unlink(temp_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Image processing test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Edge AI App Import Test ===\n")
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test image processing
        processing_ok = test_image_processing()
        
        if processing_ok:
            print("\n🎉 All tests passed! The application should work correctly.")
        else:
            print("\n❌ Image processing test failed.")
    else:
        print("\n❌ Import tests failed.")
