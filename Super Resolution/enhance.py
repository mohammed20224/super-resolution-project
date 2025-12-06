import cv2
import os
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
import numpy as np

class ImageEnhancer:
    def __init__(self):
        """Initialize Real-ESRGAN model"""
        self.model = None
        self.upsampler = None
        
    def load_model(self):
        """Load Real-ESRGAN model"""
        try:
            # Define model
            model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
            
            # Model path
            model_path = 'models/RealESRGAN_x4plus.pth'
            
            # Check if model exists, if not download it
            if not os.path.exists(model_path):
                print("Model not found. Downloading Real-ESRGAN model...")
                os.makedirs('models', exist_ok=True)
                # The model will be downloaded automatically by RealESRGANer
                model_path = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth'
            
            # Initialize upsampler
            self.upsampler = RealESRGANer(
                scale=4,
                model_path=model_path,
                model=model,
                tile=0,
                tile_pad=10,
                pre_pad=0,
                half=False  # Set to True if you have GPU with FP16 support
            )
            
            print("✓ Model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
            return False
    
    def enhance_image(self, input_path, output_path):
        """
        Enhance image using Real-ESRGAN
        
        Args:
            input_path: Path to input image
            output_path: Path to save enhanced image
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load model if not loaded
            if self.upsampler is None:
                if not self.load_model():
                    return False
            
            # Read image
            img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
            if img is None:
                print(f"✗ Could not read image: {input_path}")
                return False
            
            print(f"Processing image... Original size: {img.shape[1]}x{img.shape[0]}")
            
            # Enhance image
            output, _ = self.upsampler.enhance(img, outscale=4)
            
            # Save output
            cv2.imwrite(output_path, output)
            print(f"✓ Enhanced image saved! New size: {output.shape[1]}x{output.shape[0]}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error enhancing image: {str(e)}")
            return False


def test_enhancer():
    """Test function for the enhancer"""
    enhancer = ImageEnhancer()
    
    # Test with a sample image
    input_path = "uploads/test.jpg"
    output_path = "outputs/test_enhanced.jpg"
    
    if os.path.exists(input_path):
        enhancer.enhance_image(input_path, output_path)
    else:
        print("Please add a test image to uploads/test.jpg")


if __name__ == "__main__":
    test_enhancer()
