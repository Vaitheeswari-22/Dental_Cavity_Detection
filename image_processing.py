import os
import cv2
import numpy as np
import tensorflow as tf


# ==========================================================
# Processed Folder
# ==========================================================

PROCESSED_FOLDER = "static/processed"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


# ==========================================================
# Model Configuration
# ==========================================================

MODEL_PATH = "dental_model.keras"
IMG_SIZE = (224, 224)

_model = None


# ==========================================================
# Load Model
# ==========================================================

def get_model():

    global _model

    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)

    return _model



# ==========================================================
# Prediction Function
# ==========================================================

def predict_with_model(image_path):

    model = get_model()

    img = tf.keras.utils.load_img(
        image_path,
        target_size=IMG_SIZE
    )

    arr = tf.keras.utils.img_to_array(img)

    arr = arr / 255.0

    arr = np.expand_dims(arr, axis=0)


    prediction = model.predict(
        arr,
        verbose=0
    )[0][0]


    print("RAW PREDICTION:", prediction)


    if prediction < 0.40:

        predicted_class = "normal"

        confidence = (1 - prediction) * 100

        status = "Normal Tooth"


    else:

        predicted_class = "cavity"

        confidence = prediction * 100

        status = "Cavity Detected"


    print("RESULT:", predicted_class)


    return status, round(float(confidence), 2)




# ==========================================================
# Main Detection Function
# ==========================================================

def detect_cavity(image_path):


    filename = os.path.basename(image_path)


    img = cv2.imread(image_path)


    if img is None:
        raise Exception("Image not found")



    # ------------------------------
    # Gray Image
    # ------------------------------

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )


    gray_path = os.path.join(
        PROCESSED_FOLDER,
        "gray_" + filename
    )


    cv2.imwrite(
        gray_path,
        gray
    )



    # ------------------------------
    # Threshold
    # ------------------------------

    _, threshold = cv2.threshold(
        gray,
        120,
        255,
        cv2.THRESH_BINARY
    )


    threshold_path = os.path.join(
        PROCESSED_FOLDER,
        "threshold_" + filename
    )


    cv2.imwrite(
        threshold_path,
        threshold
    )



    # ------------------------------
    # Edge Detection
    # ------------------------------

    edge = cv2.Canny(
        gray,
        100,
        200
    )


    edge_path = os.path.join(
        PROCESSED_FOLDER,
        "edge_" + filename
    )


    cv2.imwrite(
        edge_path,
        edge
    )



    # ------------------------------
    # Final Image
    # ------------------------------

    final = img.copy()



    # ------------------------------
    # AI Prediction
    # ------------------------------

    status, percentage = predict_with_model(
        image_path
    )



    # ------------------------------
    # Add Result Text
    # ------------------------------

    color = (0,255,0)


    if status == "Cavity Detected":

        color = (0,0,255)



    cv2.putText(
        final,
        f"{status} {percentage}%",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )



    # ------------------------------
    # Save Final Image
    # ------------------------------

    final_path = os.path.join(
        PROCESSED_FOLDER,
        "final_" + filename
    )


    cv2.imwrite(
        final_path,
        final
    )



    return {

        "original": image_path,

        "gray": gray_path,

        "threshold": threshold_path,

        "edge": edge_path,

        "final": final_path,

        "status": status,

        "percentage": percentage

    }