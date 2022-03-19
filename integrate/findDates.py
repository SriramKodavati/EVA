import cv2
import os 
import numpy as np
import re
import pytesseract
from pytesseract import Output

IMG_DIR="C:\EVA\integrate\iphoneCaptures\medicine1"
custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-:" " --oem 3'
extractedTexts = []
extractedDates = []

'''
date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20|21|22)\d\d$'
date_pattern_test = '^([0-9]|[0-9][0-9]/[0-9]|[0-9][0-9]/[0-9][0-9]|[0-9][0-9][0-9][0-9])\d\d$'
date_pattern_test2 = '^([1-9]|1[0-2])(\.|-|/)([1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)20[0-9][0-9]$'
date_pattern_test3 = '^([1-9]|1[0-2]|0[1-9])(\.|-|/)(0[1-9]|[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)(20[0-9][0-9]|2[0-9])$'
'''

date_pattern_test4 = '^(.*?([1-9]|1[0-2]|0[1-9])(\.|-|/)(0[1-9]|[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)(20[0-9][0-9]|2[0-9]).*?)$'

image = cv2.imread(os.path.join(IMG_DIR,'Image3.jpeg'))
extractedTexts.extend(pytesseract.image_to_string(image, config=custom_config).splitlines())
extractedTexts.append("6/2/21")

print("Extracted texts from original image")
print(extractedTexts)

for i in range(len(extractedTexts)):
    if re.search(date_pattern_test4,extractedTexts[i],re.IGNORECASE):
        extractedDates.append(extractedTexts[i])

print(extractedDates)

'''
if re.match(date_pattern,"12/12/2001"):
    print("matched..!")
else:
    print("not matched..!")
'''