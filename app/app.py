from flask import Flask, request
import os
from moduls import blureFace_dir,blureFace_file
import time
import cv2 as cv
import numpy as np
from logger import create_logger



app = Flask(__name__)

@app.route('/blur-dir', methods=['POST'])
def blur():
    LOGGER = create_logger("blur_log")
    LOGGER.info(f"blur-dir-path request recived")
    if request.is_json:
        fd_threshold=request.data["df_threshold"]
        data = request.get_json()
        print(f'Received data: {data}')
        car_directory = data.get('car directory')
        LOGGER.info(f"{car_directory} is  being sent or blurring")
        blurred_images = blureFace_dir(car_directory,fd_threshold,LOGGER)
        LOGGER.info(f"{car_directory} has done blurring proccess")
        #blur_status options - blurred, no_detections, 
        return blurred_images,200

# recives a requestcontaining binary files
@app.route('/blur-file', methods=['POST']) 
def blur_file():
    LOGGER = create_logger("blur_log")
    LOGGER.info(f"blur-file request recived")
    req_data = request.get_json()
    images=req_data["images"]
    fd_threshold=req_data["fd_threshold"]
    LOGGER.info(f"sent to blur")
    blurred_images = blureFace_file(images,fd_threshold,LOGGER)
    LOGGER.info(f"recived from blur")
         
    return blurred_images,200




@app.route('/blur-test-local')
def blur_test_local():
        LOGGER = create_logger("blur_log")
        images=[]
        LOGGER.info(f"blurring test request recived")
        print(f'blur request recived')
        car_directory = "app/images_to_blur"
        images=os.listdir(car_directory)
        for img in images:
             images.append=cv.imread(f'{car_directory}/{img}')
        LOGGER.info(f"proccess started")
        blurred_images = blureFace_file(images,0.4,LOGGER)
        LOGGER.info(f"proccess ended")
        print(f'detected faces in {len(blurred_images)} images' )
        LOGGER.info(f'blur proccess ended blurred {len(blurred_images)} images')
        return  f'blur proccess ended blurred {len(blurred_images)} images'
    



@app.route('/isAlive',methods=['GET','POST'])
def is_alive():
    if request.method=="GET":
        return 'server is alive, "GET" request recived'
    if request.method=="POST":
        return 'server is alive, "POST" request recived'
 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)