import tensorflow as tf
import pandas as pd
import numpy as np
import os
import cv2
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def load_data():
    # Define paths
    train_path = "ml_training/source_images/training_words"
    test_path = "ml_training/source_images/testing_words"
    
    # Load labels
    df_train = pd.read_csv("ml_training/data/training_labels.csv")
    df_test = pd.read_csv("ml_training/data/testing_labels.csv")
    
    # Initialize lists for images
    train_images = []
    test_images = []
    
    # Load and process training images
    print("Loading training images...")
    for element in df_train['IMAGE']:
        abs_path = os.path.join(train_path, element)
        image = load_img(abs_path, target_size=(84, 84))
        image_array = np.array(image, dtype='float32') / 255.0
        train_images.append(image_array)
    
    # Load and process testing images
    print("Loading testing images...")
    for element in df_test['IMAGE']:
        abs_path = os.path.join(test_path, element)
        image = load_img(abs_path, target_size=(84, 84))
        image_array = np.array(image, dtype='float32') / 255.0
        test_images.append(image_array)
    
    # Convert to numpy arrays
    X_train = np.array(train_images)
    X_test = np.array(test_images)
    
    # Create label mappings
    unique_medicines = df_train['MEDICINE_NAME'].unique()
    medicine_to_idx = {medicine: idx for idx, medicine in enumerate(unique_medicines)}
    
    # Save label mappings
    os.makedirs('assets/model', exist_ok=True)
    with open('assets/model/labels.txt', 'w') as f:
        for medicine in unique_medicines:
            f.write(f"{medicine}\n")
    
    # Convert labels to numeric
    y_train = df_train['MEDICINE_NAME'].map(medicine_to_idx).values
    y_test = df_test['MEDICINE_NAME'].map(medicine_to_idx).values
    
    return X_train, X_test, y_train, y_test, len(unique_medicines)

def create_model(num_classes):
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(84, 84, 3)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Conv2D(128, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.4),
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=RMSprop(learning_rate=1e-4),
        metrics=['accuracy']
    )
    
    return model

def train_model():
    print("Loading dataset...")
    X_train, X_test, y_train, y_test, num_classes = load_data()
    
    print("Creating model...")
    model = create_model(num_classes)
    
    print("Training model...")
    history = model.fit(
        X_train, 
        y_train,
        epochs=50,
        validation_split=0.2,
        batch_size=32
    )
    
    print("Evaluating model...")
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Test Accuracy: {accuracy * 100:.2f}%')
    
    # Convert to TFLite
    print("Converting to TFLite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    # Save TFLite model
    os.makedirs('assets/model', exist_ok=True)
    with open('assets/model/model.tflite', 'wb') as f:
        f.write(tflite_model)
    
    print("Model saved as TFLite format in assets/model/model.tflite")
    return history

if __name__ == "__main__":
    train_model()