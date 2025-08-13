import cv2
import numpy as np
import streamlit as st
import torch
from PIL import Image
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
from ultralytics import YOLO

import os
import pathlib
import shutil


#####
# For face detection

PREDICTION_PATH = os.path.join('.', 'predictions')  # not sure what this is


#####
# For background removal

torch.set_float32_matmul_precision(["high", "highest"][0])

transform_image = transforms.Compose(
    [
        transforms.Resize((1024, 1024)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)


####
# Load model

def load_od_model() -> YOLO:
    finetuned_model = YOLO('utilities/face_detection_best.pt')
    return finetuned_model


def load_segmentation_model():
    birefnet = AutoModelForImageSegmentation.from_pretrained(
        "ZhengPeng7/BiRefNet", trust_remote_code=True
    )
    return birefnet


def files_cleanup(path_: str):
    if os.path.exists(path_):
        os.remove(path_)


def process_input_image(input_image_path: str, output_image_path: str, im_size=(400, 600)):
    try:
        assert os.path.exists(input_image_path)
        print(f"Image: {input_image_path}")
    except AssertionError:
        print(f"[ASSERTION] Image path doesn't exist!")
        
    input_image = cv2.imread(input_image_path)
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    input_image = cv2.resize(input_image, im_size)
    cv2.imwrite(output_image_path, cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR))


def crop_image(input_image_path: str, output_image_path: str, boundaries: dict):
    img = cv2.imread(input_image_path)
    cropped = img[boundaries["y1"]:boundaries["y2"], boundaries["x1"]:boundaries["x2"]]
    cv2.imwrite(output_image_path, cropped)


def detect_face(input_image_path: str, im_size=(400, 600)):
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
    
    
def remove_image_background(input_image_path: str, output_image_path: str):
    img = Image.open(input_image_path)
    img = img.convert("RGB")
    img_size = img.size
    input_images = transform_image(img).unsqueeze(0)
    with torch.no_grad():  # prediction
        birefnet = load_segmentation_model()
        preds = birefnet(input_images)[-1].sigmoid()
    pred = preds[0].squeeze()
    pred_pil = transforms.ToPILImage()(pred)
    mask = pred_pil.resize(img_size)
    img.putalpha(mask)
    img.save(output_image_path)
    
    
def pipeline(input_directory: str, output_directory: str, verbose=True):
    for root, dirs, files in os.walk(input_directory):
            print(f"Current directory: {root}") if verbose == True else None
            print(f"Files: {files}") if verbose == True else None
            
            for i, file in enumerate(files):
                print(f">> [File #{i}]")
                
                last_folder = pathlib.Path(root).name  # should be the containing folder, for example "RO"
                
                file_path = {
                    0: os.path.join(root, file),
                    1: os.path.join(output_directory, file.replace('.JPG', ' v2.JPG')),
                    2: os.path.join(output_directory, file.replace('.JPG', ' v3.JPG')),
                    3: os.path.join(output_directory, file.replace('JPG', 'png')),
                }
                
                if os.path.exists(file_path[3]):
                    continue
                
                process_input_image(
                    input_image_path = file_path[0],
                    output_image_path = file_path[1],
                    im_size = tuple([400, 600]))
                
                boundaries = detect_face(
                    input_image_path = file_path[1],
                    im_size = tuple([400, 600]))
                
                crop_image(
                    input_image_path=file_path[1],
                    output_image_path=file_path[2],
                    boundaries=boundaries)
                
                remove_image_background(
                    input_image_path=file_path[2],
                    output_image_path=file_path[3])
                
                files_cleanup(file_path[1])
                files_cleanup(file_path[2])
                shutil.rmtree(PREDICTION_PATH)
            
            print("-" * 20) if verbose == True else None


if __name__ == "__main__":
    pipeline(
        input_directory='static/images/downloaded/employees',
        output_directory='static/images/processed/employees',
    )
