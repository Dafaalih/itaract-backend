import cv2
import numpy as np
import tensorflow as tf
import base64

model_path = 'model/model1_2024-12-02.h5'
model = tf.keras.models.load_model(model_path)

def decode(img_path):
    with open(img_path, "rb") as file:
        image_data = file.read()

    np_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    output_path = "output_image.jpg"
    with open(output_path, "wb") as file:
        file.write(image)

    print(f"Image saved as {output_path}")
    return image

def crop_pupil(img_path):
    image = decode(img_path)
    
    # Mengonversi gambar ke grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blurred = cv2.GaussianBlur(image, (7, 7), 0)
    
    _, thresh = cv2.threshold(image_blurred, 50, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:  # Pastikan ada kontur yang ditemukan
        pupil_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(pupil_contour)
        pupil_roi = image[y:y+h, x:x+w]
        
        # Ubah ukuran ROI menjadi 150x150
        pupil_roi = cv2.resize(pupil_roi, (150, 150))
        
        # Mengubah menjadi 3 saluran (RGB)
        pupil_roi = cv2.cvtColor(pupil_roi, cv2.COLOR_GRAY2BGR)  # Mengubah menjadi 3 saluran
        
        return pupil_roi
    else:
        raise ValueError("Tidak ada kontur yang ditemukan.")

def cataract_prediction(image):
    # Normalisasi gambar
    image = image / 255.0  
    image = np.expand_dims(image, axis=0)  # Menambahkan dimensi batch
    
    predictions = model.predict(image)
    class_names = ['katarak_immatur', 'katarak_matur', 'mata_normal']  
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class = class_names[predicted_class_index]

    return predicted_class