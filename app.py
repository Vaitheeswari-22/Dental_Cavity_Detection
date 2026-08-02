from flask import Flask, render_template, request
import os
from image_processing import detect_cavity


app = Flask(__name__)


# Folder paths
UPLOAD_FOLDER = "static/uploads"
PROCESSED_FOLDER = "static/processed"


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER



# Create folders automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)



# Home page
@app.route("/")
def home():
    return render_template("index.html")



# Upload image
@app.route("/upload", methods=["POST"])
def upload():

    # Check image exists
    if "image" not in request.files:
        return "No image uploaded"



    file = request.files["image"]



    # Empty filename check
    if file.filename == "":
        return "No image selected"



    # Save uploaded image

    upload_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )


    file.save(upload_path)



    # Send image for processing

    result = detect_cavity(upload_path)



    # Show result page

    return render_template(
        "result.html",

        original=result.get("original"),

        gray=result.get("gray"),

        threshold=result.get("threshold"),

        edge=result.get("edge"),

        final=result.get("final"),

        result=result.get("status"),

        percentage=result.get("percentage")
    )




if __name__ == "__main__":

    app.run(
        debug=True
    )