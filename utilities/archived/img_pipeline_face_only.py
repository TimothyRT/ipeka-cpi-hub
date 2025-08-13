import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO

import os
import shutil


PREDICTION_PATH = os.path.join('.', 'predictions')  # not sure what this is


def load_od_model() -> YOLO:
    finetuned_model = YOLO('utilities/face_detection_best.pt')
    return finetuned_model


def inference(input_image_path: str, im_size=(400, 600)):
    finetuned_model: YOLO = load_od_model()
    results = finetuned_model.predict(input_image_path, 
                        show=False, 
                        save=True,
                        save_crop=False,
                        imgsz=im_size,
                        conf=0.6,
                        save_txt=True,  
                        project=PREDICTION_PATH, 
                        show_labels=False,
                        show_conf=False,
                        line_width=2,
                        exist_ok=True)

    names = finetuned_model.names
    nfaces = 0  # number of faces detected in picture
    for r in results:
        print(f"!!! {r.boxes.xyxy = }")
        for c in r.boxes.cls:
            nfaces += 1
            
    return {
        "x1": max(0, int(results[0].boxes.xyxy[0][0] - 125)),
        "y1": max(0, int(results[0].boxes.xyxy[0][1] - 75)),
        "x2": min(im_size[0] - 1, int(results[0].boxes.xyxy[0][2] + 125)),
        "y2": min(im_size[1] - 1, int(results[0].boxes.xyxy[0][3] + 175))
    }
        

def files_cleanup(path_: str):
    if os.path.exists(path_):
        os.remove(path_)
    shutil.rmtree(PREDICTION_PATH)


def get_upload_path():
    upload_file_path = os.path.join('.', 'uploads')
    if not os.path.exists(upload_file_path):
        os.makedirs(upload_file_path)
    upload_filename = "input.jpg"
    upload_file_path = os.path.join(upload_file_path, upload_filename)
    return upload_file_path


def process_input_image(input_image_path: str, output_image_path: str, im_size=(400, 600)):
    try:
        assert os.path.exists(input_image_path)
    except AssertionError:
        print(f"[ASSERTION] Image path doesn't exist!")
        
    input_image = cv2.imread(input_image_path)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    input_image = cv2.resize(input_image, im_size)
    cv2.imwrite(output_image_path, cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)) 
    return output_image_path


def crop_image(input_image_path: str, output_image_path: str, boundaries: dict):
    img = cv2.imread(input_image_path)
    cropped = img[boundaries["y1"]:boundaries["y2"], boundaries["x1"]:boundaries["x2"]]
    cv2.imwrite(output_image_path, cropped)


if __name__ == "__main__":
    v2_image_path = process_input_image(
        input_image_path = "static/images/downloaded/employees/RO/EVELYN SUMENDAP.JPG",
        output_image_path = "static/images/downloaded/employees/RO/EVELYN SUMENDAP v2.JPG",
        im_size = tuple([400, 600]))
    boundaries = inference(
        input_image_path = v2_image_path,
        im_size = tuple([400, 600]))
    print(f"{boundaries = }")
    crop_image(v2_image_path, "a.png", boundaries)
    files_cleanup(v2_image_path)
