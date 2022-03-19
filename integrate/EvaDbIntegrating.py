#Here we integrated both the capture of images and text recognition programs.
from cgitb import text
import cv2
import os 
import numpy as np
import pytesseract
from pytesseract import Output
import psycopg2
from fuzzywuzzy import process,fuzz

#Establishes connection to database.
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()
#cur.execute("select count from pillbottlecount")
pillBottleCount = 0
isCaptureImages = True
#pillBottleCount = cur.fetchone()[0] #Keeps track of no of pill bottles captured. 
folderPath = 'C:/EVA/pillbottles' #folder path to create a folder and save captured images.

for base, dirs, files in os.walk(folderPath):
    print('Searching in : ',base)
    for directories in dirs:
        pillBottleCount += 1

medicineNames = ["ROSUVASTATIN", "Tamsulosin HCL 0.4 MG cap sunp", "Cyclobenzaprine 5 MG", "docusate sodium 100 MG capsule", "Ibuprofen Tablet 800 MG"]

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


while isCaptureImages:
    beginOCR = False #Decides when to start OCR.
    medicineFolderPath = "" #temp variable that holds path to the medicine.
    mainImagePath = "" #Path of image with medicine name.
    extractedTexts = []
    img_counter = 0 #count of no of images captured.
    
    #Code below is to capture images. 
    font = cv2.FONT_HERSHEY_SIMPLEX 
    displayedText = "Position the bottle in the box and take pictures covering entire label."

    #folder creation for each pill bottle.
    pillBottleCount += 1
    folderName = 'pillbottle' + str(pillBottleCount)
    IMG_DIR = os.path.join(folderPath,folderName)
    medicineFolderPath = IMG_DIR
    cam = cv2.VideoCapture(0)  #opens the camera. 

    width = cam.get(cv2.CAP_PROP_FRAME_WIDTH )
    height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT )

    while True:
        ret, frame = cam.read()
        cv2.putText(frame, displayedText, (round(width*0.08),round(height*0.1)), font, 0.5, (255,255,255), 1, cv2.LINE_AA) 
        cv2.rectangle(frame, (round(width*0.3),round(height*0.2)), (round(width*0.7),round(height*0.9)), (255,255,255), 2)
        cv2.imshow('test', frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            break
        elif k%256 == 32:
            img_counter += 1
            imageName = "Image" + str(img_counter) + ".png"
            try:
                if not os.path.isdir(IMG_DIR):
                    os.mkdir(IMG_DIR)
                ret1, frame1 = cam.read()
                cv2.imwrite(os.path.join(IMG_DIR,imageName),frame1)
                print("{} written".format(imageName))
            except OSError as error:
                print("Error creating or saving a image to the folder\n",error)
    cam.release()
    cv2.destroyAllWindows()

    beginOCR = True #Starting character recognition for each image. 

    if beginOCR:
        print("Starting Tesseract OCR..!") #Beginning text extraction using Tesseract OCR. 

        percentage = 0
        medicineName = ""
        matchedtext = ""

        print('\n-----------------------------------------')
        print('TESSERACT OUTPUT --> Original Image')
        print('-----------------------------------------')

        
        for image_name in os.listdir(IMG_DIR):
            texts = [] #Temporary variable for each image texts. 

            image = cv2.imread(os.path.join(IMG_DIR,image_name))

            #preprocess image
            gray = get_grayscale(image)
            thresh = thresholding(gray)

            # Get OCR output using Pytesseract
            custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-:" " --oem 3'

            print("{} output".format(image_name))
            
            print(pytesseract.image_to_string(thresh, config=custom_config))

            texts.extend(pytesseract.image_to_string(thresh, config=custom_config).splitlines())
            texts.extend(pytesseract.image_to_string(image, config=custom_config).splitlines())

            for i in range(0,len(medicineNames)):
                matches = process.extract(medicineNames[i],texts, scorer=fuzz.ratio)
                if matches[0][1] > percentage:
                    percentage = matches[0][1]
                    medicineName = medicineNames[i]
                    matchedtext = matches[0][0]
                    mainImagePath = os.path.join(IMG_DIR,image_name)
            
            extractedTexts.extend(texts) 

        #store the data in DB.
        #cur.execute("insert into medicines values (DEFAULT, {m}, '08/20/1998', '30', '3', {i}, {f});".format(m=medicineName,i=mainImagePath,f=medicineFolderPath))
        sql_stmt = """insert into medicines(name,datefilled,quantity,refillsleft,imagepath,folderpath) values(%s,%s,%s,%s,%s,%s)"""
        data = (medicineName,'08/20/1998','30', '3', mainImagePath, medicineFolderPath)
        cur.execute(sql_stmt,data)
        conn.commit()

    img_counter = 0

    conn.commit()
    
    print("Do you want to capture images of another pill bottle[y/n]?")
    userInput = str(input())
    print(userInput)
    if(userInput=='n'):
        print("No further capturing..!")
        isCaptureImages = False

conn.commit()
#Commiting the data to the DB and closing the connection.
cur.close()
conn.close()
