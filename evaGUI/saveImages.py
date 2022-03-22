import cv2
import os
import numpy as np

def saveImages(images):
    pillBottleCount = 0 #count of no of pill bottles already in the folder. 
    folderPath = 'C:/EVA/pillbottles' #folder path to create a folder and save captured images.
    if len(images) != 0:
        for base, dirs, files in os.walk(folderPath):
            for directories in dirs:
                pillBottleCount += 1
        pillBottleCount += 1
        folderName = 'pillbottle' + str(pillBottleCount) #new folder path to store the current images.
        IMG_DIR = os.path.join(folderPath,folderName)
        if not os.path.isdir(IMG_DIR):
            os.mkdir(IMG_DIR)
        else:
            print("folder path already exists")
        imageCount = 1 #Used as image name in the folder saved.
        for img in images:
            imageName = "Image" + str(imageCount) + ".png" 
            cv2.imwrite(os.path.join(IMG_DIR,imageName),img)
            imageCount += 1
    return IMG_DIR