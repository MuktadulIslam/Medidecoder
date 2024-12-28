import tensorflow as tf
import numpy as np
import cv2

class MLHandler:
    def __init__(self):
        # Load TFLite model
        self.interpreter = tf.lite.Interpreter(model_path='assets/model/model.tflite')
        self.interpreter.allocate_tensors()
        
        # Get input and output tensors
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # Load labels
        self.labels = []
        try:
            with open('assets/model/labels.txt', 'r') as f:
                self.labels = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print("Warning: labels.txt not found")
    
    def preprocess_image(self, image):
        """Preprocess image for model input"""
        # Resize to model input size (84x84 as per your training)
        image = cv2.resize(image, (84, 84))
        
        # Convert to RGB if needed
        if len(image.shape) == 2:  # If grayscale
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:  # If RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        
        # Normalize pixel values
        image = image.astype(np.float32) / 255.0
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        return image
    
    def predict(self, image):
        """Predict medicine name from image"""
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Set input tensor
        self.interpreter.set_tensor(self.input_details[0]['index'], processed_image)
        
        # Run inference
        self.interpreter.invoke()
        
        # Get prediction
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        predicted_idx = np.argmax(output_data[0])
        
        # Return predicted label
        if predicted_idx < len(self.labels):
            return self.labels[predicted_idx]
        return "Unknown Medicine"