import os
import cv2
import numpy as np


# ==========================================================
# Processed Folder
# ==========================================================

PROCESSED_FOLDER = "static/processed"
os.makedirs(PROCESSED_FOLDER, exist_ok=True)



# ==========================================================
# Prediction Function (Temporary OpenCV Demo)
# ==========================================================

def predict_with_model(image_path):

    img = cv2.imread(image_path)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    mean_value = np.mean(gray)


    # Dark region அதிகம் இருந்தால் cavity என்று demo
    if mean_value < 100:

        status = "Cavity Detected"
        confidence = 80.0

    else:

        status = "Normal Tooth"
        confidence = 90.0


    return status, confidence




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
    # Prediction
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