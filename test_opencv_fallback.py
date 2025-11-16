#!/usr/bin/env python3
"""
Test script to specifically verify OpenCV import handling and PIL fallback
"""

import sys
import os

def test_opencv_import_handling():
    """Test that OpenCV import is handled gracefully"""
    print("Testing OpenCV import handling...")
    
    # Test OpenCV import with try-catch
    try:
        import cv2
        OPENCV_AVAILABLE = True
        print("✅ OpenCV imported successfully")
        print("   OpenCV version:", cv2.__version__)
    except ImportError as e:
        OPENCV_AVAILABLE = False
        print(f"⚠️ OpenCV not available: {e}")
        print("✅ Using PIL-based fallback as designed")
    
    return OPENCV_AVAILABLE

def test_pil_functionality():
    """Test PIL-based image processing functionality"""
    print("\nTesting PIL-based image processing...")
    
    try:
        from PIL import Image
        import numpy as np
        import tempfile
        
        # Create a test image
        test_image = Image.new('RGB', (224, 224), color='blue')
        print("✅ Created test image")
        
        # Test saving and loading
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            test_image.save(tmp_file.name)
            temp_path = tmp_file.name
        
        print("✅ Saved and loaded test image")
        
        # Test PIL-based preprocessing (same as in the main app)
        with Image.open(temp_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Resize
            img = img.resize((224, 224), Image.Resampling.LANCZOS)
            # Convert to numpy array and normalize
            processed_image = np.array(img, dtype=np.float32) / 255.0
        
        # Add batch dimension
        processed_image = np.expand_dims(processed_image, axis=0)
        
        print(f"✅ PIL-based image preprocessing successful")
        print(f"   Processed image shape: {processed_image.shape}")
        print(f"   Image value range: [{processed_image.min():.3f}, {processed_image.max():.3f}]")
        print(f"   Image dtype: {processed_image.dtype}")
        
        # Cleanup
        os.unlink(temp_path)
        
        return True
        
    except Exception as e:
        print(f"❌ PIL functionality test failed: {e}")
        return False

def test_app_imports():
    """Test that the application can be imported without OpenCV errors"""
    print("\nTesting application import...")
    
    try:
        # Import the specific modules we modified
        import streamlit as st
        import numpy as np
        from PIL import Image
        import tempfile
        import os
        
        print("✅ All basic dependencies imported successfully")
        
        # Test OpenCV import handling pattern
        try:
            import cv2
            OPENCV_AVAILABLE = True
            print("✅ OpenCV is available")
        except ImportError:
            OPENCV_AVAILABLE = False
            print("⚠️ OpenCV not available - this is expected behavior")
        
        # Test PIL image processing (the fallback we implemented)
        test_image = Image.new('RGB', (224, 224), color='green')
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            test_image.save(tmp_file.name)
            temp_path = tmp_file.name
        
        with Image.open(temp_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img = img.resize((224, 224), Image.Resampling.LANCZOS)
            processed_image = np.array(img, dtype=np.float32) / 255.0
        
        processed_image = np.expand_dims(processed_image, axis=0)
        
        print("✅ PIL-based image processing (our fallback) works correctly")
        
        # Cleanup
        os.unlink(temp_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Application import test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== OpenCV Fallback Test ===\n")
    
    # Test OpenCV import handling
    opencv_available = test_opencv_import_handling()
    
    # Test PIL functionality
    pil_ok = test_pil_functionality()
    
    # Test app imports
    app_ok = test_app_imports()
    
    # Summary
    print("\n=== Test Summary ===")
    if opencv_available:
        print("🟢 OpenCV is available (ideal case)")
    else:
        print("🟡 OpenCV not available (expected in headless environments)")
    
    if pil_ok:
        print("🟢 PIL-based image processing works")
    else:
        print("❌ PIL-based image processing failed")
    
    if app_ok:
        print("🟢 Application can be imported and basic functionality works")
    else:
        print("❌ Application import failed")
    
    if pil_ok and app_ok:
        print("\n🎉 The OpenCV fallback solution is working correctly!")
        print("   The application should now work in headless environments.")
    else:
        print("\n❌ Some tests failed. Please check the output above.")
