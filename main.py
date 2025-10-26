import io
from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import cv2

app = FastAPI()

# Load your finetuned model
# Make sure the model file is in the same directory or provide the correct path
model = YOLO("YOLOV8s_Barcode_Detection.pt")

@app.post("/decode_qr/")
async def decode_qr_from_image(file: UploadFile = File(...)):
    """
    Accepts an image file, detects a QR code, crops it, decodes it, and returns the data.
    """
    # Read image file from the upload
    contents = await file.read()
    
    # Convert the bytes to a NumPy array and then to an OpenCV image
    nparr = np.frombuffer(contents, np.uint8)
    img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform object detection on the image
    # The model expects a cv2 image (BGR)
    results = model(img_cv)

    # Convert the OpenCV image (BGR) to a PIL Image (RGB) for cropping
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

    decoded_results = []

    # Loop through the detected bounding boxes
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Get bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Crop the image using PIL
            cropped_img = img_pil.crop((x1, y1, x2, y2))

            # Decode the QR code from the cropped image
            decoded_objects = decode(cropped_img)

            if decoded_objects:
                for obj in decoded_objects:
                    decoded_results.append({
                        "type": obj.type,
                        "data": obj.data.decode('utf-8')
                    })

    if not decoded_results:
        return {"message": "No QR code found or could not be decoded."}

    return {"decoded_qrs": decoded_results}

@app.get("/")
def read_root():
    return {"message": "Welcome to the QR Code Decoder API. Send a POST request to /decode_qr/ with an image."}
