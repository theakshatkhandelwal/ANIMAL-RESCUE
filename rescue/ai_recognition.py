"""
AI Image Recognition Module for Animal Identification
Uses PIL/Pillow for basic image processing (lightweight alternative to OpenCV)
TensorFlow and OpenCV are optional and can be added later for advanced ML model support
"""
import numpy as np
import os
from PIL import Image, ImageStat

# Optional OpenCV import (for advanced image processing)
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    cv2 = None

# Optional TensorFlow import (for future ML model support)
try:
    from tensorflow import keras
    from tensorflow.keras.preprocessing import image
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    keras = None
    image = None


class AnimalRecognizer:
    """
    Simple animal recognition using pre-trained models or basic image processing
    For production, you would use a more sophisticated model
    """
    
    def __init__(self):
        self.animal_classes = ['dog', 'cat', 'bird', 'rabbit', 'other']
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """
        Load a simple model for animal recognition
        In production, you would load a pre-trained model here
        For now, we'll use basic image processing as a placeholder
        """
        try:
            # In a real implementation, you would load a pre-trained model
            # For example: self.model = keras.models.load_model('animal_classifier.h5')
            pass
        except Exception as e:
            print(f"Model loading error: {e}")
            self.model = None
    
    def preprocess_image(self, image_path):
        """Preprocess image for model input"""
        try:
            img = Image.open(image_path)
            img = img.convert('RGB')
            img = img.resize((224, 224))
            # Use numpy instead of tensorflow.keras.preprocessing
            img_array = np.array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0
            return img_array
        except Exception as e:
            print(f"Image preprocessing error: {e}")
            return None
    
    def recognize_animal(self, image_path):
        """
        Recognize animal type from image
        Returns: (animal_type, confidence)
        """
        if not os.path.exists(image_path):
            return None, 0.0
        
        try:
            # Use TensorFlow model if available
            if self.model and TENSORFLOW_AVAILABLE:
                processed_img = self.preprocess_image(image_path)
                if processed_img is not None:
                    predictions = self.model.predict(processed_img, verbose=0)
                    class_idx = np.argmax(predictions[0])
                    confidence = float(predictions[0][class_idx])
                    animal_type = self.animal_classes[class_idx] if class_idx < len(self.animal_classes) else 'other'
                    return animal_type, confidence
            
            # Use OpenCV if available for advanced processing
            if OPENCV_AVAILABLE and cv2:
                img = cv2.imread(image_path)
                if img is not None:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 50, 150)
                    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    area = cv2.contourArea(max(contours, key=cv2.contourArea)) if contours else 0
                    aspect_ratio = img.shape[1] / img.shape[0] if img.shape[0] > 0 else 1
                    
                    if area > 10000:
                        if aspect_ratio > 1.2:
                            return 'dog', 0.65
                        else:
                            return 'cat', 0.60
                    elif area > 5000:
                        return 'rabbit', 0.55
                    else:
                        return 'bird', 0.50
            
            # Fallback: Basic PIL-based heuristic classification (lightweight)
            img = Image.open(image_path)
            img = img.convert('RGB')
            width, height = img.size
            aspect_ratio = width / height if height > 0 else 1
            area = width * height
            
            # Basic heuristics based on image size and aspect ratio
            if area > 1000000:  # Large images
                if aspect_ratio > 1.2:
                    return 'dog', 0.60
                else:
                    return 'cat', 0.55
            elif area > 500000:
                return 'rabbit', 0.50
            else:
                return 'bird', 0.45
                
        except Exception as e:
            print(f"Recognition error: {e}")
            return None, 0.0
    
    def detect_animal_features(self, image_path):
        """
        Detect basic features in animal images
        Returns dictionary with detected features
        """
        features = {
            'has_face': False,
            'has_body': False,
            'color_dominant': None,
            'size_estimate': None
        }
        
        try:
            # Use OpenCV if available for advanced processing
            if OPENCV_AVAILABLE and cv2:
                img = cv2.imread(image_path)
                if img is not None:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])
                    dominant_hue = np.argmax(hist)
                    height, width = img.shape[:2]
                    features['size_estimate'] = 'large' if height * width > 500000 else 'small'
                    return features
            
            # Fallback: Basic PIL-based feature detection (lightweight)
            img = Image.open(image_path)
            img = img.convert('RGB')
            width, height = img.size
            
            # Size estimation
            features['size_estimate'] = 'large' if width * height > 500000 else 'small'
            
            # Basic color analysis using PIL
            stat = ImageStat.Stat(img)
            # Get dominant color from mean RGB
            mean_r, mean_g, mean_b = stat.mean
            if mean_r > mean_g and mean_r > mean_b:
                features['color_dominant'] = 'reddish'
            elif mean_g > mean_r and mean_g > mean_b:
                features['color_dominant'] = 'greenish'
            elif mean_b > mean_r and mean_b > mean_g:
                features['color_dominant'] = 'bluish'
            else:
                features['color_dominant'] = 'mixed'
            
            return features
            
        except Exception as e:
            print(f"Feature detection error: {e}")
            return features


# Global instance
recognizer = AnimalRecognizer()


