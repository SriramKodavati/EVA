import cv2
import os
import numpy as np
import pytesseract
from pytesseract import Output
import psycopg2
from fuzzywuzzy import process, fuzz
from dateutil import parser
import re

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def beginOCR(imgDirPath):         #Optical Character Recognition from the images.
    conn = psycopg2.connect(
    host="localhost",
    database="EVA",
    user="postgres",
    password="postgres"
    )
    cur = conn.cursor()

    pillInfo = {}
    
    preDrugInfo = {
        #'rosuvastatin':{'medicineName':'Rosuvastatin','dateFilled':'6/2/22','quantity':30,'refillsLeft':5},
        'tamsulosin hcl':{'medicineName':'tamsulosin hcl','dateFilled':'11/03/2021','quantity':90,'refillsLeft':3}
    }

    print("Starting Tesseract OCR..!") #Beginning text extraction using Tesseract OCR.
    #medicineNames = ["ROSUVASTATIN", "Tamsulosin HCL 0.4 MG cap sunp", "Cyclobenzaprine 5 MG", "docusate sodium 100 MG capsule", "Ibuprofen Tablet 800 MG"] 

    #Getting medicine names from database
    medicineNames = []
    cur.execute("select name from medicines")
    data = cur.fetchall()

    for i in range(0,len(data)):
        medicineNames.append(data[i][0])
    print(medicineNames)

    #Pill table attributes intialization.
    pillInfo['medicineName'] = "MedicineNameNone"
    pillInfo['dateFilled'] = 9/9/99
    pillInfo['quantity'] = 99
    pillInfo['refillsLeft'] = 9
    pillInfo['frontImagePath'] = "FolderPathNone"  
    pillInfo['folderPath'] = imgDirPath
    #imageFolderPath variable will be initialized when capturing the images itself.  

    percentage = 0
    matchedtext = "" #Matched extracted text.
    extractedTexts = [] #Variable to store extracted texts.
    for image_name in os.listdir(imgDirPath):        #Iterates over each image of the pill bottle and extracts texts. 
        tempTexts = []

        image = cv2.imread(os.path.join(imgDirPath,image_name))

        #preprocess image
        gray = get_grayscale(image)
        thresh = thresholding(gray)

        # Get OCR output using Pytesseract
        custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-:" " --oem 3'

        print("{} output".format(image_name))
        
        print(pytesseract.image_to_string(thresh, config=custom_config))

        extractedTexts.extend(pytesseract.image_to_string(thresh, config=custom_config).splitlines())
        extractedTexts.extend(pytesseract.image_to_string(image, config=custom_config).splitlines())
        print(extractedTexts)
        if len(extractedTexts) > 0:
            for i in range(0,len(medicineNames)):
                matches = process.extract(medicineNames[i],extractedTexts, scorer=fuzz.ratio)
                print("Percentages:\n",matches[0][1])
                if matches[0][1] > percentage and matches[0][1]>30:
                    percentage = matches[0][1]
                    pillInfo['medicineName'] = medicineNames[i]
                    matchedtext = matches[0][0]
                    pillInfo['frontImagePath'] = os.path.join(imgDirPath,image_name)
    
    if pillInfo['medicineName'].lower() in preDrugInfo:
        pillInfo['dateFilled'] = preDrugInfo[pillInfo['medicineName'].lower()]['dateFilled']
        pillInfo['quantity'] = preDrugInfo[pillInfo['medicineName'].lower()]['quantity']
        pillInfo['refillsLeft'] = preDrugInfo[pillInfo['medicineName'].lower()]['refillsLeft']
    else:
        if len(extractedTexts) > 0:
            #Extracting datefilled texts
            dateFilledTexts = ["datefilled","filled","date filled"]
            similarTexts = []
            for i in range(0,len(dateFilledTexts)):
                matches = process.extract(dateFilledTexts[i],extractedTexts, scorer=fuzz.ratio)
                if i in range(len(matches)):
                    if re.search(r'\d',matches[i][0]):
                        print("strings with nos: ",matches[i][0],matches[i][1])
                        if matches[i][1] > 50:
                            print(matches[0][1],matches[0][0])
                            similarTexts.append(matches[0][0])

            print("Texts with date filled words..!\n", similarTexts)
            noDateExtracted = True
            for i in range(0,len(similarTexts)):
                try:
                    pillInfo['dateFilled'] = parser.parse(similarTexts[i],fuzzy=True).date()
                    noDateExtracted = False
                    break
                except:
                    print("except block")
                    continue
            if noDateExtracted:
                print("date not extracted..!")
                pillInfo['dateFilled'] = "not found..!" #NULL/None can be used for database

            print("Date filled is {}\n".format(pillInfo['dateFilled']))

            #Extracting quantity
            quantityTexts = ["QTY","qty"]
            percentage = 0
            quantityText = ""
            for i in range(0,len(quantityTexts)):
                matches = process.extract(quantityTexts[i],extractedTexts,scorer=fuzz.ratio)
                for i in range(0,len(matches)):
                    if re.search(r'\d',matches[i][0]):
                        if matches[i][1] > percentage:
                            quantityText = matches[i][0]
                
            if quantityText == "":
                print("Quantity not extracted..!")
            else:
                print("Quantity extracted text..!",quantityText)
                temp = re.findall(r'\d+',quantityText)
                pillInfo['quantity'] = temp[0]
    print(pillInfo)
    cur.close()
    conn.close()
    return pillInfo

beginOCR("C:\EVA\integrate\iphoneCaptures\medicine1")



